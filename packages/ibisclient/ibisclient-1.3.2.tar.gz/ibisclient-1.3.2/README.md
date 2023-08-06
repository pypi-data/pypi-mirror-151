# Ibis (Lookup) Client Libraries

> ⚠ **The Python 2 Ibis (Lookup) Client Library is now deprecated, please move to use the provided
Python 3 Library instead.**

This repository contains the source to create and build Python 2, Python 3, Java, and PHP Ibis
(Lookup) client libraries.

You need to have Docker and Docker Compose installed to build and/or test the Ibis (Lookup) client
libraries.

## Getting started

Before attempting to build the deliverable or run tests locally, copy `secrets.env.in` to
`secrets.env` and replace the placeholder values with the correct secrets. The secrets to use
depend on whether you're running inside or outside of the CUDN. The intended way to run the tests
is with both anonymous and non-anonymous users inside the CUDN, which is what the test job in the
CI/CD pipeline should be configured for.

## Building the libraries

To build the libraries locally, run:

```sh
./build.sh
```

The output will go to the `build`, `download` and `src` directories.

See `build.xml` for targets.

## Testing the libraries

To test the libraries locally (lint and unit tests), run:

```sh
./test.sh
```

Any command line arguments are passed to the test automator (tox). For example, to run only the
unit tests:

```sh
./test.sh -e py3
```

Use `--` to pass arguments to pytest. For example, to prevent collection of output (dump straight
to the terminal) whilst retaining the default arguments:

```sh
./test.sh -- -s ./src/python3/test/unittests.py
```

## Bootstrapping the CI/CD configuration

When setting the CI/CD pipeline to run the unit tests, the following environment variables must
be defined as secrets for the CI/CD test job:

```
LOOKUP_TEST_SERVER_EDITOR_USERNAME
LOOKUP_TEST_SERVER_EDITOR_PASSWORD
```

When running on Cambridge University's GitLab runners, the values should be set for the tests to
be run inside the CUDN (which they will be). See `secrets.env.in` for more details.

## Making a release

To make a release, the source code changes and the locally built libraries should be committed to
a branch and a related merge request raised for review of the changes.

After the merge request is merged, publish the Ibis (Lookup) client library for Python to PyPi by
manually triggering the `pypi-release` job in the build pipeline of the master branch. All of the
built libraries are automatically published by the
[Lookup/Ibis web service API page](https://www.lookup.cam.ac.uk/doc/ws-doc/)
which links to the builds in the master branch of this repository.
