# -*- encoding: utf-8 -*-
# pass audit - Password Store Extension (https://www.passwordstore.org/)
# Copyright (C) 2018-2020 Alexandre PUJOL <alexandre@pujol.io>.
#

import os
import shutil
from subprocess import Popen, PIPE  # nosec
from pathlib import Path


class PasswordStoreError(Exception):
    """Error in the execution of password store."""


class PasswordStore():
    """Simple Password Store wrapper for python.

    Based on the PasswordStore class from pass-import.
    See https://github.com/roddhjav/pass-import for more information.

    """

    def __init__(self, prefix=None):
        self._binary = shutil.which('pass')
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
        if 'PASSWORD_STORE_DIR' not in self.env or self.prefix is None:
            raise PasswordStoreError("pass prefix unknown")

    def _setenv(self, var, env=None):
        """Add var in the environment variables dictionary."""
        if env is None:
            env = var
        if env in os.environ:
            self.env[var] = os.environ[env]

    def _call(self, command, data=None, nline=True):
        """Call to a command."""
        if isinstance(data, bytes):
            nline = False
        with Popen(command, universal_newlines=nline, env=self.env, stdin=PIPE,
                   stdout=PIPE, stderr=PIPE, shell=False) as process:
            (stdout, stderr) = process.communicate(data)
            res = process.wait()
            return res, stdout, stderr

    def _command(self, arg, data=None, nline=True):
        """Call to the password manager cli command."""
        command = [self._binary]
        command.extend(arg)
        res, stdout, stderr = self._call(command, data, nline)
        if res:
            raise PasswordStoreError(f"{stderr} {stdout}")
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
                if f"{os.sep}." not in file:
                    file = os.path.splitext(file)[0][1:]
                    paths.append(file)
        paths.sort()
        return paths

    def show(self, path):
        """Decrypt path and read the credentials in the password file."""
        entry = {}
        entry['group'] = os.path.dirname(path)
        entry['title'] = os.path.basename(path)
        try:
            data = self._command(['show', path]).split('\n')
        except UnicodeDecodeError:
            entry['data'] = self._command(['show', path], nline=False)
            return entry

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

    def isvalid(self):
        """Ensure the GPG keyring is usable."""
        trusted = ['m', 'f', 'u', 'w', 's']
        with open(os.path.join(self.prefix, '.gpg-id'), 'r') as file:
            gpgids = file.read().split('\n')
            gpgids.pop()

        cmd = [
            self._gpgbinary,
            '--with-colons',
            '--batch',
            '--list-keys',
            '--',
        ]
        for gpgid in gpgids:
            res, out, _ = self._call(cmd + [gpgid])
            if res:
                return False
            for line in out.split('\n'):
                record = line.split(':')
                if record[0] == 'pub':
                    trust = record[1]
            if trust not in trusted:
                return False

        cmd = [
            self._gpgbinary,
            '--with-colons',
            '--batch',
            '--list-secret-keys',
            '--',
        ]
        for gpgid in gpgids:
            res, _, _ = self._call(cmd + [gpgid])
            if res == 0:
                return True
        return False
