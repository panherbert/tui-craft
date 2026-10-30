#!/usr/bin/env python3
"""Run a bounded POSIX PTY scenario, recording bytes and terminal flags (not pixels).

Requires Python >=3.9 on macOS/Linux; stdlib only. The child command runs with
normal user permissions. Use isolated fixtures, not an attached production app.
See references/tools.md for JSON steps, examples and evidence limitations.
"""
import argparse
import errno
import json
import os
from pathlib import Path
import select
import signal
import struct
import sys
import time


def terminal_flags(fd):
    import termios
    a = termios.tcgetattr(fd)
    result = {}
    for index, names in [(0, ('BRKINT','ICRNL','INPCK','ISTRIP','IXON')),
                         (1, ('OPOST',)), (3, ('ECHO','ICANON','IEXTEN','ISIG'))]:
        for name in names:
            result[name] = bool(a[index] & getattr(termios, name))
    for name in ('VMIN','VTIME'):
        value = a[6][getattr(termios, name)]
        result[name] = value if isinstance(value, int) else value[0]
    return result


def validate(scenario):
    if not isinstance(scenario, dict):
        raise ValueError('scenario must be a JSON object')
    if set(scenario) - {'size', 'steps'}:
        raise ValueError('scenario accepts only size and steps')
    size = scenario.get('size', [80, 24])
    def valid_size(value):
        return isinstance(value, list) and len(value) == 2 and all(type(n) is int and 1 <= n <= 1000 for n in value)
    if not valid_size(size):
        raise ValueError('size must be [cols, rows], each 1..1000')
    steps = scenario.get('steps', [])
    if not isinstance(steps, list):
        raise ValueError('steps must be a list')
    for step in steps:
        if not isinstance(step, dict) or len(step) != 1:
            raise ValueError('each step needs exactly one operation')
        op, value = next(iter(step.items()))
        if op == 'wait':
            if type(value) not in (int, float) or not 0 <= value <= 10:
                raise ValueError('wait must be 0..10 seconds')
        elif op in ('send', 'expect'):
            if not isinstance(value, str) or (op == 'expect' and not value):
                raise ValueError(f'{op} needs a nonempty string' if op == 'expect' else 'send needs a string')
        elif op == 'resize':
            if not valid_size(value):
                raise ValueError('resize must be [cols, rows], each 1..1000')
        elif op == 'signal':
            if value not in ('SIGINT', 'SIGTERM', 'SIGHUP', 'SIGCONT'):
                raise ValueError('signal must be SIGINT, SIGTERM, SIGHUP or SIGCONT')
        else:
            raise ValueError(f'unknown operation: {op}')
    return size, steps


def probe(command, scenario, timeout=8, max_bytes=4*1024*1024):
    import fcntl
    import termios
    size, steps = validate(scenario)
    master, slave = os.openpty()
    def resize(value):
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', value[1], value[0], 0, 0))
    resize(size)
    before = terminal_flags(slave)
    pid = os.fork()
    if pid == 0:
        try:
            os.close(master)
            os.setsid()
            fcntl.ioctl(slave, termios.TIOCSCTTY, 0)
            for fd in (0, 1, 2):
                os.dup2(slave, fd)
            if slave > 2:
                os.close(slave)
            env = dict(os.environ, TERM=os.environ.get('TERM') or 'xterm-256color')
            if env['TERM'] == 'dumb':
                env['TERM'] = 'xterm-256color'
            os.execvpe(command[0], command, env)
        except BaseException as exc:
            os.write(2, (str(exc) + '\n').encode())
            os._exit(127)
    output = bytearray()
    status = None
    deadline = time.monotonic() + timeout
    failure = None
    completed = 0
    cursor = 0
    def drain(duration):
        nonlocal status
        stop = min(deadline, time.monotonic() + duration)
        while time.monotonic() < stop:
            if select.select([master], [], [], max(0, min(.05, stop-time.monotonic())))[0]:
                try:
                    data = os.read(master, 65536)
                except OSError as exc:
                    if exc.errno != errno.EIO:
                        raise
                    data = b''
                output.extend(data)
                if len(output) > max_bytes:
                    raise ValueError('output limit exceeded')
            if status is None:
                found, value = os.waitpid(pid, os.WNOHANG)
                if found:
                    status = value
    try:
        for step in steps:
            if time.monotonic() >= deadline:
                failure = 'scenario timeout'
                break
            op, value = next(iter(step.items()))
            if op == 'wait':
                drain(value)
            elif op == 'send':
                data = memoryview(value.encode('utf-8'))
                while data:
                    if time.monotonic() >= deadline:
                        raise ValueError('send timeout')
                    if select.select([], [master], [], .02)[1]:
                        data = data[os.write(master, data[:4096]):]
                    drain(.001)
            elif op == 'resize':
                resize(value)  # kernel sends SIGWINCH to foreground process group
                drain(.05)
            elif op == 'signal':
                os.killpg(pid, getattr(signal, value))
            elif op == 'expect':
                wanted = value.encode('utf-8')
                while output.find(wanted, cursor) < 0 and status is None and time.monotonic() < deadline:
                    drain(.05)
                position = output.find(wanted, cursor)
                if position < 0:
                    failure = f'expected bytes not observed: {value!r}'
                    break
                cursor = position + len(wanted)
            completed += 1
        while status is None and time.monotonic() < deadline and failure is None:
            drain(.05)
        if status is None and failure is None:
            failure = 'process did not exit before timeout'
        # Sample before harness-forced termination: do not mistake forced cleanup for app cleanup.
        # On macOS the slave may be invalid after child exit; the master remains queryable.
        after = terminal_flags(master)
        drain(.05)
    except (OSError, ValueError) as exc:
        failure = str(exc)
        after = terminal_flags(master)
    finally:
        if status is None:
            try:
                os.killpg(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            _, status = os.waitpid(pid, 0)
        # Remove any same-group children left behind by the isolated command.
        try:
            os.killpg(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        os.close(master)
        os.close(slave)
    result = dict(command=command, size=size, completed_steps=completed, total_steps=len(steps),
                  returncode=os.waitstatus_to_exitcode(status), failure=failure,
                  flags_before=before, flags_after=after, flags_restored=before == after,
                  captured_bytes=len(output),
                  evidence='PTY bytes/process/termios only; no emulator or physical pointer observation')
    return result, bytes(output)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scenario', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True, help='new output directory (never overwritten)')
    p.add_argument('--timeout', type=float, default=8, help='total time limit, 0 < seconds <= 60')
    p.add_argument('--expect-exit', type=int, default=0)
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    command = a.command[1:] if a.command[:1] == ['--'] else a.command
    if os.name != 'posix' or not command or not 0 < a.timeout <= 60:
        p.error('requires POSIX, a command after --, and timeout in (0,60]')
    try:
        scenario = json.loads(a.scenario.read_text())
        validate(scenario)
        a.out.mkdir(parents=True, exist_ok=False)
        result, output = probe(command, scenario, a.timeout)
        result['expected_returncode'] = a.expect_exit
        result['passed'] = result['failure'] is None and result['returncode'] == a.expect_exit and result['flags_restored']
        (a.out / 'output.bin').write_bytes(output)
        (a.out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))
        return 0 if result['passed'] else 1
    except (OSError, ValueError, TypeError) as exc:
        p.exit(2, f'pty_probe: {exc}\n')

if __name__ == '__main__':
    sys.exit(main())
