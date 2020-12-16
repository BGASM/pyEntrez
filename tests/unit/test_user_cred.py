import os
from pathlib import Path, PosixPath, WindowsPath

from yaml import dump as dmp
from yaml import safe_load as sl

import user_cred


class TestUser_Cred:
    def safe_load(self, path):
        with open(path) as file1:
            return sl(file1)

    def safe_write(self, path, output):
        with open (path, 'w') as file2:
            return dmp(output, file2)

    def test_check_new_first(self, tmpdir, mocker):
        config_usr_path=[(True, None), (False, Path(tmpdir))]
        m1 = mocker.patch(
            'pyentrez.user_cred.get_usr_path',
            side_effect=[config_usr_path[0], config_usr_path[1]])
        m2 = mocker.patch('pyentrez.user_cred.first_run')
        # Test that the passed in directory gets returned on success
        assert (user_cred.check_new() == tmpdir)
        # Test that if a new user, function will loop back on itself
        assert m1.call_count==2 and m2.call_count==1

    def test_user_path_returning(self, mocker, fix_dir):
        m1 = mocker.patch(
            'pyentrez.user_cred.safe_open_file',
            return_value=self.safe_load(fix_dir / 'config' / 'core_config.yaml'),
        )
        bool1, pth = user_cred.get_usr_path()
        # Test that if username is in coreconfig that: Path and first_time=False are returned
        assert ((type(pth) is Path or WindowsPath or PosixPath) and not bool1)

    def test_user_path_new(self, mocker, mock_env_user, fix_dir):
        m1 = mocker.patch(
            'pyentrez.user_cred.safe_open_file',
            return_value=self.safe_load(fix_dir / 'config' / 'core_config.yaml'),
        )
        bool1, pth = user_cred.get_usr_path()
        # Test that a new user will return: first_time = True and Path = False
        assert (bool1 and not pth)

    def test_user_add(self, mocker, mock_env_user, tmpdir, fix_dir):
        m1 = mocker.patch(
            'pyentrez.user_cred.safe_open_file',
            return_value=self.safe_load(fix_dir / 'config' / 'core_config.yaml'))
        m2 = mocker.patch('pyentrez.user_cred.safe_write_file')
        user_cred.cfg_user_add(tmpdir)
        assert 'Test_User' in m2.call_args.args[1]['USER_CFG']
        #assert x==0

    def test_safe_open(self, fix_dir):
        assert user_cred.safe_open_file(fix_dir / 'config' / 'core_config.yaml') is not None

    def test_safe_write(self, fix_dir):
        out = user_cred.safe_write_file(fix_dir / 'dmp.txt', {'test': 'test'})
        assert (fix_dir / 'dmp.txt').exists()
        os.remove(fix_dir / 'dmp.txt')

    def test_makedirs(self, tmpdir, mocker):
        m1 = mocker.patch('pyentrez.user_cred.cfg_user_add')
        user_cred.makedirs(tmpdir)
        assert (tmpdir / 'settings').exists()
        assert (tmpdir / 'data').exists()
