import os
import sys
import subprocess
import traceback
import glob


cmd = ' '.join(['conda', 'build', '.ci\\conda-recipe', '--output-folder', '.ci\\conda-build\\', '--no-test'])
resp = subprocess.check_output(cmd, shell=True)
print("anaconda build resp:", resp)