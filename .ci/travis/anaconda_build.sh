#!/usr/bin/env bash

conda install -q conda-build anaconda-client
conda build .ci/conda-recipe/ --output-folder .ci/conda-build/
