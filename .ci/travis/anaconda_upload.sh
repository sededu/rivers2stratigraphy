#!/usr/bin/env bash

if [[ "$TRAVIS_TAG" == v* ]]; then
	{ # try

		echo "Uploading to Anaconda Cloud main channel"
		anaconda -t $CONDA_TOKEN upload --force --user sededu --channel main .ci/conda-build/**/rivers2stratigraphy*bz2
		echo "Upload to Anaconda Cloud main channel successful!"
		exit 0

	} || { # catch

		echo -e "Failed during upload to Anaconda Cloud main channel!"
		exit 1

	}
else
    	{ # try

		echo "Uploading to Anaconda Cloud"
		anaconda -t $CONDA_TOKEN upload --force --user sededu --channel dev .ci/conda-build/**/rivers2stratigraphy*bz2
		echo "Upload to Anaconda Cloud dev channel successful!"
		exit 0

	} || { # catch

		echo -e "Failed during upload to Anaconda Cloud dev channel!"
		exit 1

	}
fi


