import os
import pytest


@pytest.fixture
def testdata_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
