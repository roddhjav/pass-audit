# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog][keep-changelog].

## [1.2] - 2022-01-30
### Added
- Check for duplicate / re-used passwords  [#22](https://github.com/roddhjav/pass-audit/issues/22)
- Add option to limit checks to specific filename (-n, --name) [#26](https://github.com/roddhjav/pass-import/pull/26)

### Changed
- Simplify the audit process
- Use setup.py to manage the full installation and deprecate the Makefile
- Use only Gitlab CI, remove Travis for CI/CD

### Fixed
- Terminate the GnuPG commandline as it could potentially be a security issue. [#28](https://github.com/roddhjav/pass-import/pull/28).
- Multiple minor fixes: [#20](https://github.com/roddhjav/pass-import/pull/26), [#21](https://github.com/roddhjav/pass-import/pull/26),  [#25](https://github.com/roddhjav/pass-import/pull/26)


## [1.1] - 2020-04-26
### Added
* Added Debian packaging

### Changed
* Import the structure from pass-import into pass-audit
* pass-audit will run even if zxcvbn is not present


## [1.0.1] - 2019-02-01
### Fixed
* Fixed makefile


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


[1.2]: https://github.com/roddhjav/pass-audit/releases/tag/v1.2
[1.1]: https://github.com/roddhjav/pass-audit/releases/tag/v1.1
[1.0.1]: https://github.com/roddhjav/pass-audit/releases/tag/v1.0.1
[1.0]: https://github.com/roddhjav/pass-audit/releases/tag/v1.0
[0.1]: https://github.com/roddhjav/pass-audit/releases/tag/v0.1

[keep-changelog]: https://keepachangelog.com/en/1.0.0/
