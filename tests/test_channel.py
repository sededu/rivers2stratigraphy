import pytest

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

from rivers2stratigraphy.channel import ActiveChannel

def test1():
    assert True

def test2():
    assert True

def default_ActiveChannel():
    activeChannel = ActiveChannel()
    assert activeChannel.avul_num == 0
    assert activeChannel.Bast == 0
