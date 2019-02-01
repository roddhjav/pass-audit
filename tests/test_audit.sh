#!/usr/bin/env bash

export test_description="Testing 'pass audit'"
cd tests
source ./commons.sh
test_cleanup

test_expect_success 'Testing passwords audit with K-anonymity method.' '
    _pass audit Password/
    '

test_done
