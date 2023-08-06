# python-ngramratio

A method for similarity scoring of two strings.

The method, namely `nratio`, belongs to the class `SequenceMatcherExtended`, which is an extension of the `SequenceMatcher` class of the [difflib package](https://docs.python.org/3/library/difflib.html). In particular, `nratio` (method of `SequenceMatcherExtended`) is an augmenation of `ratio` (method of `SequenceMatcher`).

`ngramratio` is to be pronounced as "n gram ratio". The library uses n-grams to find a similarity score via a division (ratio) of the number of matched characters by the total number of characters. See below for more details.

## Motivation

To compute a similarity score based on matching n-grams (with n>=1 chosen by the user) rather than matching single characters (as in the case of the `ratio` method).

## Installation

To install the Python library run:

    pip install ngramratio

The library will be installed as `ngramratio` to `bin` on
Linux (e.g. `/usr/bin`); or as `ngramratio.exe` to `Scripts` in your
Python installation on Windows (e.g.
`C:\Python27\Scripts\ngramratio.exe`).

You may consider installing the library only for the current user:

    pip install ngramratio --user

In this case the library will be installed to
`~/.local/bin/ngramratio` on Linux and to
`%APPDATA%\Python\Scripts\ngramratio.exe` on Windows.

## Library usage

The module provides a method, `nratio`, which takes an integer number (the user's required minimum n-gram length, i.e. number of consecutive characters, to be matched) and outputs a similarity index (float number in [0,1]).

### **First step**: initialize an object of class SequenceMatcherExtended specifying the two strings to be compared:

```
    >>> from ngramratio import ngramratio

    >>> SequenceMatcherExtended = ngrmaratio.SequenceMatcherExtended

    >>> a = "ab cde" # string 1
    >>> b = "bcde"   # string 2

    >>> s = SequenceMatcherExtended(a, b)
```

**Alternatively**, the last line can be rewritten more generally as

```
    >>> s = SequenceMatcherExtended(None, a, b, None)
```

where the first and last arguments are used to specify that no string will be considered junk. For more information on these arguments, see the documentation of the original [difflib package](https://docs.python.org/3/library/difflib.html).

### **Second step**: apply the `ratio` and `nratio` methods and compare similarity scores:

```
    >>> s.ratio()
    >>> # Matches any character. Matches: "b" (length 1), "cde"(length 3). Score: (3+1)*2/10.
    0.8
    >>> s.nratio(1)
    >>> # Matches substring of length 1 or more. It replicates `ratio()`'s functionality.
    0.8
    >>> s.nratio(2)
    >>> # Matches substring of length 2 or more. Matches: "cde"(length 3). Score: 3*2/10.
    0.6
    >>> s.nratio(3)
    >>> # Matches substring of length 3 or more. Matches: "cde"(length 3). Score: 3*2/10.
    0.6
    >>> s.nratio(4)
    >>> # Matches substring of length 4 or more. Score 0/10.
    0.0
```

The similarity score is computed as `the number of characters matched` (m) mutiplied by `two` (2) and divided by `the total numer of characters` (T) of the two strings, i.e. similarity score = 2m/T. Note that Python always returns a float upon computing a division.

## Testing in a virtual environment

This project uses [pytest](https://docs.pytest.org/) testing
framework with [tox](https://tox.readthedocs.io/) and [docker](https://docs.docker.com/language/) to automate testing in
different python environments. Tests are stored in the `test/`
folder.

To test a specific python version, for example version 3.6, edit the last few characters of the `startTest.sh` script to **py36** AND change the image to python 3.6 on line 4 of the `docker-compose.yaml` file.

To run tests, run `bash _scripts/startTest.sh`. This will start a docker container using the specified python image. After testing, or before testing a different python version, run `bash _scripts/teardown.sh` to remove the docker container.

The library has been tested successfully for python >= 3.6.

## Testing on your local machine with no v.e.

You can use `tox` directly in your local machine. Make sure to install `tox`, `pytest` before testing.

On Linux `tox` expects to find executables like `python3.6`, `python3.10` etc. On Windows it looks for
`C:\Python36\python.exe` and
`C:\Python310\python.exe` respectively.

To test a specific Python environment, use the `-e` option. For example, to
test against Python 3.7 run:

    tox -e py37

in the root of the project source tree.

To fix code formatting (this will install `pre-commit` as a dependency), run:

    tox -e lint

See the `tox.ini` file in the repository to learn more about the testing instructions being used.

## Contributions

Contributions should include tests and an explanation for the changes
they propose. Documentation (examples, docstrings, README.md) should be
updated accordingly.
