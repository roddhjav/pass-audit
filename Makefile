DESTDIR ?= /

all:
	@python3 setup.py build
	@echo "pass-audit was built successfully. You can now install it with \"make install\""

install:
	@python3 setup.py install --root="$(DESTDIR)" --optimize=1 --skip-build
	@echo "pass-audit is installed successfully"

local:
	@python3 setup.py install --user --optimize=1
	@echo "pass-audit is locally installed successfully."
	@echo "Remember to set PASSWORD_STORE_ENABLE_EXTENSIONS to 'true' for the extension to be enabled."

tests:
	@python3 -m green -vvv --run-coverage --termcolor --processes $(shell nproc)
	@coverage html

lint:
	@prospector --profile .prospector.yaml --strictness veryhigh \
		-t dodgy -t mccabe -t pydocstyle -t pycodestyle -t pylint \
		-t profile-validator -t pyflakes -t pyroma \
		pass_audit/
	@prospector --profile .prospector.yaml --strictness veryhigh \
		-t dodgy -t mccabe -t pydocstyle -t pycodestyle -t pylint \
		-t profile-validator -t pyflakes \
		setup.py
	@prospector --profile .prospector.yaml  --strictness veryhigh \
		-t dodgy -t mccabe -t mypy -t pydocstyle -t pycodestyle -t pylint \
		-t profile-validator -t pyflakes -t pyroma \
		tests/

security:
	@bandit -r pass_audit tests setup.py

docs:
	@pandoc -t man -s -o share/man/man1/pass-audit.1 share/man/man1/pass-audit.md

GPGKEY ?= 06A26D531D56C42D66805049C5469996F0DF68EC
PKGNAME := pass-extension-audit
BUILDIR := /home/build/$(PKGNAME)
debian:
	@docker stop debian &> /dev/null || true
	@docker run --rm -tid --name debian --volume $(PWD):$(BUILDIR) \
	 	--volume $(HOME)/.gnupg:/home/build/.gnupg debian &> /dev/null || true
	@docker exec debian useradd -m -s /bin/bash -u $(shell id -u) build || true
	@docker exec debian chown -R build:build /home/build
	@docker exec debian apt-get update
	@docker exec debian apt-get -qq -y --no-install-recommends upgrade
	@docker exec debian apt-get -qq -y --no-install-recommends install \
			build-essential debhelper fakeroot dh-python python3-setuptools \
			python3-requests pass
	@docker exec -it --user build --workdir=$(BUILDIR) debian \
			dpkg-buildpackage -b -d -us -ui --sign-key=$(GPGKEY)
	@docker exec -it --user build debian bash -c 'mv ~/$(PKGNAME)*.* ~/$(PKGNAME)'
	@docker exec -it --user build debian bash -c 'mv ~/pass-audit*.* ~/$(PKGNAME)'

pip:
	@python setup.py sdist bdist_wheel
	@twine check dist/*
	@gpg --detach-sign -a dist/*
	@twine upload --sign --identity $(GPGKEY) dist/*

clean:
	@rm -rf .coverage .mypy_cache .pybuild .ropeproject build config.json \
		debian/.debhelper debian/debhelper* debian/pass-extension-audit* \
		debian/files *.deb *.buildinfo *.changes \
		dist *.egg-info htmlcov pass_audit/**/__pycache__/ */__pycache__/ \
		__pycache__ session.baseline.sqlite session.sqlite \
		tests/assets/gnupg/random_seed tests/assets/test-results/ \
		tests/**/__pycache__/

.PHONY: install local tests lint security pip debian clean
