#!/usr/bin/env bash

{ # try

	echo "Uploading to Anaconda Cloud"
	anaconda -t $CONDA_TOKEN upload --force --user sededu .ci/conda-build/**/rivers2stratigraphy*bz2
	echo "Upload to Anaconda Cloud successful!"

} || { # catch

	echo -e "Failed during upload to Anaconda Cloud!"
	exit 1

}



