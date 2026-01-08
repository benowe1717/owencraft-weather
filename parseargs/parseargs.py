#!/usr/bin/env python3
"""
ParseArgs() class file

ParseArgs() is a class that wraps around the argparse library to accept
and handle command line parameters.
"""
import argparse


class ParseArgs():
    """
    ParseArgs() class file

    ParseArgs() is a class that wraps around the argparse library to accept
    and handle command line parameters.
    """

    def __init__(self, args: list[str]) -> None:
        self._args = args
        self._zipcode = 0
        self._country_code = 'US'

        self._parser = self._create_parser()
        self._parse_args: argparse.Namespace = self.parser.parse_args(
            self.args
        )
        self._handle_args()

    @property
    def args(self) -> list[str]:
        """
        Getter for the args property

        This is a list of strings where each item in the list is an argument
        passed to the program at execution.

        Args:
            None

        Returns:
            A list of strings where each item in the list is an argument
            passed to the program at execution

        Raises:
            None
        """
        return self._args

    @property
    def zipcode(self) -> int:
        """
        Getter for the format property

        This determines which format the program will output to.

        Args:
            None

        Returns:
            The zipcode to check the weather in.

        Raises:
            None
        """
        return self._zipcode

    @property
    def country_code(self) -> str:
        """
        Getter for the format property

        This determines which format the program will output to.

        Args:
            None

        Returns:
            The two letter country code that the zipcode resides in.

        Raises:
            None
        """
        return self._country_code

    @property
    def parser(self) -> argparse.ArgumentParser:
        """
        Getter for the parser property

        This is the ArgumentParser object for the running instance of this
        class.

        Args:
            None

        Returns:
            The ArgumentParser object

        Raises:
            None
        """
        return self._parser

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the Argument Parser with all required arguments

        This method creates the ArgumentParser object and adds all of the
        required and optional command line parameters that this program will
        accept. It also sets the self.parser property.

        Args:
            None

        Returns:
            An instance of the ArgumentParser object

        Raises:
            None
        """
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog='main.py',
            description='Control the weather on a Minecraft Server'
        )

        # -z/--zipcode
        parser.add_argument(
            '-z',
            '--zipcode',
            nargs=1,
            required=False,
            help='The zipcode to check the weather in'
        )

        # -c/--country-code
        parser.add_argument(
            '-c',
            '--country-code',
            nargs=1,
            required=False,
            help='The two letter country code that the zipcode resides in'
        )

        # -v/--version
        parser.add_argument(
            '-v',
            '--version',
            action='store_true',
            required=False,
            help="Show this program's current version"
        )

        return parser

    def _handle_args(self) -> None:
        """
        Handle all passed arguments

        This method handles all of the parameters that are passed to the
        program by validating if they are correct and taking the appropriate
        action.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        # Print out the version information
        if self._parse_args.version:
            self._print_version()
            self.parser.exit()

        # Set the zipcode
        if self._parse_args.zipcode:
            try:
                self._zipcode = int(self._parse_args.zipcode[0].strip())
            except ValueError:
                self.parser.error('Invalid zipcode given!')

        else:
            self.parser.error('Zipcode is required!')

        # If the country code is given, set it
        if self._parse_args.country_code:
            self._country_code = self._parse_args.country_code[0].strip(
            ).upper()

    def _print_version(self) -> None:
        """
        Prints out the warranty and version number of the program

        This method is used to print out the version and warranty information
        for this program. It is used in -v/--version parameter.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        print('owencraft-weather v0.1.0')
        print(
            'This is free software:',
            'you are free to change and redistribute it.')
        print('There is NO WARARNTY, to the extent permitted by law.')
        print('Written by Benjamin Owen; see below for original code')
        print('<https://github.com/benowe1717/owencraft-weather>')
