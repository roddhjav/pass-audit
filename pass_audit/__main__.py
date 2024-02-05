# -*- coding: utf-8 -*
# pass audit - Password Store Extension (https://www.passwordstore.org/)
# Copyright (C) 2018-2022 Alexandre PUJOL <alexandre@pujol.io>.
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
 breached password detection from haveibeenpwned.com using K-anonymity method,
 duplicated passwords, and password strength estimation using zxcvbn."""
        epilog = "More information may be found in the pass-audit(1) man page."

        super().__init__(prog='pass audit',
                         description=description,
                         formatter_class=RawDescriptionHelpFormatter,
                         epilog=epilog)
        self.add_arguments()
        self.passwordstore = bool(
            os.environ.get('_PASSWORD_STORE_EXTENSION', '') == 'audit')

    def add_arguments(self):
        """Set arguments."""
        self.add_argument('paths', type=str, nargs='?', metavar='pass-names',
                          default='', help="""Path(s) to audit in the password
                          store, If empty audit the full store.""")

        self.add_argument('-V', '--version', action='version',
                          version='%(prog)s ' + __version__,
                          help='Show the program version and exit.')
        self.add_argument('-n', '--name', type=str, default="*",
                          help="""Check only passwords with this filename""")
        group = self.add_mutually_exclusive_group()
        group.add_argument('-v', '--verbose', action='count', default=0,
                           help='Set verbosity level, '
                                'can be used more than once.')
        group.add_argument('-q', '--quiet', action='store_true',
                           help='Be quiet.')


def setup():
    """Read program arguments & sanity checks."""
    parser = ArgParser()
    arg = parser.parse_args(sys.argv)
    msg = Msg(arg.verbose, arg.quiet)

    if not parser.passwordstore:
        msg.die("not running inside password-store.")

    if arg.paths == '':
        msg.message("Auditing whole store - this may take some time")

    store = PasswordStore()
    if not store.exist():
        msg.die("no password store to audit.")
    if not store.isvalid():
        msg.die('invalid user ID, password access aborted.')

    paths_raw = store.list(arg.paths, arg.name)
    paths = []

    if not paths_raw:
        msg.die(f"{arg.paths} is not in the password store.")

    with open(os.path.join(store.prefix, ".pass-audit-ignore"), "r") as ignore:
        ignore_paths = ignore.read()

    for path in paths_raw:
        add_path = False
        for ignore_path in ignore_paths.split("\n"):
            if ignore_path == "":
                continue

            if ignore_path.startswith("#"):
                continue

            if not path.startswith(ignore_path):
                add_path = True
            else:
                add_path = False
                break

        if add_path:
            paths.append(path)

    return msg, store, paths


def pass_read(msg, store, paths):
    """Read data from the password store."""
    msg.verbose("Reading the password store")
    data = {}
    for path in paths:
        try:
            msg.verbose(f"Reading {path}")
            data[path] = store.show(path)
        except PasswordStoreError as error:
            msg.warning(
                f"Impossible to read {path} from the password store: {error}")
    return data


def zxcvbn_parse(details):
    """Nicely print the results from zxcvbn."""
    sequence = ''
    for seq in details.get('sequence', []):
        sequence += f"{seq['token']}({seq['pattern']}) "
    res = f"Score {details['score']} ({details['guesses']} guesses). "
    return res + f"This estimate is based on the sequence {sequence}"


def main():
    """pass-audit main function."""
    msg, store, paths = setup()

    data = pass_read(msg, store, paths)
    audit = PassAudit(data, msg.verb)

    msg.verbose("Checking for breached passwords")
    breached = audit.password()
    for path, payload, count in breached:
        msg.warning(f"Password breached: {payload} from {path} has"
                    f" been breached {count} time(s).")

    msg.verbose("Checking for weak passwords")
    try:
        weak = audit.zxcvbn()
    except ImportError as error:
        weak = []
        msg.warning(f"python3-{error.name} not present, skipping check")
    for path, payload, details in weak:
        msg.warning(f"Weak password detected: {payload} from {path}"
                    f" might be weak. {zxcvbn_parse(details)}")

    msg.verbose("Checking for duplicated passwords")
    duplicated = audit.duplicates()
    for paths in duplicated:
        msg.warning(f"Duplicated passwords detected in {', '.join(paths)}")

    if not breached and not weak and not duplicated:
        msg.success(f"None of the {len(data)} passwords tested are "
                    "breached, duplicated or weak.")
    else:
        msg.error(f"{len(data)} passwords tested and {len(breached)} breached,"
                  f" {len(weak)} weak passwords found,"
                  f" {len(duplicated)} duplicated passwords found.")
        msg.message("You should update them with 'pass update'.")


if __name__ == "__main__":
    sys.argv.pop(0)
    main()
