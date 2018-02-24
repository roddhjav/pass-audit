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
import setup
import shutil
import unittest


class TestPassStore(setup.TestPass):
    prefix = "pass-store"

    def test_environment_no_prefix(self):
        """Testing: no prefix & binary."""
        os.environ.pop('PASSWORD_STORE_DIR', None)
        os.environ.pop('PASSWORD_STORE_BIN', None)
        with self.assertRaises(self.passaudit.PasswordStoreError):
            self.passaudit.PasswordStore()
        os.environ['PASSWORD_STORE_DIR'] = self.prefix
        os.environ['PASSWORD_STORE_BIN'] = shutil.which("pass")

    def test_environment_variables(self):
        """Testing: environment variables."""
        self.assertEqual(self.store.env['PASSWORD_STORE_DIR'], os.environ['PASSWORD_STORE_DIR'])
        self.assertEqual(self.store.env['PASSWORD_STORE_BIN'], os.environ['PASSWORD_STORE_BIN'])
        self.assertEqual(self.store.env['GNUPGHOME'], os.environ['GNUPGHOME'])

    # def test_list(self):
    #     """Testing: pass list."""
    #     ref = ['Social/news.ycombinator.com', 'Social/mastodon.social',
    #            'Social/twitter.com', 'CornerCases/note', 'CornerCases/empty password',
    #            'CornerCases/space title', 'CornerCases/empty entry', 'Bank/aib',
    #            'Servers/ovh.com', 'Servers/ovh.com0', 'Emails/dpbx@klivak.xb',
    #            'Emails/dpbx@afoqwdr.tx', 'Emails/WS/dpbx@fner.ws', 'Emails/WS/dpbx@mnyfymt.ws']
    #     self.assertEqual(self.store.list(), ref)
    #
    # def test_list_root(self):
    #     """ Testing: pass list path/ """
    #     ref = ['Emails/dpbx@klivak.xb', 'Emails/dpbx@afoqwdr.tx',
    #            'Emails/WS/dpbx@fner.ws', 'Emails/WS/dpbx@mnyfymt.ws']
    #     self.assertEqual(self.store.list('Emails'), ref)
    #     ref = ['Emails/WS/dpbx@fner.ws', 'Emails/WS/dpbx@mnyfymt.ws']
    #     self.assertEqual(self.store.list('Emails/WS'), ref)

    def test_show(self):  # Test empty entry, empty pass...
        """ Testing: pass show password """
        path = "Social/mastodon.social"
        password = "D<INNeT?#?Bf4%`zA/4i!/'$T"
        self.assertEqual(self.store.show(path), password)


if __name__ == '__main__':
    unittest.main()
