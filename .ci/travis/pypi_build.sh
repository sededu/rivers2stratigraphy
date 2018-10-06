#!/usr/bin/env bash
# borrowed from Landlab implementation

TRAVIS_TAG=$TRAVIS_TAG
TRAVIS_BRANCH=$TRAVIS_BRANCH
RELEASE=$RELEASE

if [[ "$RELEASE" == "1" ]]; then
        echo "RELEASE = 1"
        echo "Tag is... $TRAVIS_TAG"
        echo "Branch name is... $TRAVIS_BRANCH"

        echo "Installing deployment requirements."
        pip3 install twine wheel
    if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
        echo "Creating a source distribution."
        python setup.py sdist bdist_wheel
    # else
        # echo "Creating a binary wheel distribution."
        # python setup.py bdist_wheel
    fi
else
  echo "RELEASE != 1"
  echo "Not deploying to pypi."
  echo "Tag is... $TRAVIS_TAG"
  echo "Branch name is... $TRAVIS_BRANCH"
fi
