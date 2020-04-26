# -*- encoding: utf-8 -*-
# pass-audit - test suite
# Copyright (C) 2018-2020 Alexandre PUJOL <alexandre@pujol.io>.
#

from unittest import mock

import pass_audit.audit
import tests


class TestPwnedAPI(tests.Test):
    """Test the PwnedAPI class."""

    def setUp(self):
        self.api = pass_audit.audit.PwnedAPI()

    @mock.patch('requests.get', tests.mock_request)
    def test_password_range(self):
        """Testing: https://api.haveibeenpwned.com/range API."""
        prefix = '21BD1'
        phash = '21BD12DC183F740EE76F27B78EB39C8AD972A757'
        hashes, counts = self.api.password_range(prefix)
        self.assertIn(phash, hashes)
        self.assertTrue(counts[hashes.index(phash)] == 52579)
        self.assertTrue(len(hashes) == len(counts))
        self.assertTrue(len(hashes) == 11)
