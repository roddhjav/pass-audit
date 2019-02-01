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
import shutil

from .. import pass_audit
from tests.commons import TestPass


class TestPassStoreCommon(TestPass):

    def setUp(self):
        # The test name is the test method name after 'test_'
        testname = self.id().split('.').pop()[len('test_'):]

        # Set PASSWORD_STORE_DIR & declare a passwordstore object
        prefix = os.path.join(self.tmp, testname)
        os.environ['PASSWORD_STORE_DIR'] = prefix
        self.store = pass_audit.PasswordStore()

        # Re-initialize the test directory
        if os.path.isdir(prefix):
            shutil.rmtree(prefix, ignore_errors=True)
        os.makedirs(prefix, exist_ok=True)

    def test_environment_no_prefix(self):
        """Testing: no prefix."""
        os.environ.pop('PASSWORD_STORE_DIR', None)
        with self.assertRaises(pass_audit.PasswordStoreError):
            pass_audit.PasswordStore()

    def test_environment_variables(self):
        """Testing: environment variables."""
        self.assertEqual(self.store.env['PASSWORD_STORE_DIR'], os.environ['PASSWORD_STORE_DIR'])
        self.assertEqual(self.store.env['GNUPGHOME'], os.environ['GNUPGHOME'])

    def test_exist(self):
        """Testing: store not initialized."""
        self.assertFalse(self.store.exist())
        with self.assertRaises(pass_audit.PasswordStoreError):
            self.store._pass(['insert', '--multiline', 'Test/test'], 'dummy')
        self._passinit()
        self.assertTrue(self.store.exist())

    def test_valid_recipients(self):
        """Testing: valid recipients."""
        self.gpgids = ['D4C78DB7920E1E27F5416B81CC9DB947CF90C77B',
                       '70BD448330ACF0653645B8F2B4DDBFF0D774A374',
                       '62EBE74BE834C2EC71E6414595C4B715EB7D54A8', '']
        self._passinit()
        self.assertTrue(self.store.is_valid_recipients())

    def test_invalid_recipients(self):
        """Testing: invalid recipients."""
        self.gpgids = ['D4C78DB7920E1E27F5416B81CC9DB947CF90C77B',
                       'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
                       '62EBE74BE834C2EC71E6414595C4B715EB7D54A8', '']
        self._passinit()
        self.assertFalse(self.store.is_valid_recipients())

    def test_empty_recipients(self):
        """Testing: empty recipients."""
        self.gpgids = ['']
        self._passinit()
        self.assertFalse(self.store.is_valid_recipients())


class TestPassStoreList(TestPass):
    prefix = "tests/pass-store"

    def test_list_path(self):
        """Testing: pass list exact path."""
        path = 'Social/mastodon.social'
        ref = ['Social/mastodon.social']
        self.assertEqual(self.store.list(path), ref)

    def test_list(self):
        """Testing: pass list."""
        ref = ['Bank/aib', 'CornerCases/empty entry',
               'CornerCases/empty password', 'CornerCases/note',
               'CornerCases/space title', 'Emails/WS/dpbx@fner.ws',
               'Emails/WS/dpbx@mnyfymt.ws', 'Emails/dpbx@afoqwdr.tx',
               'Emails/dpbx@klivak.xb', 'Servers/ovh.com', 'Servers/ovh.com0',
               'Social/mastodon.social', 'Social/news.ycombinator.com',
               'Social/twitter.com']
        self.assertEqual(self.store.list(), ref)

    def test_list_root(self):
        """ Testing: pass list path/ """
        ref = ['Emails/WS/dpbx@fner.ws', 'Emails/WS/dpbx@mnyfymt.ws',
               'Emails/dpbx@afoqwdr.tx', 'Emails/dpbx@klivak.xb']
        self.assertEqual(self.store.list('Emails'), ref)
        ref = ['Emails/WS/dpbx@fner.ws', 'Emails/WS/dpbx@mnyfymt.ws']
        self.assertEqual(self.store.list('Emails/WS'), ref)

    def test_show(self):
        """Testing: pass show password."""
        path = "Social/mastodon.social"
        password = "D<INNeT?#?Bf4%`zA/4i!/'$T"
        self.assertEqual(self.store.show(path).split('\n')[0], password)
