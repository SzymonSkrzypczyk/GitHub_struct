import pytest
from github_struct.dir_processing import _flatten, _get_files


def test_flatten():
    assert _flatten([[1, 2, 3], 4]) == [1, 2, 3, 4]
    assert _flatten([[[1, [2]], 3], 4]) == [1, 2, 3, 4]


def test_get_files():
    files = _get_files('https://github.com/realpython/materials/tree/master/serverless-sms-service')
    assert isinstance(files, list)
    assert not isinstance(files[0], list)
    assert len(files) > 0
