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

import pass_audit
from tests.commons import TestPass


class TestPassAudit(TestPass):
    passwords_nb = 7
    msg = pass_audit.Msg()

    def test_password_notpwned(self):
        """Testing: pass audit for password not breached with K-anonymity."""
        data = self._getdata("Password/notpwned")
        audit = pass_audit.PassAudit(data, self.msg)
        breached = audit.password()
        self.assertTrue(len(breached) == 0)

    def test_password_pwned(self):
        """Testing: pass audit for password breached with K-anonymity."""
        ref_counts = [52579, 3, 120, 1386, 3730471, 123422, 411]
        data = self._getdata("Password/pwned")
        audit = pass_audit.PassAudit(data, self.msg)
        breached = audit.password()
        self.assertTrue(len(breached) == self.passwords_nb)
        for path, password, count in breached:
            self.assertIn(path, data)
            self.assertTrue(data[path]['password'] == password)
            ref_index = int(path[-1:]) - 1
            self.assertTrue(ref_counts[ref_index] == count)
