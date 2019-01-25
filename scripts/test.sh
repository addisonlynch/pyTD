#! /bin/bash

# Obtain refresh token and store
A=$(python get_refresh_token.py)
export TD_REFRESH_TOKEN=$A

cd ..

# flake8 check
echo "flake8 check..."
flake8 pyTD
rc=$?; if [[ $rc != 0 ]]; then
	echo "flake8 check failed."
	exit $rc;
fi
echo "PASSED"

# flake8-rst check
echo "flake8-rst docs check..."
flake8-rst --filename="*.rst" .
rc=$?; if [[ $rc != 0 ]]; then
    echo "flake8-rst docs check failed."
    exit $rc;
fi
echo "PASSED"

# run all tests
echo "pytest..."
cd pyTD
pytest -x tests
rc=$?;

if [[ $rc != 0 ]]; then
	echo "Pytest failed."
	exit $rc
fi
echo "PASSED"

echo 'All tests passed!'
