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
	@echo "pass-$(PROG) was built succesfully. You can now install it wit \"make install\""
	@echo
	@echo "To run pass $(PROG) one needs to have some tools installed on the system:"
	@echo "     password-store, python3, python3-requests and python3-zxcvbn"

install:
	@install -v -d "$(DESTDIR)$(MANDIR)/man1"
	@install -v -d "$(DESTDIR)$(SYSTEM_EXTENSION_DIR)/"
	@install -v -d "$(DESTDIR)$(BASHCOMPDIR)"
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
	make -C tests

lint:
	shellcheck -s bash $(PROG).bash

clean:
	@rm -vrf tests/test-results/ tests/gnupg/random_seed

.PHONY: install uninstall tests lint clean
