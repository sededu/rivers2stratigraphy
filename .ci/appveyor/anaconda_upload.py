import os
import sys
import subprocess
import traceback
import glob

print('Using python: {prefix}'.format(prefix=sys.prefix))

repo_tag = os.environ.get('APPVEYOR_REPO_TAG', 'false')
tag_name = os.environ.get('APPVEYOR_REPO_TAG_NAME', '')
token = os.environ.get('CONDA_TOKEN', 'NOT_A_TOKEN')

if repo_tag == 'true' and tag_name.startswith('v'):
    # print('Repo is tagged and starts with v:')
    print('Uploading to "main" channel......')
    _upload = True
    channel = 'main'
    os.environ['BUILD_STR'] = ''
elif repo_tag == 'true' and not tag_name.startswith('v'):
    # print('Repo is tagged but not a release:')
    print('Uploading to "dev" channel......')
    _upload = True
    channel = 'dev'
    os.environ['BUILD_STR'] = 'dev'
else:
    _upload = False

if _upload:
    # try to locate the built file, 
    # if you can't find it, assume build failed

    # anaconda -t $CONDA_TOKEN upload --force --user sededu --channel main .ci/conda-build/**/rivers2stratigraphy*bz2
        

    binary_path = glob.glob('.ci/conda-build/**/rivers2stratigraphy*bz2')
    if os.path.isfile(binary_path):
        print('File to upload located at:\n\t', binary_path)
    else:
        raise RuntimeError('{name}: not a file'.format(name=binary_path))

    cmd = ' '.join(['anaconda', '-t', token, 'upload', '--force',
                    '--user', 'sededu', '--channel', channel,
                    binary_path.decode('utf-8')])

    try:
        print('Uploading to Anaconda Cloud with command:\n\t',
              cmd)
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        traceback.print_exc()
