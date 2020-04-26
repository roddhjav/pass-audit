# -*- encoding: utf-8 -*-
# pass-audit - test suite
# Copyright (C) 2018-2020 Alexandre PUJOL <alexandre@pujol.io>.
#

from unittest import mock

import pass_audit.audit
import pass_audit.msg
import tests


class TestPassAudit(tests.Test):
    """Test the PassAudit class."""
    passwords_nb = 7

    @classmethod
    def setUpClass(cls):
        cls.msg = pass_audit.msg.Msg()

    @mock.patch('requests.get', tests.mock_request)
    def test_password_notpwned(self):
        """Testing: pass audit for password not breached with K-anonymity."""
        data = tests.getdata('Password/notpwned')
        audit = pass_audit.audit.PassAudit(data, self.msg)
        breached = audit.password()
        self.assertTrue(len(breached) == 0)

    @mock.patch('requests.get', tests.mock_request)
    def test_password_pwned(self):
        """Testing: pass audit for password breached with K-anonymity."""
        ref_counts = [52579, 3, 120, 1386, 3730471, 123422, 411]
        data = tests.getdata('Password/pwned')
        audit = pass_audit.audit.PassAudit(data, self.msg)
        breached = audit.password()
        self.assertTrue(len(breached) == self.passwords_nb)
        for path, password, count in breached:
            self.assertIn(path, data)
            self.assertTrue(data[path]['password'] == password)
            ref_index = int(path[-1:]) - 1
            self.assertTrue(ref_counts[ref_index] == count)
