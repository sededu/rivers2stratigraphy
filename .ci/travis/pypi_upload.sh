#!/usr/bin/env bash
# borrowed from Landlab implementation

if [[ "$RELEASE" == "1" ]]; then
  echo "Uploading to Pypi."
  twine upload -u amoodie -p$PYPI_PASS dist/*
  echo "Done."
else
  echo "RELEASE != 1"
  echo "Not deploying."
  echo "Tag is... $TRAVIS_TAG"
  echo "Branch name is... $TRAVIS_BRANCH"
fi
