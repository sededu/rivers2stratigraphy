import os
import sys
import subprocess
import traceback
import glob

print('Using python: {prefix}'.format(prefix=sys.prefix))

repo_tag = os.environ.get('APPVEYOR_REPO_TAG', 'false')
tag_name = os.environ.get('APPVEYOR_REPO_TAG_NAME', '')
token = os.environ.get('CONDA_TOKEN', 'NOT_A_TOKEN')
repo_branch = os.environ.get('APPVEYOR_REPO_BRANCH', '')
pull_request_num = os.environ.get('APPVEYOR_PULL_REQUEST_NUMBER', '')


if repo_tag == 'true' and tag_name.startswith('v'):
    print('Tag made for release:')
    print('Building for "main" channel......')
    _build = True
    channel = 'main'
    # os.environ['BUILD_STR'] = ''
elif repo_branch == 'master' and not pull_request_num:
    # if($env:APPVEYOR_REPO_BRANCH -eq "master" -and !$env:APPVEYOR_PULL_REQUEST_NUMBER)
    print('Commit made to master, and not PR:')
    print('Building for "dev" channel......')
    _build = True
    channel = 'dev'
    # os.environ['BUILD_STR'] = 'dev'
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
    print('No indicators made to build:')
    print('Not building.......')
