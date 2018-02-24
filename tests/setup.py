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
import sys
import shutil
import unittest
import importlib


class TestPass(unittest.TestCase):
    tmp = "/tmp/pass-audit/python/"
    gpgid = "D4C78DB7920E1E27F5416B81CC9DB947CF90C77B"
    prefix = "audit-store"

    @classmethod
    def setUpClass(self):
        # Getting pass-audit module
        try:
            sys.path.append('../lib')
            self.passaudit = importlib.import_module('audit')
        except Exception as e:
            print("Unable to find audit.py: %s", e)
            exit(1)

        # GPG Config
        if 'GPG_AGENT_INFO' in os.environ:
            os.environ.pop('GPG_AGENT_INFO', None)
        os.environ['GNUPGHOME'] = os.path.join(os.getcwd(), 'gnupg')

        # Pass config
        os.environ['PASSWORD_STORE_BIN'] = shutil.which("pass")
        os.environ['PASSWORD_STORE_DIR'] = self.prefix
        self.store = self.passaudit.PasswordStore()
        os.makedirs(self.tmp, exist_ok=True)

    def _passinit(self):
        with open(os.path.join(self.store.prefix, '.gpg-id'), 'w') as file:
            file.write("%s\n" % self.gpgid)

    def _getdata(self, root):
        data = dict()
        for path in self.store.list(root):
            data[path] = self.store.show(path)
        return data
