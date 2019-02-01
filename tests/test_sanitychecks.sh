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

test_done
