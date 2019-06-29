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

import os
import sys
import shutil
import hashlib
import argparse
from pathlib import Path
from subprocess import Popen, PIPE  # nosec

__version__ = '1.0.1'


class PasswordStoreError(Exception):
    """Error in the execution of password store."""


class Msg():
    """General class to manage output messages."""
    green = '\033[32m'
    yellow = '\033[33m'
    magenta = '\033[35m'
    Bred = '\033[1m\033[91m'
    Bgreen = '\033[1m\033[92m'
    Byellow = '\033[1m\033[93m'
    Bmagenta = '\033[1m\033[95m'
    Bold = '\033[1m'
    end = '\033[0m'

    def __init__(self, verbose=False, quiet=False):
        self.verb = verbose
        self.quiet = quiet
        if self.quiet:
            self.verb = False

    def verbose(self, msg=''):
        """Verbose method."""
        if self.verb:
            print("%s  .  %s%s%s" % (self.Bmagenta, self.magenta, msg,
                                     self.end))

    def message(self, msg=''):
        """Message method."""
        if not self.quiet:
            print("%s  .  %s%s" % (self.Bold, self.end, msg))

    def success(self, msg=''):
        """Success method."""
        if not self.quiet:
            print("%s (*) %s%s%s%s" % (self.Bgreen, self.end,
                                       self.green, msg, self.end))

    def warning(self, msg=''):
        """Warning method."""
        if not self.quiet:
            print("%s  w  %s%s%s%s" % (self.Byellow, self.end,
                                       self.yellow, msg, self.end))

    def error(self, msg=''):
        """Error method."""
        print("%s [x] %s%sError: %s%s" % (self.Bred, self.end,
                                          self.Bold, self.end, msg))

    def die(self, msg=''):
        """Show an error and exit the program."""
        self.error(msg)
        exit(1)


try:
    import requests
    from zxcvbn import zxcvbn
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    err = Msg()  # pylint: disable=invalid-name
    err.die("Some modules are not present, you can install them with:\n"
            "  'sudo apt-get install python3-requests python3-zxcvbn', or\n"
            "  'pip3 install requests zxcvbn'")


def zxcvbn_parse(details):
    """Nicely print the results from zxcvbn."""
    sequence = ''
    for seq in details.get('sequence', []):
        sequence += "%s(%s) " % (seq['token'], seq['pattern'])
    res = "Score %s (%s guesses). " % (details['score'], details['guesses'])
    return res + "This estimate is based on the sequence %s" % sequence


