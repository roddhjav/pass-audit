PROG ?= audit
PREFIX ?= /usr
DESTDIR ?= /
LIBDIR ?= $(PREFIX)/lib
SYSTEM_EXTENSION_DIR ?= $(LIBDIR)/password-store/extensions
MANDIR ?= $(PREFIX)/share/man

BASHCOMPDIR ?= /etc/bash_completion.d
ZSHCOMPDIR ?= $(PREFIX)/share/zsh/site-functions

all:
	@python3 setup.py build
	@echo
	@echo "pass-$(PROG) was built successfully. You can now install it with \"make install\""
	@echo
	@echo "To run pass $(PROG) one needs to have some tools installed on the system:"
	@echo "     password-store, python3, python3-requests and python3-zxcvbn"

install:
	@install -v -d "$(DESTDIR)$(MANDIR)/man1"
	@install -v -d "$(DESTDIR)$(SYSTEM_EXTENSION_DIR)/"
	@install -v -d "$(DESTDIR)$(BASHCOMPDIR)" "$(DESTDIR)$(ZSHCOMPDIR)"
	@install -v -m 0755 "$(PROG).bash" "$(DESTDIR)$(SYSTEM_EXTENSION_DIR)/$(PROG).bash"
	@install -v -m 0644 "pass-$(PROG).1" "$(DESTDIR)$(MANDIR)/man1/pass-$(PROG).1"
	@install -v -m 0644 "completion/pass-$(PROG).bash" "$(DESTDIR)$(BASHCOMPDIR)/pass-$(PROG)"
	@install -v -m 0644 "completion/pass-$(PROG).zsh" "$(DESTDIR)$(ZSHCOMPDIR)/_pass-$(PROG)"
	@python3 setup.py install --root="$(DESTDIR)" --prefix="$(PREFIX)" --optimize=1 --skip-build
	@echo
	@echo "pass-$(PROG) is installed succesfully"
	@echo

uninstall:
	@rm -vrf \
		"$(DESTDIR)$(SYSTEM_EXTENSION_DIR)/$(PROG).bash" \
		"$(DESTDIR)$(MANDIR)/man1/pass-$(PROG).1" \
		"$(DESTDIR)$(ZSHCOMPDIR)/_pass-$(PROG)" \
		"$(DESTDIR)$(BASHCOMPDIR)/pass-$(PROG)"


PASSWORD_STORE_DIR ?= $(HOME)/.password-store
PASSWORD_STORE_EXTENSIONS_DIR ?= $(PASSWORD_STORE_DIR)/.extensions
local:
	@install -v -d "$(DESTDIR)$(PASSWORD_STORE_EXTENSIONS_DIR)/"
	@install -v -m 0755 "$(PROG).bash" "$(DESTDIR)$(PASSWORD_STORE_EXTENSIONS_DIR)/$(PROG).bash"
	@python3 setup.py install --user --optimize=1
	@echo
	@echo "pass-$(PROG) is localy installed succesfully."
	@echo "Warning, because it is a local installation, there is no manual page or shell completion."


tests:
	@python3 -m green -vvv --run-coverage --termcolor --processes $(shell nproc)
	@coverage html

lint:
	@prospector --profile .prospector.yaml --strictness veryhigh \
		-t dodgy -t mccabe -t pep257 -t pep8 -t pylint \
		-t profile-validator -t pyflakes -t pyroma \
		pass_audit/
	@prospector --profile .prospector.yaml --strictness veryhigh \
		-t dodgy -t mccabe -t pep257 -t pep8 -t pylint \
		-t profile-validator -t pyflakes -t pyroma \
		setup.py
	@prospector --profile .prospector.yaml  --strictness veryhigh \
		-t dodgy -t mccabe -t mypy -t pep257 -t pep8 -t pylint \
		-t profile-validator -t pyflakes -t pyroma \
		tests/

security:
	@bandit -r pass_audit tests setup.py

clean:
	@rm -rf .coverage .mypy_cache .pybuild .ropeproject build \
		debian/.debhelper debian/debhelper* debian/pass-extension-import* \
		dist *.egg-info htmlcov */__pycache__/ __pycache__ \
		session.baseline.sqlite session.sqlite \
		tests/gnupg/random_seed tests/test-results/

.PHONY: install uninstall local tests tests_bash $(T) lint security clean
