#!/usr/bin/env bash

{ # try

    conda install -q conda-build anaconda-client
	conda build -q .ci/conda-recipe/ --output-folder .ci/conda-build/ --no-test

} || { # catch

    echo -e "Failed during build in anaconda_build.sh!"
    exit 1

}


