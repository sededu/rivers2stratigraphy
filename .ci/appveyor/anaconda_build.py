import os
import sys
import subprocess
import traceback
import glob

print('Using python: {prefix}'.format(prefix=sys.prefix))

repo_tag = os.environ.get('APPVEYOR_REPO_TAG', 'false')
tag_name = os.environ.get('APPVEYOR_REPO_TAG_NAME', '')
token = os.environ.get('ANACONDA_TOKEN', 'NOT_A_TOKEN')

if repo_tag == 'true' and tag_name.startswith('v'):
    print('Repo is tagged and starts with v:')
    print('Building for "main" channel......')
    _build = True
    channel = 'main'
    os.environ['BUILD_STR'] = ''
elif repo_tag == 'true' and not tag_name.startswith('v'):
    print('Repo is tagged but not a release:')
    print('Building for "dev" channel......')
    _build = True
    channel = 'dev'
    os.environ['BUILD_STR'] = 'dev'
else:
    _build = False

if _build:
    try:
        cmd = ' '.join(['conda', 'build', os.path.join('.ci', 'conda-recipe'),
                        '--output-folder', os.path.join('.ci', 'conda-build'),
                        '--no-test'])
        response = subprocess.check_output(cmd, shell=True)
        print('Build succeeded.')
    except subprocess.CalledProcessError:
        print('\n\nBuild failed.\n\n')
        traceback.print_exc()
else:
    print('Not building.......')
