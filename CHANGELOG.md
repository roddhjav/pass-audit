# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog][keep-changelog].

## [1.0] - 2019-02-01
### Added
* Add support for zxcvbn.

### Changed
* Allow audit of given paths.
* Add support for individual and multiple paths.
* Changed the extension structure to a classic python program:
  - The extension is now installed using setuptools for the python part,
  - Use `prospector` and `bandit` as python linter tool and security checker,
  - Add Gitlab CI,
  - Add SAST [security dashboard](https://gitlab.com/roddhjav/pass-audit/security/dashboard),
  - Simplify the tests.

### Fixed
* Ignore the first line of a file when parsing user input [#10](https://github.com/roddhjav/pass-import//pull/10).
* Include passwords not located in subdirectory in checks [#11](https://github.com/roddhjav/pass-import//pull/11).

## [0.1] - 2018-02-24

* Initial release.


[0.2]: https://github.com/roddhjav/pass-audit/releases/tag/v1.0
[0.1]: https://github.com/roddhjav/pass-audit/releases/tag/v0.1

[keep-changelog]: https://keepachangelog.com/en/1.0.0/
