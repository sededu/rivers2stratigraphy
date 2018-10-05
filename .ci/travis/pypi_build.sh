#!/usr/bin/env bash
# borrowed from Landlab implementation

if [[ "$TRAVIS_TAG" == v* ]]; then
  echo "Installing deployment requirements."
  pip install twine wheel
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