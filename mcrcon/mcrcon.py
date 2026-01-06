#!/usr/bin/env python3
"""
Mcrcon() class file

Mcrcon() is a class that wraps around the mcrcon binary to interact with
Minecraft's Remote Console feature.
"""
import os
import re
import subprocess
import sys
from typing import Any


class Mcrcon():
    """
    Mcrcon() class file

    Mcrcon() is a class that wraps around the mcrcon binary to interact with
    Minecraft's Remote Console feature.
    """

    def __init__(self) -> None:
        self._hostname = os.getenv('MCRCON_HOST')
        self._password = os.getenv('MCRCON_PASS')

        if not self.hostname:
            print('MCRCON_HOST unset!')
            sys.exit(1)

        if not self.password:
            print('MCRCON_PASS unset!')
            sys.exit(1)

    @property
    def hostname(self) -> str | None:
        """
        Getter for the hostname property

        The hostname is the target Minecraft server, which is likely just
        localhost or 127.0.0.1, though it can be any hostname or IP Address

        Args:
            None

        Returns:
            Either the hostname or IP Address in string format, or None if
            the MCRCON_HOST environment variable is not set.

        Raises:
            None
        """
        return self._hostname

    @property
    def password(self) -> str | None:
        """
        Getter for the password property

        The password is the remote console password defined in the Minecraft
        server's server.properties file.

        Args:
            None

        Returns:
            Either the password in string format, or None if the MCRCON_PASS
            environment variable si not set.

        Raises:
            None
        """
        return self._password

    def _ansi_decode(self, output: str) -> str:
        """
        Strip all ANSI characters from the output

        All MCRCON packets have ANSI characters in them. This method
        strips out all of those characters by doing a find and replace.

        Args:
            output: The direct output from the self._run_command() method

        Returns:
            A string with all ANSI characters stripped from the output

        Raises:
            None
        """
        pattern = r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]'
        return re.sub(pattern, '', output)

    def _mcrcon_strip(self, output: str) -> str:
        """
        Remove lines of data when using MCRCON from multiple sources

        When using MCRCON from multiple sources, the output from MCRCON
        gets combined all into a single stream. So this strips out
        all the possible lines that aren't relevant.

        Args:
            output: The direct output from the self._run_command() method

        Returns:
            A string with all configured lines and characters stripped from
            the output

        Raises:
            None
        """
        lines: list[str] = [
            'Automatic saving is now disabled',
            'Automatic saving is now enabled',
            'Saved the game'
        ]
        for line in lines:
            output = output.replace(line, '')

        return output

    def _run_command(self, cmd: str) -> list[str]:
        """
        Run an MCRCON command and return the output

        This method runs a command against the configured MCRCON target,
        strips out all of the ANSI characters, and any irrelevant lines of
        data, and returns the output as a list of strings.

        Args:
            cmd: The command you want to run

        Returns:
            A list of strings where each string in the list is a line of
            output from the command

        Raises:
            ValueError when the command fails to run
        """
        if not self.password:
            raise ValueError('MCRCON_PASS is unset!')

        command: list[str] = [
            '/usr/local/bin/mcrcon', '-p', self.password, cmd
        ]
        try:
            output: subprocess.CompletedProcess = subprocess.run(
                command, capture_output=True, check=True
            )
            if output.returncode > 0:
                raise ValueError(f'[WARN] {output.stderr.decode()}')

            data: str = self._ansi_decode(output.stdout.decode())
            data = self._mcrcon_strip(data)

            return data.splitlines()

        except subprocess.CalledProcessError as err:
            stdout: list[str] = err.stdout.decode().splitlines()
            stderr: list[str] = err.stderr.decode().splitlines()

            msg: list[str] = ['[ERROR]', ''.join(stdout)]
            if len(stderr) > 0:
                msg.append('::')
                msg.append(''.join(stderr))

            raise ValueError(' '.join(msg)) from err

    def get_count_of_players_online(self) -> str:
        """
        Get the count of logged in players

        This method returns the total number of players online as found
        from the `list` MCRCON command.

        Args:
            None

        Returns:
            The total number of online players in string format

        Raises:
            None
        """
        try:
            output: list[str] = self._run_command('list')
            pattern: str = r'^.*?are\s+(\d+)\s+of\s+a\s+max'
            match = re.match(pattern, output[0])
            if not match:
                return '0'

            return match.group(1)

        except ValueError as err:
            print(err)
            sys.exit(1)

    def get_online_players(
            self, players: list[dict[str, str]]) -> list[dict[str, Any]]:
        """
        Get the names of players who are logged in

        This method returns which players are online and offline as found
        from the `list` MCRCON command.

        Args:
            players: A list of dictionaries containing the player names
            from the whitelist

        Returns:
            A list of dictionaries where each dictionary is a player and
            their online status, like this:
            {
                'player': playername1234,
                'count': 0 # 0 if offline, 1 if online
            }

        Raises:
            None
        """
        logged_in_players: list[dict[str, Any]] = []

        for player in players:
            for key, value in player.items():
                if key == 'name':
                    logged_in: dict[str, Any] = {
                        'player': value,
                        'count': 0
                    }
                    logged_in_players.append(logged_in)

        pattern: str = r'^.*?online\:\s+([A-z0-9\,\s]+)'
        try:
            output: list[str] = self._run_command('list')
            matches = re.match(pattern, output[0])
            if not matches:
                return logged_in_players

            for player in matches.group(1).split(','):
                name: str = player.strip()
                for logged_in in logged_in_players:
                    if logged_in['player'] == name:
                        logged_in['count'] = 1

        except ValueError as err:
            print(err)

        return logged_in_players
