import configargparse

import pytest
import attr
from pathlib import Path
from pyentrez.main import cmdline
from pyentrez import exceptions
from loguru import logger

test_args1 = {'credentials': False, 'version': False, 'mongo': False, 'TUI': 'on', 'INIT': False, 'email': 'notarealemail@fake.edu', 'user': None, 'db': 'pubmed', 'sort': 'relevance', 'retmax': 200, 'retmode': 'txt', 'rettype': 'medline', 'dbURI': None}
test_args2 = {'credentials': False, 'version': False, 'mongo': False, 'TUI': 'off', 'INIT': False, 'email': 'notarealemail@fake.edu', 'user': None, 'db': 'pubmed', 'sort': 'relevance', 'retmax': 200, 'retmode': 'txt', 'rettype': 'medline', 'dbURI': None}
test_args3 = {'credentials': False, 'version': False, 'mongo': False, 'TUI': 'on', 'INIT': True, 'email': 'notarealemail@fake.edu', 'user': None, 'db': 'pubmed', 'sort': 'relevance', 'retmax': 200, 'retmode': 'txt', 'rettype': 'medline', 'dbURI': None}
test_args = [test_args1, test_args2, test_args3]
# test_parse = configargparse.ArgumentParser(description='Dick Dick DIck Dick Dick .', formatter_class=configargparse.DefaultsRawFormatter)

"""
class A(object):
    def __init__(self, *args):
        for key, value in test_args1.items():
            setattr(self, key, value)


class B(object):
    def __init__(self, *args):
        for key, value in test_args2.items():
            setattr(self, key, value)


class C(object):
    def __init__(self, *args):
        for key, value in test_args3.items():
            setattr(self, key, value)
"""
"""
Run order:
- Execute tries _run
- _run calls initialize()
    - initialize creates a parser and sets Home path
- _run calls run_pyentrez()
    - run_pyentrez checks args and calls for:
        - first_run, starttui, or notui
            - _first_run makes a new user
            - starttui makes a cui root, manager, and starts
            - notui makes a cmd_entrez and starts

"""

"""config = {'return_value': (configargparse.ArgumentParser(None), tmpdir)}
        m1 = mocker.patch('pyentrez.cmdline.get_parser', **config)
        m2 = mocker.patch('configargparse.ArgumentParser.parse_args', A)
        m3 = mocker.patch('pyentrez.cmdline.starttui')
        print(m3.called)
        m4 = mocker.patch('pyentrez.cmdline.notui')
        m5 = mocker.patch('pyentrez.user_cred.first_run')

        execute()
        assert(m3.called)
        assert(not m4.called)
        assert(not m5.called)"""

@attr.s
class MockedParser:
    args = attr.ib()
    path = attr.ib()

    @classmethod
    def set_1(cls, tmpdir):
        set_ret = test_args[0]
        return cls(set_ret, tmpdir)

    @classmethod
    def set_2(cls, tmpdir):
        set_ret = test_args[1]
        return cls(set_ret, tmpdir)

    @classmethod
    def set_3(cls, tmpdir):
        set_ret = test_args[2]
        return cls(set_ret, tmpdir)



class TestCmdline:
    def test_mocker(self, mocker):
        tester = cmdline.CLI()
        m1 = mocker.patch('pyentrez.main.cmdline.CLI.execute')
        tester.execute()
        assert m1.called
        assert tester.catastrophic_failure is False

    def test_execute_keyboardinterrupt(self, mocker):
        tester = cmdline.CLI()
        m1 = mocker.patch('pyentrez.main.cmdline.CLI._run',
                          side_effect=KeyboardInterrupt)
        tester.execute()
        assert tester.catastrophic_failure is True

    def test_execute_executionerror(self, mocker):
        tester = cmdline.CLI()
        m1 = mocker.patch('pyentrez.main.cmdline.CLI._run',
                          side_effect=exceptions.ExecutionError("Raised"))
        tester.execute()
        assert tester.catastrophic_failure is True

    def test_execute_earlyquit(self, mocker):
        tester = cmdline.CLI()
        m1 = mocker.patch('pyentrez.main.cmdline.CLI._run',
                          side_effect=exceptions.EarlyQuit("Raised"))
        tester.execute()
        assert tester.catastrophic_failure is True

    def test_initialize(self, mocker, tmpdir):
        tester = cmdline.CLI()
        m1 = mocker.patch('pyentrez.main.cmdline.GetParser.get_parser',
                          return_value=MockedParser.set_1(tmpdir))
        tester.initialize()
        assert tester.args.get('Home') == str(tmpdir)
        assert m1.called

    def test_run_pyentrez_version(self):
        tester = cmdline.CLI()
        tester.args = test_args[0]
        tester.args['version'] = True
        with pytest.raises(SystemExit):
            tester.run_pyentrez()

    def test_run_pyentrez_starttui(self, mocker):
        tester = cmdline.CLI()
        tester.args = test_args[0]
        tester.args['verbose'] = None
        tester.args['output'] = None
        m0 = mocker.patch('pyentrez.configure_logger')
        m1 = mocker.patch('pyentrez.main.cmdline.CLI.starttui')
        m2 = mocker.patch('pyentrez.main.cmdline.CLI.notui')
        tester.run_pyentrez()
        assert m0.called
        assert m1.called
        assert not m2.called

    def test_run_pyentrez_notui(self, mocker):
        tester = cmdline.CLI()
        tester.args = test_args[1]
        tester.args['verbose'] = None
        tester.args['output'] = None
        m0 = mocker.patch('pyentrez.configure_logger')
        m1 = mocker.patch('pyentrez.main.cmdline.CLI.starttui')
        m2 = mocker.patch('pyentrez.main.cmdline.CLI.notui')
        tester.run_pyentrez()
        assert m0.called
        assert not m1.called
        assert m2.called

    def test_run_pyentrez_init(self, mocker):
        tester = cmdline.CLI()
        tester.args = test_args[2]
        m1 = mocker.patch('pyentrez.main.user_cred.first_run')
        tester.run_pyentrez()
        assert m1.called





