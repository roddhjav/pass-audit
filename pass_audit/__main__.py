#!/usr/bin/env python3
# -*- coding: utf-8 -*
# pass audit - Password Store Extension (https://www.passwordstore.org/)
# Copyright (C) 2018-2020 Alexandre PUJOL <alexandre@pujol.io>.
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

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from pass_audit import __version__
from pass_audit.audit import PassAudit
from pass_audit.msg import Msg
from pass_audit.passwordstore import PasswordStore, PasswordStoreError


class ArgParser(ArgumentParser):
    """Manages argument parsing and adds some defaults."""

    def __init__(self):
        description = """
 A pass extension for auditing your password repository. It supports safe
 breached password detection from haveibeenpwned.com using K-anonymity method
 and password strength estimaton using zxcvbn."""
        epilog = "More information may be found in the pass-audit(1) man page."

        super(ArgParser,
              self).__init__(prog='pass import',
                             description=description,
                             formatter_class=RawDescriptionHelpFormatter,
                             epilog=epilog)
        self.add_arguments()

    def add_arguments(self):
        """Set arguments."""
        self.add_argument('paths', type=str, nargs='?', metavar='pass-names',
                          default='', help="""Path(s) to audit in the password
                          store, If empty audit the full store.""")

        self.add_argument('-V', '--version', action='version',
                          version='%(prog)s ' + __version__,
                          help='Show the program version and exit.')
        group = self.add_mutually_exclusive_group()
        group.add_argument('-v', '--verbose', action='count', default=0,
                           help='Set verbosity level, '
                                'can be used more than once.')
        group.add_argument('-q', '--quiet', action='store_true',
                           help='Be quiet.')


def setup():
    """Read progam arguments & sanity checks."""
    parser = ArgParser()
    arg = parser.parse_args(sys.argv)
    msg = Msg(arg.verbose, arg.quiet)

    if arg.paths == '':
        msg.message("Auditing whole store - this may take some time")

    store = PasswordStore()
    if not store.exist():
        msg.die("no password store to audit.")
    if not store.isvalid():
        msg.die('invalid user ID, password access aborted.')

    paths = store.list(arg.paths)
    if not paths:
        msg.die("%s is not in the password store." % arg.paths)

    return msg, store, paths


def pass_read(msg, store, paths):
    """Read data from the password store."""
    msg.verbose("Reading the password store")
    data = dict()
    for path in paths:
        try:
            msg.verbose("Reading %s" % path)
            data[path] = store.show(path)
        except PasswordStoreError as error:
            msg.warning("Imposible to read %s from the password store: %s"
                        % (path, error))
    return data


def pass_audit(msg, data):
    """Audit of the password store."""
    audit = PassAudit(data, msg)

    msg.verbose("Checking for breached passwords")
    breached = audit.password()

    msg.verbose("Checking for weak passwords")
    weak = audit.zxcvbn()

    return breached, weak


def zxcvbn_parse(details):
    """Nicely print the results from zxcvbn."""
    sequence = ''
    for seq in details.get('sequence', []):
        sequence += "%s(%s) " % (seq['token'], seq['pattern'])
    res = "Score %s (%s guesses). " % (details['score'], details['guesses'])
    return res + "This estimate is based on the sequence %s" % sequence


def report(msg, data, breached, weak):
    """Print final report."""
    for path, payload, count in breached:
        msg.warning("Password breached: %s from %s has"
                    " been breached %s time(s)." % (payload, path, count))
    for path, payload, details in weak:
        msg.warning("Weak password detected: %s from %s might be weak. %s"
                    % (payload, path, zxcvbn_parse(details)))

    if not breached and not weak:
        msg.success("None of the %s passwords tested are breached or weak."
                    % len(data))
    else:
        msg.error("%d passwords tested and %d breached, %d weak "
                  "passwords found." % (len(data), len(breached), len(weak)))
        msg.message("You should update them with 'pass update'.")


def main():
    """pass-audit main function."""
    msg, store, paths = setup()

    data = pass_read(msg, store, paths)
    breached, weak = pass_audit(msg, data)

    report(msg, data, breached, weak)


if __name__ == "__main__":
    sys.argv.pop(0)
    main()
