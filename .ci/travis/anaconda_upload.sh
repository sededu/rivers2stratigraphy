#!/usr/bin/env bash

echo "Uploading to Anaconda Cloud"
anaconda -t $CONDA_TOKEN upload --force --user sededu .ci/conda-build/**/rivers2stratigraphy*bz2

echo "Done."