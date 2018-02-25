<h1 align="center">pass audit</h1>
<p align="center">
    <a href="https://travis-ci.org/roddhjav/pass-audit">
        <img src="https://img.shields.io/travis/roddhjav/pass-audit/master.svg"
            alt="Build Status"></a>
    <a href="https://www.codacy.com/app/roddhjav/pass-audit">
        <img src="https://img.shields.io/codacy/coverage/593851adcd354d179bf5b5b43eac0440/master.svg"
	          alt="Code Coverage" /></a>
    <a href="https://www.codacy.com/app/roddhjav/pass-audit">
        <img src="https://img.shields.io/codacy/grade/593851adcd354d179bf5b5b43eac0440/master.svg"
            alt="Code Quality"></a>
</p>
<p align="center">
A <a href="https://www.passwordstore.org/">pass</a> extension for auditing your
password repository.
</p>

## Description
`pass audit` is a password-store extension for auditing your password repository.
It supports safe breached password detection from [haveibeenpwned.com][HIBP]
using a [K-anonymity][Kanonymity] method. Using this method, you do not need to
(fully) trust the server that stores the breached password. You should read the
[security consideration](#security-consideration) section for more information.

**Warning** This extension is still in development. As of today, it only
supports password breach detection from HIBP. Must more features are planned
including but not limited to:
* Full support for haveibeenpwned API,
* Extended support for password breached API,
* Fully featured, local password store analysis.


## Usage

```
usage: pass audit [-h] [-V] [paths]

  A pass extension for auditing your password repository. It supports safe
  breached password detection from haveibeenpwned.com using K-anonymity method.

positional arguments:
  paths          Path to audit in the password store.

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

More reading:
* https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/
* https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/


## Installation
If you do not wish to install this extension as system extension, you need to
enable user extension with `PASSWORD_STORE_ENABLE_EXTENSIONS=true pass`. You can
create an alias in `.bashrc`: `alias pass='PASSWORD_STORE_ENABLE_EXTENSIONS=true pass'`.
Otherwise you should use one of the following method to install a system
extemsion.

**Requirements**
* `pass 1.7.0` or greater.
* `python3` (python 3.4, 3.5 and 3.6 are supported)
* `python-requests`
  - Debian/Ubuntu: `sudo apt-get install python3-defusedxml`
  - OSX: `pip3 install requests`

**From git**
```sh
git clone https://github.com/roddhjav/pass-audit/
cd pass-import
sudo make install
```

**OS X**
```sh
git clone https://github.com/roddhjav/pass-audit/
cd pass-import
make install PREFIX=/usr/local
```

**ArchLinux**

`pass-audit` is available in the [Arch User Repository][aur].
```sh
pacaur -S pass-audit  # or your preferred AUR install method
```


## Contribution
Feedback, contributors, pull requests are all very welcome.


## License

    Copyright (C) 2018  Alexandre PUJOL

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

[aur]: https://aur.archlinux.org/packages/pass-audit
[pass]: https://www.passwordstore.org/
[Kanonymity]: https://en.wikipedia.org/wiki/K-anonymity
[HIBP]: https://haveibeenpwned.com/
