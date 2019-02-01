#!/usr/bin/env python3
# pass audit - Password Store Extension (https://www.passwordstore.org/)
# Copyright (C) 2018-2019 Alexandre PUJOL <alexandre@pujol.io>.
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
import pass_audit


class TestBase(unittest.TestCase):
    tmp = "/tmp/pass-audit/python/"
    gpgids = ['D4C78DB7920E1E27F5416B81CC9DB947CF90C77B', '']
    prefix = "tests/audit-store"


class TestPass(TestBase):
    """Base test class for passwordstore related tests.
    This base test class provides the unittest with.
        1. A working gpg keyring
        2. A directory where it can create new password store
        3. A _passinit function
    """

    @classmethod
    def setUpClass(self):
        # GPG Settings
        if 'GPG_AGENT_INFO' in os.environ:
            os.environ.pop('GPG_AGENT_INFO')
        os.environ['GNUPGHOME'] = os.path.join(os.getcwd(), 'tests/gnupg')

        # Set PASSWORD_STORE_DIR & declare a passwordstore object
        os.environ['PASSWORD_STORE_DIR'] = self.prefix
        self.store = pass_audit.PasswordStore()
        os.makedirs(self.tmp, exist_ok=True)

    def _passinit(self):
        with open(os.path.join(self.store.prefix, '.gpg-id'), 'w') as file:
            file.write('\n'.join(self.gpgids))

    def _getdata(self, root):
        data = dict()
        for path in self.store.list(root):
            data[path] = self.store.show(path)
        return data
