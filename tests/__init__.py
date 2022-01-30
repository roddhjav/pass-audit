#!/usr/bin/env python3
# pass audit - Password Store Extension (https://www.passwordstore.org/)
# Copyright (C) 2018-2022 Alexandre PUJOL <alexandre@pujol.io>.
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
"""pass-audit test suite common resources.
It provides:
  - tests.tmp Path to the test temporary directory.
  - tests.tests Root path for tests
  - tests.assets Root path of tests assets.
  - tests.prefix Path to the reference audit repository.
  - tests.Tests() Base test class.
  - tests.captured() Context manager to capture stdout.
  - tests.getdata() Get data from the reference repository.
  - tests.mock_request() Mock HIBP API response.
"""

import os
import sys
import shutil
import unittest
from io import StringIO
from contextlib import contextmanager

import pass_audit.__main__
from pass_audit.passwordstore import PasswordStore


tmp = "/tmp/tests/pass-audit/"  # nosec
tests = os.path.abspath('tests')
assets = os.path.join(tests, 'assets') + os.sep
prefix = assets + 'audit-store'


@contextmanager
def captured():
    """Context manager to capture stdout."""
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def getdata(root):
    """Get data from the reference repository."""
    data = {}
    store = PasswordStore(prefix)
    for path in store.list(root):
        data[path] = store.show(path)
    return data


def mock_request(*args, **kwargs):
    """Mock HIBP API response."""

    class MockResponse:
        def __init__(self):
            data = [
                "D5EE0CB1A41071812CCED2F1930E6E1A5D2:2",
                "2DC183F740EE76F27B78EB39C8AD972A757:52579",
                "CF164D7A51A1FD864B1BF9E1CE8A3EC171B:4",
                "D0B910E7A3028703C0B30039795E908CEB2:7",
                "AD6438836DBE526AA231ABDE2D0EEF74D42:3",
                "EBAB0A7CE978E0194608B572E4F9404AA21:3",
                "17727EAB0E800E62A776C76381DEFBC4145:120",
                "5370372AC65308F03F6ED75EC6068C8E1BE:1386",
                "1E4C9B93F3F0682250B6CF8331B7EE68FD8:3730471",
                "437FAA5A7FCE15D1DDCB9EAEAEA377667B8:123422",
                "944C22589AC652B0F47918D58CA0CDCCB63:411"
            ]

            self.text = "\r\n".join(data)

        def raise_for_status(self):
            pass

    return MockResponse()


class Test(unittest.TestCase):
    """Common resources for all tests.

    :param str prefix: Path to a password repository.
    :param list gpgids: Test GPGIDs.

    """
    prefix = ''
    gpgids = ['D4C78DB7920E1E27F5416B81CC9DB947CF90C77B', '']

    def __init__(self, methodName='runTest'):  # noqa
        super().__init__(methodName)

        # GPG keyring & pass settings
        os.environ.pop('GPG_AGENT_INFO', None)
        os.environ.pop('PASSWORD_STORE_SIGNING_KEY', None)
        os.environ['GNUPGHOME'] = os.path.join(os.getcwd(), assets + 'gnupg')

    def _tmpdir(self, path=''):
        """Create a temporary test directory named after the testname."""
        self.prefix = os.path.join(tmp, self._testMethodName)

        # Re-initialize the test directory
        if os.path.isdir(self.prefix):
            shutil.rmtree(self.prefix, ignore_errors=True)
        os.makedirs(self.prefix, exist_ok=True)

        if path != '':
            self.prefix = os.path.join(self.prefix, path)

    def main(self, cmd, code=None, msg=''):
        """Call to the main function."""
        sys.argv = cmd
        if code is None:
            pass_audit.__main__.main()
        elif msg == '':
            with self.assertRaises(SystemExit) as cm:
                pass_audit.__main__.main()
            self.assertEqual(cm.exception.code, code)
        else:
            with captured() as (out, err):
                with self.assertRaises(SystemExit) as cm:
                    pass_audit.__main__.main()
                if code == 0:
                    message = out.getvalue().strip()
                else:
                    message = err.getvalue().strip()
                self.assertIn(msg, message)
                self.assertEqual(cm.exception.code, code)

    def _init_pass(self):
        """Initialize a new password store repository."""
        with open(os.path.join(self.prefix, '.gpg-id'), 'w') as file:
            file.write('\n'.join(self.gpgids))
