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

from .. import pass_audit
from tests.commons import TestPass


class TestPwnedAPI(TestPass):

    def setUp(self):
        self.api = pass_audit.PwnedAPI()

    def test_password_range(self):
        """Testing: https://api.haveibeenpwned.com/range API."""
        prefix = '21BD1'
        phash = '21BD12DC183F740EE76F27B78EB39C8AD972A757'
        hashes, counts = self.api.password_range(prefix)
        self.assertIn(phash, hashes)
        self.assertTrue(counts[hashes.index(phash)] == 52579)
        self.assertTrue(len(hashes) == len(counts))
        self.assertTrue(len(hashes) == 528)
