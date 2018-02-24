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

import os
import sys
import glob
import hashlib
import requests
import argparse
from subprocess import Popen, PIPE


BASEAPIURL = "https://api.pwnedpasswords.com/"

GREEN = '\033[32m'
YELLOW = '\033[33m'
MAGENTA = '\033[35m'
BRED = '\033[1m\033[91m'
BGREEN = '\033[1m\033[92m'
BYELLOW = '\033[1m\033[93m'
BMAGENTA = '\033[1m\033[95m'
BOLD = '\033[1m'
END = '\033[0m'
VERBOSE = False
QUIET = False


def verbose(msg=''):
    if VERBOSE:
        print("%s  .  %s%s%s" % (BMAGENTA, END, MAGENTA, msg))


def message(msg=''):
    if not QUIET:
        print("%s  .  %s%s" % (BOLD, END, msg))


def success(msg=''):
    if not QUIET:
        print("%s (*) %s%s%s%s" % (BGREEN, END, GREEN, msg, END))


def warning(msg=''):
    if not QUIET:
        print("%s  w  %s%s%s%s" % (BYELLOW, END, YELLOW, msg, END))


def error(msg=''):
    print("%s [x] %s%sError: %s%s" % (BRED, END, BOLD, END, msg))


def die(msg=''):
    error(msg)
    exit(1)


class PasswordStoreError(Exception):
    """Error in the execution of password store."""


class PasswordStore():
    """Simple Password Store for python, only able to show password.
    Supports all the environment variables.
    """
    def __init__(self):
        self.env = dict(**os.environ)
        self._setenv('PASSWORD_STORE_DIR')
        self._setenv('PASSWORD_STORE_KEY')
        self._setenv('PASSWORD_STORE_GIT', 'GIT_DIR')
        self._setenv('PASSWORD_STORE_GPG_OPTS')
        self._setenv('PASSWORD_STORE_X_SELECTION', 'X_SELECTION')
        self._setenv('PASSWORD_STORE_CLIP_TIME', 'CLIP_TIME')
        self._setenv('PASSWORD_STORE_UMASK')
        self._setenv('PASSWORD_STORE_GENERATED_LENGHT', 'GENERATED_LENGTH')
        self._setenv('PASSWORD_STORE_CHARACTER_SET', 'CHARACTER_SET')
        self._setenv('PASSWORD_STORE_CHARACTER_SET_NO_SYMBOLS',
                     'CHARACTER_SET_NO_SYMBOLS')
        self._setenv('PASSWORD_STORE_ENABLE_EXTENSIONS')
        self._setenv('PASSWORD_STORE_EXTENSIONS_DIR', 'EXTENSIONS')
        self._setenv('PASSWORD_STORE_SIGNING_KEY')
        self._setenv('GNUPGHOME')
        self._setenv('PASSWORD_STORE_BIN')

        mandatory = ['PASSWORD_STORE_DIR', 'PASSWORD_STORE_BIN']
        if not all(x in self.env for x in mandatory):
            raise PasswordStoreError("pass prefix or binary unknown")
        self.prefix = self.env['PASSWORD_STORE_DIR']
        self.passbinary = self.env['PASSWORD_STORE_BIN']

    def _setenv(self, var, env=None):
        """Add var in the environment variables directory."""
        if env is None:
            env = var
        if env in os.environ:
            self.env[var] = os.environ[env]

    def _pass(self, arg=None, data=None):
        """Call to password store."""
        command = [self.passbinary]
        if arg is not None:
            command.extend(arg)

        process = Popen(command, universal_newlines=True, env=self.env,
                        stdin=PIPE, stdout=PIPE, stderr=PIPE)  # nosec
        (stdout, stderr) = process.communicate(data)
        res = process.wait()
        if res:
            raise PasswordStoreError("%s %s" % (stderr, stdout))
        return stdout

    def list(self, path=''):
        """ Return a list of paths in a store """
        paths = []
        prefix = os.path.join(self.prefix, path)
        for file in glob.glob(prefix + '*/**/*.gpg', recursive=True):
            if not file[0] == '.':
                file = os.path.splitext(file)[0]
                file = file[len(self.prefix)+1:]
                paths.append(file)
        return paths

    def show(self, path):
        """Decrypt path and read the password from the password file."""
        return self._pass(['show', path]).split('\n')[0]

    def exist(self):
        """Return True if the password store is initialized."""
        return os.path.isfile(os.path.join(self.prefix, '.gpg-id'))


class PwnedAPI():
    """Simple wrapper for https://haveibeenpwned.com API."""

    @staticmethod
    def password_range(prefix):
        url = BASEAPIURL + 'range/' + prefix
        res = requests.get(url, verify=True)
        res.raise_for_status()

        hashes = []
        counts = []
        for item in res.text.split('\r\n'):
            (partialhash, count) = item.split(':')
            hashes.append(prefix + partialhash)
            counts.append(int(count))
        return (hashes, counts)


class PassAudit():

    def __init__(self, data):
        self.data = data

    def password(self):
        """K-anonimity password breach detection on haveibeenpwned.com."""
        # Generate the list of hashes and prefixes to query.
        data = []
        prefixes = []
        for path, password in self.data.items():
            hash = hashlib.sha1(password.encode("utf8")).hexdigest().upper()
            prefix = hash[0:5]
            data.append((path, password, hash, prefix))
            if prefix not in prefixes:
                prefixes.append(prefix)

        # Query the server and collect the buckets
        buckets = dict()
        for prefix in prefixes:
            buckets[prefix] = PwnedAPI.password_range(prefix)

        # Compare the data and return the breached passwords.
        breached = []
        for path, password, hash, prefix in data:
            if hash in buckets[prefix][0]:
                index = buckets[prefix][0].index(hash)
                count = buckets[prefix][1][index]
                breached.append((path, password, count))
        return breached


def main(argv):
    # Geting arguments for 'pass import'
    parser = argparse.ArgumentParser(prog='pass audit', description="""
  A pass extension for auditing your password repository. It supports safe
  breached password detection from haveibeenpwned.com using K-anonymity method.""",
    usage="%(prog)s [-h] [-V] paths",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="More information may be found in the pass-audit(1) man page.")

    parser.add_argument('paths', type=str, nargs='?',
                        help="""Path to audit in the password store.""")
    parser.add_argument('-q', '--quiet', action='store_true', help='Be quiet.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Be verbose.')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 1.0',
                        help='Show the program version and exit.')

    arg = parser.parse_args(argv)

    # Manage verbose & quiet messages
    if arg.quiet:
        arg.verbose = False
    global VERBOSE
    global QUIET
    VERBOSE = arg.verbose
    QUIET = arg.quiet

    # Sanity checks
    if arg.paths is None:
        die("pass-names not present. See 'pass audit -h'")
    store = PasswordStore()
    if not store.exist():
        die("no password store to audit.")

    # Read data from the password store.
    data = dict()
    for path in store.list(arg.paths):
        try:
            data[path] = store.show(path)
        except PasswordStoreError as e:
            warning("Imposible to read %s from the password store: %s"
                    % (path, e))

    # Start the audit of the password store
    audit = PassAudit(data)
    breached = audit.password()
    for path, password, count in breached:
        warning("Password breached: %s from %s has been breached %s time(s)."
                % (password, path, count))

    # Report!
    if len(breached) == 0:
        success("None of the %s passwords tested are breached." % len(data))
        message("But it does not means they are strong.")
    else:
        error("%d passwords tested and %d breached passwords found."
              % (len(data), len(breached)))
        message("You should update them with 'pass-update'.")


if __name__ == "__main__":
    sys.argv.pop(0)
    main(sys.argv)
