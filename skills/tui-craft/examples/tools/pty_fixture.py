"""Synthetic lifecycle fixture for the probe tests, not an application starter."""
import os
import signal
import sys
import termios
import tty

original = termios.tcgetattr(0)
done = False
code = 0

def stop(signum, frame):
    global done, code
    done, code = True, 128 + signum
    # Interrupt a blocking read via a short timeout configured below.

def size(signum=None, frame=None):
    s = os.get_terminal_size(0)
    os.write(1, f'SIZE:{s.columns}x{s.lines}\n'.encode())

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGWINCH, size)
try:
    tty.setraw(0)
    attrs = termios.tcgetattr(0)
    attrs[6][termios.VMIN], attrs[6][termios.VTIME] = 0, 1
    termios.tcsetattr(0, termios.TCSANOW, attrs)
    os.write(1, b'READY\n')
    while not done:
        data = os.read(0, 1024)
        if b'\x03' in data:
            done, code = True, 130
        if b'q' in data:
            done = True
        if b'!' in data:
            raise RuntimeError('injected failure')
        if data:
            os.write(1, b'INPUT:' + data.hex().encode() + b'\n')
finally:
    if '--dirty' not in sys.argv:
        termios.tcsetattr(0, termios.TCSANOW, original)
sys.exit(code)
