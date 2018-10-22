#! /bin/bash

echo "flake8 check..."
flake8 pyTD
rc=$?; if [[ $rc != 0 ]]; then
	echo "flake8 check failed."
	exit $rc;
fi
echo "PASSED"

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
