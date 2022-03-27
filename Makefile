DESTDIR ?= /

all:
	@python3 setup.py build
	@echo "pass-audit was built successfully. You can now install it wit \"make install\""

install:
	@python3 setup.py install --root="$(DESTDIR)" --optimize=1 --skip-build
	@echo "pass-audit is installed succesfully"

local:
	@python3 setup.py install --user --optimize=1
	@echo "pass-audit is localy installed succesfully."
	@echo "Remember to set PASSWORD_STORE_ENABLE_EXTENSIONS to 'true' for the extension to be enabled."

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
		-t profile-validator -t pyflakes \
		setup.py
	@prospector --profile .prospector.yaml  --strictness veryhigh \
		-t dodgy -t mccabe -t mypy -t pep257 -t pep8 -t pylint \
		-t profile-validator -t pyflakes -t pyroma \
		tests/

security:
	@bandit -r pass_audit tests setup.py

docs:
	@pandoc -t man -s -o share/man/man1/pass-audit.1 share/man/man1/pass-audit.md

clean:
	@rm -rf .coverage .mypy_cache .pybuild .ropeproject build config.json \
		debian/.debhelper debian/debhelper* debian/pass-extension-audit* \
		debian/files *.deb *.buildinfo *.changes \
		dist *.egg-info htmlcov pass_audit/**/__pycache__/ */__pycache__/ \
		__pycache__ session.baseline.sqlite session.sqlite \
		tests/assets/gnupg/random_seed tests/assets/test-results/ \
		tests/**/__pycache__/

.PHONY: install uninstall local tests tests_bash $(T) lint security clean
