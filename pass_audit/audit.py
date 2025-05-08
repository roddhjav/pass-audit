# -*- encoding: utf-8 -*-
# pass audit - Password Store Extension (https://www.passwordstore.org/)
# Copyright (C) 2018-2022 Alexandre PUJOL <alexandre@pujol.io>.
#

import os
import hashlib

import requests
try:
    from zxcvbn import zxcvbn
    ZXCVBN = True
except ImportError:
    ZXCVBN = False

from pass_audit import __version__


class PwnedAPI():
    """Simple wrapper for https://haveibeenpwned.com API."""

    def __init__(self):
        self.headers = {'user-agent': f"pass-audit/{__version__}"}

    def password_range(self, prefix):
        """Query the haveibeenpwned API to retrieve the bucket ``prefix``."""
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
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

    def __init__(self, data, verbose):
        self.data = data
        self.verbose = verbose

    def password(self):
        """K-anonymity password breach detection on haveibeenpwned.com."""
        # Generate the list of hashes and prefixes to query.
        data = []
        api = PwnedAPI()
        buckets = {}
        for path, entry in self.data.items():
            if self.verbose:
                print(f"Getting the prefix of {path}")
            if entry.get('password', '') == '':
                continue
            password = entry['password'].encode("utf8")
            phash = hashlib.sha1(password).hexdigest().upper()  # nosec
            prefix = phash[0:5]
            data.append((path, entry, phash, prefix))
            if prefix not in buckets:
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
        """Password strength estimation using Dropbox' zxcvbn."""
        if not ZXCVBN:
            raise ImportError(name='zxcvbn')

        weak = []
        for path, entry in self.data.items():
            if self.verbose:
                print(f"Checking {path}")
            if entry.get('password', '') == '':
                continue
            password = entry['password']
            user_input = list(entry.values()) + path.split(os.sep)
            if password in user_input:
                user_input.remove(password)
            try:
                results = zxcvbn(password, user_inputs=user_input)
            except ValueError:
                pass
            else:
                if results['score'] <= 2:
                    weak.append((path, password, results))
        return weak

    def duplicates(self):
        """Check for duplicated passwords."""
        seen = {}
        for path, entry in self.data.items():
            if entry.get('password', '') == '':
                continue
            password = entry['password']
            if password in seen:
                seen[password].append(path)
            else:
                seen[password] = [path]

        duplicated = []
        for paths in seen.values():
            if len(paths) > 1:
                duplicated.append(paths)
        return duplicated
