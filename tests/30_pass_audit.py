#!/usr/bin/env python3
# pass audit - Password Store Extension (https://www.passwordstore.org/)
# Copyright (C) 2018 Alexandre PUJOL <alexandre@pujol.io>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import unittest
import setup


class TestPassAuditCMD(setup.TestPass):

    def _passaudit(self, cmd, code=None):
        if code is None:
            self.passaudit.main(cmd)
        else:
            with self.assertRaises(SystemExit) as cm:
                self.passaudit.main(cmd)
            self.assertEqual(cm.exception.code, code)

    def test_pass_audit_help(self):
        """Testing: pass audit --help."""
        cmd = ['--help']
        self._passaudit(cmd, 0)

    def test_pass_audit_version(self):
        """Testing: pass audit --version."""
        cmd = ['--version']
        self._passaudit(cmd, 0)

    def test_pass_audit_PathsNotPresent(self):
        """Testing: empty paths."""
        cmd = []
        self._passaudit(cmd, 1)

    def test_pass_audit_NotAnOption(self):
        """Testing: pass audit --not-an-option."""
        cmd = ['--not-an-option', '-q']
        self._passaudit(cmd, 2)

    def test_pass_audit_StoreNotInitialized(self):
        """Testing: store not initialized."""
        cmd = ['Password/', '-v']
        os.rename(os.path.join(self.store.prefix, '.gpg-id'),
                  os.path.join(self.store.prefix, 'backup.gpg-id'))
        self._passaudit(cmd, 1)
        os.rename(os.path.join(self.store.prefix, 'backup.gpg-id'),
                  os.path.join(self.store.prefix, '.gpg-id'))

    def test_pass_audit_passwords_notpwned(self):
        """Testing: pass audit Password/notpwned."""
        cmd = ['Password/notpwned']
        self._passaudit(cmd)

    def test_pass_audit_passwords_pwned(self):
        """Testing: pass audit Password/pwned."""
        cmd = ['Password/pwned']
        self._passaudit(cmd)


if __name__ == '__main__':
    unittest.main()
