#!/usr/bin/env bash
# borrowed from Landlab implementation

RELEASE=$RELEASE

if [[ "$RELEASE" == "1" ]]; then
	if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
      	echo "Uploading to Pypi."
  		twine upload -u amoodie -p$PYPI_PASS dist/*
  		echo "Done."
		# else
  		#   echo "Creating a binary wheel distribution."
  		#   python setup.py bdist_wheel
  	fi
fi
