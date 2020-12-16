import shutil
from pathlib import Path

import pytest

root = Path(__file__).parent.parent.parent
root /= 'tests/fixtures'

@pytest.fixture
def mock_env_user(monkeypatch):
    monkeypatch.setenv("USERNAME", "Test_User")
    monkeypatch.setenv("HOME", str(root / '_home'))

@pytest.fixture
def temp_datadir(tmpdir):
    test_dir = root / 'data'
    if test_dir.is_dir():
        shutil.copytree(test_dir, tmpdir, dirs_exist_ok=True)
    return tmpdir

@pytest.fixture
def fix_dir() -> Path:
    return root

@pytest.fixture
def temp_confdir(tmpdir):
    test_dir = root / 'config'
    if test_dir.is_dir():
        tmpdir = shutil.copytree(test_dir, tmpdir, dirs_exist_ok=True)
    return tmpdir