class PasswordStore():
    """Simple Password Store wrapper for python.

    Based on the PasswordStore class from pass-import.
    See https://github.com/roddhjav/pass-import for more information.

    """

    def __init__(self, prefix=None):
        self._passbinary = shutil.which('pass')
        self._gpgbinary = shutil.which('gpg2') or shutil.which('gpg')
        self.env = dict(**os.environ)
        self._setenv('PASSWORD_STORE_DIR')
        self._setenv('PASSWORD_STORE_KEY')
        self._setenv('PASSWORD_STORE_GIT', 'GIT_DIR')
        self._setenv('PASSWORD_STORE_GPG_OPTS')
        self._setenv('PASSWORD_STORE_X_SELECTION', 'X_SELECTION')
        self._setenv('PASSWORD_STORE_CLIP_TIME', 'CLIP_TIME')
        self._setenv('PASSWORD_STORE_UMASK')
        self._setenv('PASSWORD_STORE_GENERATED_LENGTH', 'GENERATED_LENGTH')
        self._setenv('PASSWORD_STORE_CHARACTER_SET', 'CHARACTER_SET')
        self._setenv('PASSWORD_STORE_CHARACTER_SET_NO_SYMBOLS',
                     'CHARACTER_SET_NO_SYMBOLS')
        self._setenv('PASSWORD_STORE_ENABLE_EXTENSIONS')
        self._setenv('PASSWORD_STORE_EXTENSIONS_DIR', 'EXTENSIONS')
        self._setenv('PASSWORD_STORE_SIGNING_KEY')
        self._setenv('GNUPGHOME')

        if prefix:
            self.prefix = prefix
        if 'PASSWORD_STORE_DIR' not in self.env:
            raise PasswordStoreError("pass prefix unknown")

    def _setenv(self, var, env=None):
        """Add var in the environment variables dictionary."""
        if env is None:
            env = var
        if env in os.environ:
            self.env[var] = os.environ[env]

    def _call(self, command, data=None):
        """Call to a command."""
        with Popen(command, universal_newlines=True, env=self.env, stdin=PIPE,
                   stdout=PIPE, stderr=PIPE, shell=False) as process:
            (stdout, stderr) = process.communicate(data)
            res = process.wait()
            return res, stdout, stderr

    def _pass(self, arg=None, data=None):
        """Call to password store."""
        command = [self._passbinary]
        if arg is not None:
            command.extend(arg)

        res, stdout, stderr = self._call(command, data)
        if res:
            raise PasswordStoreError("%s %s" % (stderr, stdout))
        return stdout

    @property
    def prefix(self):
        """Get password store prefix from PASSWORD_STORE_DIR."""
        return self.env['PASSWORD_STORE_DIR']

    @prefix.setter
    def prefix(self, value):
        self.env['PASSWORD_STORE_DIR'] = value

    def list(self, path=''):
        """List the paths in the password store repository."""
        prefix = os.path.join(self.prefix, path)
        if os.path.isfile(prefix + '.gpg'):
            paths = [path]
        else:
            paths = []
            for ppath in Path(prefix).rglob('*.gpg'):
                file = os.sep + str(ppath)[len(self.prefix) + 1:]
                if "%s." % os.sep not in file:
                    file = os.path.splitext(file)[0][1:]
                    paths.append(file)
        paths.sort()
        return paths

    def show(self, path):
        """Decrypt path and read the credentials in the password file."""
        entry = dict()
        entry['group'] = os.path.dirname(path)
        entry['title'] = os.path.basename(path)
        data = self._pass(['show', path]).split('\n')
        data.pop()
        if data:
            line = data.pop(0)
            if ': ' in line:
                (key, value) = line.split(': ', 1)
                entry[key] = value
            else:
                entry['password'] = line
        for line in data:
            if ': ' in line:
                (key, value) = line.split(': ', 1)
                entry[key] = value
            elif line.startswith('otpauth://'):
                entry['otpauth'] = line
            elif 'comments' in entry:
                entry['comments'] += '\n' + line
        return entry

    def exist(self):
        """Check if the password store is initialized."""
        return os.path.isfile(os.path.join(self.prefix, '.gpg-id'))

    def is_valid_recipients(self):
        """Ensure the GPG keyring is usable."""
        with open(os.path.join(self.prefix, '.gpg-id'), 'r') as file:
            gpgids = file.read().split('\n')
            gpgids.pop()

        cmd = [self._gpgbinary, '--with-colons', '--batch', '--list-keys']
        for gpgid in gpgids:
            res, _, _ = self._call(cmd + [gpgid])
            if res:
                return False

        cmd = [self._gpgbinary, '--with-colons', '--batch',
               '--list-secret-keys']
        for gpgid in gpgids:
            res, _, _ = self._call(cmd + [gpgid])
            if res == 0:
                return True
        return False


class PwnedAPI():
    """Simple wrapper for https://haveibeenpwned.com API."""

    def __init__(self):
        self.headers = {'user-agent': 'pass-audit/%s' % __version__}

    def password_range(self, prefix):
        """Query the haveibeenpwned api to retrieve the bucket ``prefix``."""
        url = "https://api.pwnedpasswords.com/range/%s" % prefix
        res = requests.get(url, headers=self.headers, verify=True)
        res.raise_for_status()

        hashes = []
        counts = []
        for item in res.text.split('\r\n'):
            (partialhash, count) = item.split(':')
            hashes.append(prefix + partialhash)
            counts.append(int(count))
        return (hashes, counts)


