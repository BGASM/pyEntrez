import pytest
from _pytest.monkeypatch import MonkeyPatch

import __main__ as main

monkeypatch = MonkeyPatch()

@pytest.mark.parametrize("test_input", [(3,0), (2,6), (3,7)])
def test_main(monkeypatch, test_input):
    monkeypatch.setattr("sys.version_info", lambda x: (test_input))
    pytest.raises(Exception, main.main, match="Script needs to be run with Python 3.8")
