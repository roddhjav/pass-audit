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
    tmp = "/tmp/pass-audit/python/"  # nosec
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
    def setUpClass(cls):
        # GPG Settings
        if 'GPG_AGENT_INFO' in os.environ:
            os.environ.pop('GPG_AGENT_INFO')
        os.environ['GNUPGHOME'] = os.path.join(os.getcwd(), 'tests/gnupg')

        # Set PASSWORD_STORE_DIR & declare a passwordstore object
        os.environ['PASSWORD_STORE_DIR'] = cls.prefix
        cls.store = pass_audit.PasswordStore()
        os.makedirs(cls.tmp, exist_ok=True)

    def _passinit(self):
        with open(os.path.join(self.store.prefix, '.gpg-id'), 'w') as file:
            file.write('\n'.join(self.gpgids))

    def _getdata(self, root):
        data = dict()
        for path in self.store.list(root):
            data[path] = self.store.show(path)
        return data


def mock_request(*args, **kwargs):
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