class PassAudit():
    """Pass audit main class."""

    def __init__(self, data, msg):
        self.data = data
        self.msg = msg

    def password(self):
        """K-anonimity password breach detection on haveibeenpwned.com."""
        # Generate the list of hashes and prefixes to query.
        self.msg.verbose("Checking for breached passwords [hibp]:")
        data = []
        prefixes = []
        api = PwnedAPI()
        buckets = dict()
        for path, entry in self.data.items():
            self.msg.verbose("[hibp] %s" % path)
            password = entry.get('password', '').encode("utf8")
            phash = hashlib.sha1(password).hexdigest().upper()  # nosec
            prefix = phash[0:5]
            data.append((path, entry, phash, prefix))
            if prefix not in prefixes:
                prefixes.append(prefix)
                buckets[prefix] = api.password_range(prefix)

        # Compare the data and return the breached passwords.
        breached = []
        for path, entry, phash, prefix in data:
            if phash in buckets[prefix][0]:
                index = buckets[prefix][0].index(phash)
                count = buckets[prefix][1][index]
                breached.append((path, entry.get('password', ''), count))
        return breached

    def zxcvbn(self):
        """Password strength estimaton usuing Dropbox' zxcvbn."""
        self.msg.verbose("Checking for weak passwords [zxcvbn]:")
        breached = []
        for path, entry in self.data.items():
            self.msg.verbose("[zxcvbn] %s" % path)
            password = entry.get('password', '')
            user_input = list(entry.values()) + path.split(os.sep)
            user_input.remove(password)
            results = zxcvbn(password, user_inputs=user_input)
            if results['score'] <= 2:
                breached.append((path, password, results))
        return breached


def argumentsparse(argv):
    """Geting arguments for 'pass import'."""
    parser = argparse.ArgumentParser(prog='pass audit', description="""
  A pass extension for auditing your password repository. It supports safe
  breached password detection from haveibeenpwned.com using K-anonymity method
  and password strength estimaton usuing zxcvbn.""",
    formatter_class=argparse.RawDescriptionHelpFormatter,  # noqa
    epilog="More information may be found in the pass-audit(1) man page.")

    parser.add_argument('paths', type=str, nargs='?', metavar='pass-names',
                        default='', help="""Path(s) to audit in the password
                        store, If empty audit the full store.""")
    parser.add_argument('-q', '--quiet', action='store_true', help='Be quiet.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Be verbose.')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s ' + __version__,
                        help='Show the program version and exit.')

    return parser.parse_args(argv)


def sanitychecks(arg, msg):
    """Sanity checks."""
    if arg.paths == '':
        msg.message("Auditing whole store - this may take some time")

    store = PasswordStore()
    if not store.exist():
        msg.die("no password store to audit.")
    if not store.is_valid_recipients():
        msg.die('invalid user ID, password encryption aborted.')

    paths = store.list(arg.paths)
    if not paths:
        msg.die("%s is not in the password store." % arg.paths)

    return (store, paths)


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


def main(argv):
    """pass-audit main function."""
    arg = argumentsparse(argv)
    msg = Msg(arg.verbose, arg.quiet)
    (store, paths) = sanitychecks(arg, msg)

    # Read data from the password store.
    msg.verbose("Reading password store [init]:")
    data = dict()
    for path in paths:
        try:
            msg.verbose("[init] %s" % path)
            data[path] = store.show(path)
        except PasswordStoreError as error:
            msg.warning("Imposible to read %s from the password store: %s"
                        % (path, error))

    # Start the audit of the password store
    audit = PassAudit(data, msg)
    breached = audit.password()
    weak = audit.zxcvbn()

    # Report!
    report(msg, data, breached, weak)


if __name__ == "__main__":
    sys.argv.pop(0)
    main(sys.argv)
