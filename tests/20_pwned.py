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

import unittest
import setup


class TestPwnedAPI(setup.TestPass):

    def setUp(self):
        self.api = self.passaudit.PwnedAPI()

    def test_password_range(self):
        """Testing: https://api.haveibeenpwned.com/range API."""
        prefix = '21BD1'
        hash = '21BD12DC183F740EE76F27B78EB39C8AD972A757'
        hashes, counts = self.api.password_range(prefix)
        self.assertIn(hash, hashes)
        self.assertTrue(counts[hashes.index(hash)] == 47205)
        self.assertTrue(len(hashes) == len(counts))
        self.assertTrue(len(hashes) == 475)


if __name__ == '__main__':
    unittest.main()
