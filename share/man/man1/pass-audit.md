% pass-audit(1)
% pass audit was written by Alexandre Pujol (alexandre@pujol.io)
% March 2022

# NAME

pass-audit — A *pass*(1) extension for auditing your password repository.

# SYNOPSIS

**pass audit** [*options…*] [*pass-names*]

# DESCRIPTION

**pass audit** is a password-store extension for auditing your password repository.
Passwords will be checked against the Python implementation of Dropbox'
**zxcvbn** algorithm and Troy Hunt's *Have I Been Pwned* Service.
It supports safe breached password detection from *haveibeenpwned.com*
using a **K-anonymity** method. Using this method, you do not need to
(fully) trust the server that stores the breached password. You should read the
*SECURITY CONSIDERATION* section for more information.


# COMMAND

**pass audit** [*options…*] [*pass-names*]

[*pass-names*]

: Path(s) to audit in the password store, If empty audit the full store.

`--name=<name>`, `-n <name>`

: Check only passwords with this filename.

`--help`, `-h`

: Print the program usage.

`--verbose`, `-v`

: Be more verbose. This option can be specified multiple times to set the
  verbosity level.

`--quiet`, `-q`

: Be quiet


# EXAMPLES

### Audit a subfolder for pwned passwords

```sh
pass audit goodpasswords/
(*) None of the 7 passwords tested are breached.
 .  But it does not means they are strong.
```

```sh
pass audit pwnedpasswords/
 w  Password breached: password from Password/pwned/5 has been breached 3303003 time(s).
 w  Password breached: correct horse battery staple from Password/pwned/2 has been breached 2 time(s).
[x] Error: 7 passwords tested and 2 breached passwords found.
 .  You should update them with 'pass-update'.
```

# SECURITY CONSIDERATION

## K-anonymity

This program uses K-anonymity to retrieve the knowledge of breached passwords
from HIBP server. K-anonymity applied to breached password check on an untrusted
remote server is a recent cryptographic approach. It means only the first five
characters of the SHA1 hash of your password is sent to the server. It offers
decent anonymity; nevertheless, it is not an entirely secure solution.

**More reading:**

* https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/
* https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/

## Mandatory Access Control (MAC)

AppArmor profiles for *pass* and *pass-audit* are available in **apparmor.d**.
If your distribution support AppArmor, you can clone the repository and run:

```sh
sudo ./pick pass pass-import
```

to only install these AppArmor security profiles.

## Network

pass-audit only needs to establish network connection to connect to the
*haveibeenpwned.com* server.

## Password Update

You might also want to update the passwords imported using **pass-update**(1).


# SEE ALSO
`pass(1)`, `pass-tomb(1)`, `pass-update(1)`, `pass-otp(1)`, `pimport(1)`, `pass-import(1)`
