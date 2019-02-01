<h1 align="center">pass audit</h1>
<p align="center">
    <a href="https://travis-ci.org/roddhjav/pass-audit">
        <img src="https://img.shields.io/travis/roddhjav/pass-audit/master.svg?style=flat-square"
             alt="Build Status"></a>
    <a href="https://gitlab.com/roddhjav/pass-audit/pipelines">
        <img src="https://gitlab.com/roddhjav/pass-audit/badges/master/pipeline.svg?style=flat-square"
             alt="Pipeline Status" /></a>
    <a href="https://www.codacy.com/app/roddhjav/pass-audit">
        <img src="https://img.shields.io/codacy/coverage/593851adcd354d179bf5b5b43eac0440/master.svg?style=flat-square"
	           alt="Code Coverage" /></a>
    <a href="https://www.codacy.com/app/roddhjav/pass-audit">
        <img src="https://img.shields.io/codacy/grade/593851adcd354d179bf5b5b43eac0440/master.svg?style=flat-square"
             alt="Code Quality"></a>
    <a href="https://github.com/roddhjav/pass-audit/releases/latest">
        <img src="https://img.shields.io/github/release/roddhjav/pass-audit.svg?maxAge=600&style=flat-square"
             alt="Last Release" /></a>
</p>
<p align="center">
    A <a href="https://www.passwordstore.org/">pass</a> extension for auditing
    your password repository.
</p>

## Description
`pass audit` is a password-store extension for auditing your password repository.
Passwords will be checked against the Python implementation of Dropbox'
[`zxcvbn`][zxcvbn] algorithm and Troy Hunt's *Have I Been Pwned* Service.
It supports safe breached password detection from [haveibeenpwned.com][HIBP]
using a [K-anonymity][Kanonymity] method. Using this method, you do not need to
(fully) trust the server that stores the breached password. You should read the
[security consideration](#security-consideration) section for more information.


## Usage

```
usage: pass audit [-h] [-V] pass-names

  A pass extension for auditing your password repository. It supports safe
  breached password detection from haveibeenpwned.com using K-anonymity method
  and password strength estimaton usuing zxcvbn.

positional arguments:
  pass-names     Path(s) to audit in the password store, If empty audit the
                 full store.

optional arguments:
  -h, --help     show this help message and exit
  -q, --quiet    Be quiet.
  -v, --verbose  Be verbose.
  -V, --version  Show the program version and exit.

More information may be found in the pass-audit(1) man page.
```
See `man pass-audit` for more information.


## Examples

**Audit a subfolder for pwned passwords**
```
pass audit goodpasswords/
(*) None of the 7 passwords tested are breached.
 .  But it does not means they are strong.
```

```
pass audit pwnedpasswords/
 w  Password breached: password from Password/pwned/5 has been breached 3303003 time(s).
 w  Password breached: correct horse battery staple from Password/pwned/2 has been breached 2 time(s).
[x] Error: 7 passwords tested and 2 breached passwords found.
 .  You should update them with 'pass-update'.
```


## Security consideration

This program uses K-anonymity to retrieve the knowledge of breached passwords
from HIBP server. K-anonymity applied to breached password check on an untrusted
remote server is a recent cryptographic approach. It means only the first five
characters of the SHA1 hash of your password is sent to the server. It offers
decent anonymity; nevertheless, it is not an entirely secure solution.

**More reading:**
* https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/
* https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/


## Installation

**Requirements**
* `pass 1.7.0` or greater.
* `python3` (python 3.5 and 3.6 are supported)
* `python3-requests`
  - Debian/Ubuntu: `sudo apt-get install python3-requests`
  - OSX: `pip3 install requests`
* `python3-zxcvbn` (`pip3 install zxcvbn`)

**ArchLinux**

`pass-audit` is available in the [Arch User Repository][aur].
```sh
yay -S pass-audit  # or your preferred AUR install method
```

**From git**
```sh
git clone https://github.com/roddhjav/pass-audit/
cd pass-audit
make
sudo make install  # For OSX: make install PREFIX=/usr/local
```

**Stable version**
```sh
wget https://github.com/roddhjav/pass-audit/releases/download/v0.1/pass-audit-0.1.tar.gz
tar xzf pass-audit-0.1.tar.gz
cd pass-audit-0.1
make
sudo make install  # For OSX: make install PREFIX=/usr/local
```

[Releases][releases] and commits are signed using [`06A26D531D56C42D66805049C5469996F0DF68EC`][keys].
You should check the key's fingerprint and verify the signature:
```sh
wget https://github.com/roddhjav/pass-audit/releases/download/v0.1/pass-audit-0.1.tar.gz.asc
gpg --recv-keys 06A26D531D56C42D66805049C5469996F0DF68EC
gpg --verify pass-audit-0.1.tar.gz.asc
```

**Local install**

Alternatively, from git or a stable version you can do a local install with:
```sh
cd pass-audit
make local
```


## Contribution
Feedback, contributors, pull requests are all very welcome.

### Contributors
 * [Tobias Girstmair](https://gir.st/) (zxcvbn)


## License

    Copyright (C) 2018  Alexandre PUJOL and Contributors

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

[keys]: https://pujol.io/keys
[aur]: https://aur.archlinux.org/packages/pass-audit
[releases]: https://github.com/roddhjav/pass-audit/releases
[pass]: https://www.passwordstore.org/
[Kanonymity]: https://en.wikipedia.org/wiki/K-anonymity
[HIBP]: https://haveibeenpwned.com/
[zxcvbn]: https://blogs.dropbox.com/tech/2012/04/zxcvbn-realistic-password-strength-estimation/
