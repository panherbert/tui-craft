"""Run via python -B -m unittest discover -s examples/tools -v."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).with_name('pty_fixture.py')
spec = importlib.util.spec_from_file_location('pty_probe', ROOT/'scripts/pty_probe.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

@unittest.skipUnless(os.name == 'posix', 'POSIX PTY only')
class ProbeTests(unittest.TestCase):
    def run_case(self, steps, extra=()):
        return probe.probe([sys.executable, '-B', str(FIXTURE), *extra], {'steps':[{'expect':'READY'}, *steps]}, timeout=2)

    def test_input_resize_clean_exit(self):
        r, data = self.run_case([{'resize':[60,18]}, {'expect':'SIZE:60x18'}, {'send':'q'}])
        self.assertIsNone(r['failure'])
        self.assertEqual(r['returncode'], 0)
        self.assertTrue(r['flags_restored'])
        self.assertIn(b'INPUT:71', data)

    def test_raw_ctrl_c(self):
        r, _ = self.run_case([{'send':'\x03'}])
        self.assertEqual(r['returncode'], 130)
        self.assertTrue(r['flags_restored'])

    def test_sigterm(self):
        r, _ = self.run_case([{'signal':'SIGTERM'}])
        self.assertEqual(r['returncode'], 143)
        self.assertTrue(r['flags_restored'])

    def test_exception_cleanup(self):
        r, _ = self.run_case([{'send':'!'}])
        self.assertEqual(r['returncode'], 1)
        self.assertTrue(r['flags_restored'])

    def test_dirty_exit_detected(self):
        r, _ = self.run_case([{'send':'q'}], ['--dirty'])
        self.assertFalse(r['flags_restored'])

    def test_missing_expectation_fails(self):
        r, _ = self.run_case([{'send':'q'}, {'expect':'NOT-PRINTED'}])
        self.assertIn('not observed', r['failure'])

    def test_timeout_is_failure(self):
        r, _ = probe.probe([sys.executable,'-c','import time; time.sleep(10)'], {}, timeout=.1)
        self.assertIn('timeout', r['failure'])
        self.assertNotEqual(r['returncode'], 0)

    def test_cli_creates_artifacts_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            scenario = d/'s.json'
            scenario.write_text(json.dumps({'steps':[{'expect':'READY'},{'send':'q'}]}))
            args=[sys.executable, '-B', str(ROOT/'scripts/pty_probe.py'), '--scenario',str(scenario),'--out',str(d/'result'),'--',sys.executable,'-B',str(FIXTURE)]
            first=subprocess.run(args,capture_output=True)
            self.assertEqual(first.returncode,0,first.stderr)
            self.assertTrue(json.loads((d/'result/result.json').read_text())['passed'])
            self.assertTrue((d/'result/output.bin').exists())
            self.assertEqual(subprocess.run(args,capture_output=True).returncode,2)

    def test_invalid_scenario(self):
        for value in ({'size':[0,20]}, {'steps':[{'signal':'SIGKILL'}]}, {'steps':[{'wait':99}]}, {'steps':[{'send':'a','wait':1}]}):
            with self.assertRaises(ValueError):
                probe.validate(value)


class PackageTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run([sys.executable, '-B', str(ROOT/'scripts/package_skill.py'), *map(str,args)], capture_output=True, text=True)

    def test_structure_and_links(self):
        r = self.run_tool('check')
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_reproducible_archive_and_no_overwrite(self):
        import zipfile
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d)/'a.zip', Path(d)/'b.zip'
            for path in (a,b):
                r = self.run_tool('build','--out',path)
                self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertNotEqual(self.run_tool('build','--out',a).returncode,0)
            with zipfile.ZipFile(a) as z:
                self.assertIn('tui-craft/SKILL.md', z.namelist())
                self.assertIsNone(z.testzip())
                self.assertTrue(all(n.startswith('tui-craft/') for n in z.namelist()))

    def test_install_refuses_existing_skill(self):
        with tempfile.TemporaryDirectory() as d:
            r = self.run_tool('install','--dest',d)
            self.assertEqual(r.returncode,0,r.stderr)
            skill=Path(d)/'tui-craft/SKILL.md'
            skill.write_text('existing user content')
            self.assertNotEqual(self.run_tool('install','--dest',d).returncode,0)
            self.assertEqual(skill.read_text(),'existing user content')

    def test_missing_link_is_rejected(self):
        import shutil
        spec = importlib.util.spec_from_file_location('package_skill', ROOT/'scripts/package_skill.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'skill'
            shutil.copytree(ROOT,dest)
            (dest/'bad.md').write_text('[missing](does-not-exist.md)')
            with self.assertRaisesRegex(ValueError,'broken'):
                module.check(dest)

if __name__ == '__main__':
    unittest.main()
