# -*- encoding: utf-8 -*-
# pass audit - Password Store Extension (https://www.passwordstore.org/)
# Copyright (C) 2018-2020 Alexandre PUJOL <alexandre@pujol.io>.
#

import sys


class Msg():
    """General class to manage output messages."""
    # Normal colors
    green = '\033[32m'
    yellow = '\033[33m'
    magenta = '\033[35m'
    end = '\033[0m'

    # Bold colors
    RED = '\033[1m\033[91m'
    GREEN = '\033[1m\033[92m'
    YELLOW = '\033[1m\033[93m'
    MAGENTA = '\033[1m\033[95m'
    BOLD = '\033[1m'

    def __init__(self, verbose=0, quiet=False):
        self.verb = verbose
        self.quiet = quiet
        if self.quiet:
            self.verb = 0

    def verbose(self, msg=''):
        """Verbose method."""
        if self.verb >= 1:
            out = "%s  .  %s%s%s%s" % (self.MAGENTA, self.end, self.magenta,
                                       msg, self.end)
            print(out, file=sys.stdout)

    def debug(self, msg=''):
        """Debug method."""
        if self.verb >= 3:
            self.verbose(msg)

    def message(self, msg=''):
        """Message method."""
        if not self.quiet:
            out = "%s  .  %s%s" % (self.BOLD, self.end, msg)
            print(out, file=sys.stdout)

    def success(self, msg=''):
        """Success method."""
        if not self.quiet:
            out = "%s (*) %s%s%s%s" % (self.GREEN, self.end, self.green, msg,
                                       self.end)
            print(out, file=sys.stdout)

    def warning(self, msg=''):
        """Warning method."""
        if not self.quiet:
            out = "%s  w  %s%s%s%s" % (self.YELLOW, self.end, self.yellow, msg,
                                       self.end)
            print(out, file=sys.stdout)

    def error(self, msg=''):
        """Error method."""
        err = "%s [x] %s%sError: %s%s" % (self.RED, self.end, self.BOLD,
                                          self.end, msg)
        print(err, file=sys.stderr)

    def die(self, msg=''):
        """Show an error and exit the program."""
        self.error(msg)
        sys.exit(1)
