#!/usr/bin/env bash
# borrowed from Landlab implementation

TRAVIS_TAG=$TRAVIS_TAG
TRAVIS_BRANCH=$TRAVIS_BRANCH

echo "Tag is... $TRAVIS_TAG"
echo "Branch name is... $TRAVIS_BRANCH"

if [[ "$DEPLOY" == "1" ]]; then
  echo "Installing deployment requirements."
  pip3 install twine wheel
  if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    echo "Creating a source distribution."
    python setup.py sdist
  else
    echo "Creating a binary wheel distribution."
    python setup.py bdist_wheel
  fi
else
  echo "Not deploying."
  echo "Tag is... $TRAVIS_TAG"
  echo "Branch name is... $TRAVIS_BRANCH"
fi
