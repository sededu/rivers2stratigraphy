#!/usr/bin/env bash

{ # try

    conda create -q -n build-environment python=$TRAVIS_PYTHON_VERSION
	source activate build-environment

} || { # catch

    echo -e "Failed to create new build-environemnt!"
    exit 1

}


{ # try

    conda install -q conda-build anaconda-client
	conda build -q .ci/conda-recipe/ --output-folder .ci/conda-build/ --no-test

} || { # catch

    echo -e "Failed during build in anaconda_build.sh!"
    exit 1

}


