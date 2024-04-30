#!/usr/bin/env python3
import os.path
from unittest.mock import MagicMock, patch

import pytest

from src.classes.mcrcon import McRcon


class TestMcRcon():
    def setUp(self):
        self.file = '/usr/local/bin/mcrcon'
        self.hostname = 'localhost'
        self.creds_file = 'tests/data/.mcrcon'
        self.port = 25575
        self.mcrcon = McRcon(self.file, self.hostname, self.creds_file)

    def tearDown(self):
        del self.mcrcon
        del self.port
        del self.creds_file
        del self.hostname
        del self.file

    def test_file_exists_failed(self):
        self.setUp()
        file = '/tmp/mcrcon'
        result = self.mcrcon._file_exists(file)
        assert result is False
        self.tearDown()

    def test_file_exists(self):
        self.setUp()
        result = self.mcrcon._file_exists(self.file)
        assert result is True
        self.tearDown()

    def test_is_file_failed(self):
        self.setUp()
        file = '/tmp'
        result = self.mcrcon._is_file(file)
        assert result is False
        self.tearDown()

    def test_is_file(self):
        self.setUp()
        result = self.mcrcon._is_file(self.file)
        assert result is True
        self.tearDown()

    def test_is_readable_failed(self):
        self.setUp()
        file = '/swapfile'
        result = self.mcrcon._is_readable(file)
        assert result is False
        self.tearDown()

    def test_is_readable(self):
        self.setUp()
        result = self.mcrcon._is_readable(self.creds_file)
        assert result is True
        self.tearDown()

    def test_is_executable_failed(self):
        self.setUp()
        result = self.mcrcon._is_executable(self.creds_file)
        assert result is False
        self.tearDown()

    def test_is_executable(self):
        self.setUp()
        result = self.mcrcon._is_executable(self.file)
        assert result is True
        self.tearDown()

    def test_is_valid_hostname_failed(self):
        self.setUp()
        hostname = 'My Computer'
        result = self.mcrcon._is_valid_hostname(hostname)
        assert result is False
        self.tearDown()

    def test_is_valid_hostname(self):
        self.setUp()
        result = self.mcrcon._is_valid_hostname(self.hostname)
        assert result is True
        self.tearDown()

    def test_is_valid_port_failed(self):
        self.setUp()
        port = 5674328247561
        result = self.mcrcon._is_valid_port(port)
        assert result is False
        self.tearDown()

    def test_is_valid_port(self):
        self.setUp()
        result = self.mcrcon._is_valid_port(self.port)
        assert result is True
        self.tearDown()

    def test_get_mcrcon_file(self):
        self.setUp()
        filepath = os.path.abspath(self.file)
        assert self.mcrcon.mcrcon == filepath
        self.tearDown()

    def test_set_mcrcon_file_failed_not_found(self):
        self.setUp()
        file = '/tmp/mcrcon'
        with pytest.raises(ValueError):
            mcrcon = McRcon(file, self.hostname, self.creds_file)
            assert mcrcon.mcrcon is None
            assert mcrcon.hostname == self.hostname
            assert mcrcon.port == self.port
        self.tearDown()

    def test_set_mcrcon_file_failed_not_a_file(self):
        self.setUp()
        file = '/tmp'
        with pytest.raises(ValueError):
            mcrcon = McRcon(file, self.hostname, self.creds_file)
            assert mcrcon.mcrcon is None
            assert mcrcon.hostname == self.hostname
            assert mcrcon.port == self.port
        self.tearDown()

    def test_set_mcrcon_file_failed_not_executable(self):
        self.setUp()
        with pytest.raises(ValueError):
            mcrcon = McRcon(self.creds_file, self.hostname, self.creds_file)
            assert mcrcon.mcrcon is None
            assert mcrcon.hostname == self.hostname
            assert mcrcon.port == self.port
        self.tearDown()

    def test_get_hostname(self):
        self.setUp()
        assert self.mcrcon.hostname == self.hostname
        self.tearDown()

    def test_set_hostname_failed(self):
        self.setUp()
        hostname = 'REcycle Bin'
        with pytest.raises(ValueError):
            mcrcon = McRcon(self.file, hostname, self.creds_file)
            assert mcrcon.mcrcon == self.file
            assert mcrcon.hostname is None
        self.tearDown()

    def test_get_creds_file(self):
        self.setUp()
        filepath = os.path.abspath(self.creds_file)
        assert self.mcrcon.credentials_file == filepath
        self.tearDown()

    def test_set_creds_file_failed_not_found(self):
        self.setUp()
        file = '/tmp/mcrcon'
        with pytest.raises(ValueError):
            mcrcon = McRcon(self.file, self.hostname, file)
            assert mcrcon.mcrcon == self.file
            assert mcrcon.hostname == self.hostname
            assert mcrcon.credentials_file is None
        self.tearDown()

    def test_set_creds_file_failed_not_a_file(self):
        self.setUp()
        file = '/tmp'
        with pytest.raises(ValueError):
            mcrcon = McRcon(self.file, self.hostname, file)
            assert mcrcon.mcrcon == self.file
            assert mcrcon.hostname == self.hostname
            assert mcrcon.credentials_file is None
        self.tearDown()

    def test_set_creds_file_failed_not_readable(self):
        self.setUp()
        file = '/swapfile'
        with pytest.raises(ValueError):
            mcrcon = McRcon(self.file, self.hostname, file)
            assert mcrcon.mcrcon == self.file
            assert mcrcon.hostname == self.hostname
            assert mcrcon.credentials_file is None
        self.tearDown()

    def test_get_port(self):
        self.setUp()
        assert self.mcrcon.port == self.port
        self.tearDown()

    def test_set_port_failed(self):
        self.setUp()
        port = 123412341234
        filepath = os.path.abspath(self.creds_file)
        with pytest.raises(ValueError):
            mcrcon = McRcon(
                self.file,
                self.hostname,
                self.creds_file,
                port=port)
            assert mcrcon.mcrcon == self.file
            assert mcrcon.hostname == self.hostname
            assert mcrcon.credentials_file == filepath
            assert mcrcon.port is None
        self.tearDown()

    def test_set_port(self):
        self.setUp()
        port = 443
        filepath = os.path.abspath(self.creds_file)
        mcrcon = McRcon(
            self.file,
            self.hostname,
            self.creds_file,
            port=port)
        assert mcrcon.mcrcon == self.file
        assert mcrcon.hostname == self.hostname
        assert mcrcon.credentials_file == filepath
        assert mcrcon.port == port
        self.tearDown()

    def test_get_password(self):
        self.setUp()
        password = 'somePasswordGoeshere12!'
        assert self.mcrcon._password == password
        self.tearDown()

    @patch('src.classes.mcrcon.subprocess.run')
    def test_set_weather_failed_connection_refused(self, mock_run, capsys):
        self.setUp()
        msg = "Connection failed.\nError 111: Connection refused"
        mock_stdout = MagicMock()
        mock_stdout.configure_mock(
            **{'return_value': msg, 'returncode': 1, 'stderr': msg})
        mock_run.return_value = mock_stdout
        result = self.mcrcon.set_weather('clear')
        captured = capsys.readouterr()
        assert result is False
        assert mock_stdout.stderr == msg
        assert captured.out == f"{msg}\n"
        self.tearDown()

    @patch('src.classes.mcrcon.subprocess.run')
    def test_set_weather_failed_no_route_to_host(self, mock_run, capsys):
        self.setUp()
        msg = "Connection failed.\nError 113: No route to host"
        mock_stdout = MagicMock()
        mock_stdout.configure_mock(
            **{'return_value': msg, 'returncode': 1, 'stderr': msg})
        mock_run.return_value = mock_stdout
        result = self.mcrcon.set_weather('clear')
        captured = capsys.readouterr()
        assert result is False
        assert mock_stdout.stderr == msg
        assert captured.out == f"{msg}\n"
        self.tearDown()

    @patch('src.classes.mcrcon.subprocess.run')
    def test_set_weather_failed_bad_password(self, mock_run, capsys):
        self.setUp()
        msg = 'Authentication failed!'
        mock_stdout = MagicMock()
        mock_stdout.configure_mock(
            **{'return_value': msg, 'returncode': 1, 'stderr': msg})
        mock_run.return_value = mock_stdout
        result = self.mcrcon.set_weather('clear')
        captured = capsys.readouterr()
        assert result is False
        assert mock_stdout.stderr == msg
        assert captured.out == f"{msg}\n"
        self.tearDown()

    @patch('src.classes.mcrcon.subprocess.run')
    def test_set_weather(self, mock_run):
        self.setUp()
        action = 'clear'
        msg = f'Set the weather to {action}'
        mock_stdout = MagicMock()
        mock_stdout.configure_mock(
            **{'return_value': msg, 'returncode': 0, 'stdout': msg})
        mock_run.return_value = mock_stdout
        result = self.mcrcon.set_weather(action)
        assert result is True
        self.tearDown()
