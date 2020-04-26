# -*- encoding: utf-8 -*-
# pass-audit - test suite
# Copyright (C) 2018-2020 Alexandre PUJOL <alexandre@pujol.io>.
#

import pass_audit.msg
import tests


class TestMsg(tests.Test):
    """Test the Msg class."""

    def setUp(self):
        self.msg = pass_audit.msg.Msg()

    def test_debug(self):
        """Testing: debug message."""
        msg = pass_audit.msg.Msg(3)
        with tests.captured() as (out, err):
            msg.debug('debug message')
            message = out.getvalue().strip()
        self.assertEqual(err.getvalue().strip(), '')
        self.assertEqual(
            message, '\x1b[1m\x1b[95m  .  \x1b[0m\x1b[35mdebug message\x1b[0m')

    def test_verbose_simple(self):
        """Testing: message verbose simple."""
        with tests.captured() as (out, err):
            self.msg.verbose('verbose message')
            message = out.getvalue().strip()
        self.assertEqual(err.getvalue().strip(), '')
        self.assertEqual(message, '')

    def test_verbose(self):
        """Testing: message verbose."""
        msg = pass_audit.msg.Msg(1)
        with tests.captured() as (out, err):
            msg.verbose('verbose message')
            message = out.getvalue().strip()
        self.assertEqual(err.getvalue().strip(), '')
        self.assertEqual(
            message,
            '\x1b[1m\x1b[95m  .  \x1b[0m\x1b[35mverbose message\x1b[0m')

    def test_message(self):
        """Testing: classic message."""
        with tests.captured() as (out, err):
            self.msg.message('classic message')
            message = out.getvalue().strip()
            print(message)
        self.assertEqual(err.getvalue().strip(), '')
        self.assertEqual(message, '\x1b[1m  .  \x1b[0mclassic message')

        msg = pass_audit.msg.Msg(1, True)
        with tests.captured() as (out, err):
            msg.message('classic message')
            message = out.getvalue().strip()
            print(message)
        self.assertEqual(err.getvalue().strip(), '')
        self.assertEqual(message, '')

    def test_success(self):
        """Testing: success message."""
        with tests.captured() as (out, err):
            self.msg.success('success message')
            message = out.getvalue().strip()
        self.assertEqual(err.getvalue().strip(), '')
        self.assertEqual(
            message,
            '\x1b[1m\x1b[92m (*) \x1b[0m\x1b[32msuccess message\x1b[0m')

    def test_warning(self):
        """Testing: warning message."""
        with tests.captured() as (out, err):
            self.msg.warning('warning message')
            message = out.getvalue().strip()
        self.assertEqual(err.getvalue().strip(), '')
        self.assertEqual(
            message,
            '\x1b[1m\x1b[93m  w  \x1b[0m\x1b[33mwarning message\x1b[0m')

    def test_error(self):
        """Testing: error message."""
        with tests.captured() as (out, err):
            self.msg.error('error message')
            message = err.getvalue().strip()
        self.assertEqual(out.getvalue().strip(), '')
        self.assertEqual(
            message,
            '\x1b[1m\x1b[91m [x] \x1b[0m\x1b[1mError: \x1b[0merror message')

    def test_die(self):
        """Testing: die message."""
        with tests.captured() as (out, err):
            with self.assertRaises(SystemExit) as cm:
                self.msg.die('critical error')
            message = err.getvalue().strip()
            self.assertEqual(cm.exception.code, 1)
        self.assertEqual(out.getvalue().strip(), '')
        self.assertEqual(
            message,
            '\x1b[1m\x1b[91m [x] \x1b[0m\x1b[1mError: \x1b[0mcritical error')
