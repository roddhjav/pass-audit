# -*- encoding: utf-8 -*-
# pass-audit - test suite
# Copyright (C) 2018-2020 Alexandre PUJOL <alexandre@pujol.io>.
#

import os
from unittest import mock

from pass_audit.passwordstore import PasswordStore
import tests


class TestMain(tests.Test):
    """Test common pass-audit main."""

    @classmethod
    def setUpClass(cls):
        cls.prefix = tests.prefix
        cls.store = PasswordStore(tests.prefix)
        os.environ['PASSWORD_STORE_DIR'] = tests.prefix
        os.environ['_PASSWORD_STORE_EXTENSION'] = 'audit'  # nosec

    def test_main_help(self):
        """Testing: pass audit --help."""
        cmd = ['--help']
        print(self.store.prefix)
        self.main(cmd, 0)

    def test_main_version(self):
        """Testing: pass audit --version."""
        cmd = ['--version']
        self.main(cmd, 0)

    def test_main_not_an_option(self):
        """Testing: pass audit --not-an-option."""
        cmd = ['--not-an-option', '-q']
        self.main(cmd, 2)

    def test_main_store_do_not_exist(self):
        """Testing: store not initialized."""
        cmd = ['Password/', '-v']
        os.rename(os.path.join(self.store.prefix, '.gpg-id'),
                  os.path.join(self.store.prefix, 'backup.gpg-id'))
        self.main(cmd, 1, 'no password store to audit.')
        os.rename(os.path.join(self.store.prefix, 'backup.gpg-id'),
                  os.path.join(self.store.prefix, '.gpg-id'))

    def test_main_invalid_keys(self):
        """Testing: invalid user ID."""
        os.rename(os.path.join(self.store.prefix, '.gpg-id'),
                  os.path.join(self.store.prefix, 'backup.gpg-id'))
        self.gpgids = ['']
        self._init_pass()
        self.main(
            [''], 1,
            'invalid user ID, password access aborted.')

        os.rename(os.path.join(self.store.prefix, 'backup.gpg-id'),
                  os.path.join(self.store.prefix, '.gpg-id'))

    def test_main_not_inside_pass(self):
        """Testing: python3 -m audit."""
        os.environ.pop('_PASSWORD_STORE_EXTENSION')
        self.main([''], 1, 'not running inside password-store.')
        os.environ['_PASSWORD_STORE_EXTENSION'] = 'audit'  # nosec

    def test_main_not_a_file(self):
        """Testing: pass audit not_a_file."""
        cmd = ['not_a_file']
        self.main(cmd, 1, 'not_a_file is not in the password store.')

    @mock.patch('requests.get', tests.mock_request)
    def test_main_passwords_notpwned(self):
        """Testing: pass audit Password/notpwned."""
        cmd = ['Password/notpwned']
        self.main(cmd)

    @mock.patch('requests.get', tests.mock_request)
    def test_main_passwords_pwned(self):
        """Testing: pass audit Password/pwned."""
        cmd = ['Password/pwned']
        self.main(cmd)

    @mock.patch('requests.get', tests.mock_request)
    def test_main_passwords_good(self):
        """Testing: pass audit Password/good."""
        cmd = ['Password/good']
        self.main(cmd)

    @mock.patch('requests.get', tests.mock_request)
    def test_main_passwords_all(self):
        """Testing: pass audit ."""
        cmd = ['']
        self.main(cmd)
