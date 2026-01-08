# owencraft-weather

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.10.12+
- [OpenWeatherMap](https://openweathermap.org) Account and API Key
- Ubuntu 22.04.5 (this most likely works on other Linux distributions as well, but probably not Windows)
- MCRCON (https://github.com/Tiiffi/mcrcon)

## Installing

To install owencraft-weather, follow these steps:

1. Check out the repository on a machine with Python 3.10.12+ and MCRCON installed:
`git clone https://github.com/benowe1717/owencraft-weather`

2. Create a Python virtual environment in the repository's folder:
`python3 -m venv .venv`

3. Activate the virtual environment with:
`source .venv/bin/activate`

4. Install all requirements:
`python3 -m pip install -r requirements.txt`

## Using

To use owencraft-weather, follow these steps:
NOTE: Always have the virtual environment active! (see step #3 from ##Installing)

Run the program and provide a zip code:
`python3 main.py -z 01234`

If you need to provide a Country Code (US is the default):
`python3 main.py -z 01234 -c US`

## Contributing to owencraft-weather

To contribute to owencraft-weather, follow these steps:

1. Fork this repository
2. Create a branch: `git checkout -b <branch_name>`
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the Pull Request

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

- [@benowe1717](https://github.com/benowe1717)

## Contact

For help or support on this repository, follow these steps:

- [Create an issue](https://github.com/benowe1717/owencraft-weather/issues)

## License

This project uses the following license: GNU GPLv3.

## Sources

- https://github.com/scottydocs/README-template.md/blob/master/README.md
- https://choosealicense.com/
- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/
