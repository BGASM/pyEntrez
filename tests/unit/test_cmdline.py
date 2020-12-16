import configargparse

from cmdline import execute

test_args1 = {'credentials': False, 'version': False, 'mongo': False, 'TUI': True, 'INIT': False, 'email': 'notarealemail@fake.edu', 'user': None, 'db': 'pubmed', 'sort': 'relevance', 'retmax': 200, 'retmode': 'txt', 'rettype': 'medline', 'dbURI': None}
test_args2 = {'credentials': False, 'version': False, 'mongo': False, 'TUI': False, 'INIT': False, 'email': 'notarealemail@fake.edu', 'user': None, 'db': 'pubmed', 'sort': 'relevance', 'retmax': 200, 'retmode': 'txt', 'rettype': 'medline', 'dbURI': None}
test_args3 = {'credentials': False, 'version': False, 'mongo': False, 'TUI': True, 'INIT': True, 'email': 'notarealemail@fake.edu', 'user': None, 'db': 'pubmed', 'sort': 'relevance', 'retmax': 200, 'retmode': 'txt', 'rettype': 'medline', 'dbURI': None}
test_parse = configargparse.ArgumentParser(description='Dick Dick DIck Dick Dick .', formatter_class=configargparse.DefaultsRawFormatter)


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



class TestCmdline:
   def test_execute_path1(self, tmpdir, mocker):
        config = {'return_value': (configargparse.ArgumentParser(None), tmpdir)}
        m1 = mocker.patch('pyentrez.cmdline.get_parser', **config)
        m2 = mocker.patch('configargparse.ArgumentParser.parse_args', A)
        m3 = mocker.patch('pyentrez.cmdline.starttui')
        print(m3.called)
        m4 = mocker.patch('pyentrez.cmdline.notui')
        m5 = mocker.patch('pyentrez.user_cred.first_run')

        execute()
        assert(m3.called)
        assert(not m4.called)
        assert(not m5.called)

   def test_execute_path2(self, tmpdir, mocker):
       config = {'return_value': (configargparse.ArgumentParser(None), tmpdir)}
       m1 = mocker.patch('pyentrez.cmdline.get_parser', **config)
       m2 = mocker.patch('configargparse.ArgumentParser.parse_args', B)
       m3 = mocker.patch('pyentrez.cmdline.starttui')
       print(m3.called)
       m4 = mocker.patch('pyentrez.cmdline.notui')
       m5 = mocker.patch('pyentrez.user_cred.first_run')

       execute()
       assert (not m3.called)
       assert (m4.called)
       assert (not m5.called)

   def test_execute_path3(self, tmpdir, mocker):
       config = {'return_value': (configargparse.ArgumentParser(None), tmpdir)}
       m1 = mocker.patch('pyentrez.cmdline.get_parser', **config)
       m2 = mocker.patch('configargparse.ArgumentParser.parse_args', C)
       m3 = mocker.patch('pyentrez.cmdline.starttui')
       print(m3.called)
       m4 = mocker.patch('pyentrez.cmdline.notui')
       m5 = mocker.patch('pyentrez.user_cred.first_run')

       execute()
       assert (m3.called and m5.called)
       assert (not m4.called)
