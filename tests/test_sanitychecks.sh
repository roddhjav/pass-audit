#!/usr/bin/env bash

export test_description="Testing 'pass audit'"
cd tests
source ./commons.sh

test_expect_success 'Testing corner cases' '
    test_must_fail _pass audit --not-an-option
    '

test_expect_success 'Testing help message' '
    _pass audit --help | grep "[paths]" &&
    _pass audit --version | grep "pass audit"
    '

if test_have_prereq CI; then
    export PASSWORD_STORE_ENABLE_EXTENSIONS=''
    export PASSWORD_STORE_EXTENSIONS_DIR=''
    test_expect_success 'Testing extension installation' '
        make --directory=$EXT_HOME install &&
        _pass audit --version | grep "pass audit 1.0" &&
        make --directory=$EXT_HOME uninstall
        '
fi

test_done
