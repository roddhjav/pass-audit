# -*- encoding: utf-8 -*-
# pass-audit - test suite
# Copyright (C) 2018-2022 Alexandre PUJOL <alexandre@pujol.io>.
#

from unittest import mock

import pass_audit.audit
import pass_audit.msg
import tests


class TestPassAudit(tests.Test):
    """Test the PassAudit class."""
    passwords_nb = 7
    passwords_unignored = 4

    @mock.patch('requests.get', tests.mock_request)
    def test_password_notpwned(self):
        """Testing: pass audit for password not breached with K-anonymity."""
        data = tests.getdata('Password/notpwned')
        audit = pass_audit.audit.PassAudit(data, True)
        breached = audit.password()
        self.assertTrue(len(breached) == 0)

    @mock.patch('requests.get', tests.mock_request)
    def test_password_pwned(self):
        """Testing: pass audit for password breached with K-anonymity."""
        ref_counts = [52579, 3, 120, 1386, 3730471, 123422, 411]
        data = tests.getdata('Password/pwned')
        audit = pass_audit.audit.PassAudit(data, True)
        breached = audit.password()
        self.assertTrue(len(breached) == self.passwords_nb)
        for path, password, count in breached:
            self.assertIn(path, data)
            self.assertTrue(data[path]['password'] == password)
            ref_index = int(path[-1:]) - 1
            self.assertTrue(ref_counts[ref_index] == count)

    def test_password_ignore(self):
        """Testing: if .pass-audit-ignore works"""
        data = tests.getdata('Password/ignore')
        audit = pass_audit.audit.PassAudit(data, True)
        passwords = audit.password()

        self.assertTrue(len(passwords) == self.passwords_unignored)

    def test_zxcvbn_weak(self):
        """Testing: pass audit for weak password with zxcvbn."""
        data = tests.getdata('Password/pwned/1')
        audit = pass_audit.audit.PassAudit(data, True)
        weak = audit.zxcvbn()
        self.assertTrue(len(weak) == 1)
        self.assertTrue(weak[0][2]['score'] == 0)

    def test_zxcvbn_strong(self):
        """Testing: pass audit for strong password with zxcvbn."""
        data = tests.getdata('Password/good')
        audit = pass_audit.audit.PassAudit(data, True)
        weak = audit.zxcvbn()
        self.assertTrue(len(weak) == 0)

    def test_duplicates_yes(self):
        """Testing: pass audit for duplicated passwords."""
        data = tests.getdata('Password/notpwned/1')
        data['Password/notpwned/copy'] = data['Password/notpwned/1']
        audit = pass_audit.audit.PassAudit(data, True)
        duplicated = audit.duplicates()
        self.assertTrue(len(duplicated) == 1)

    def test_duplicates_no(self):
        """Testing: pass audit for not duplicated passwords."""
        data = tests.getdata('Password/notpwned/')
        audit = pass_audit.audit.PassAudit(data, True)
        duplicated = audit.duplicates()
        self.assertTrue(len(duplicated) == 0)

    def test_empty(self):
        """Testing: pass audit for empty password."""
        data = {'empty': {'password': ''}}
        audit = pass_audit.audit.PassAudit(data, True)
        weak = audit.zxcvbn()
        breached = audit.password()
        duplicated = audit.duplicates()
        self.assertTrue(len(weak) == 0)
        self.assertTrue(len(breached) == 0)
        self.assertTrue(len(duplicated) == 0)
