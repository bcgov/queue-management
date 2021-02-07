
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](../LICENSE)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=bcgov_sbc-pay&metric=alert_status)](https://sonarcloud.io/code?id=bcgov_sbc-pay&selected=bcgov_sbc-pay%3Areport-api)
[![codecov](https://codecov.io/gh/bcgov/sbc-pay/branch/development/graph/badge.svg?flag=reportapi)](https://codecov.io/gh/bcgov/sbc-pay/tree/development/report-api)

# REPORT API

BC Registries report service.


## Development Environment

Follow the instructions of the [Development Readme](https://github.com/bcgov/entity/blob/master/docs/development.md)
to setup your local development environment.

## Development Setup

1. Follow the [instructions](https://github.com/bcgov/entity/blob/master/docs/setup-forking-workflow.md) to checkout the project from GitHub.
2. Open the pay-api directory in VS Code to treat it as a project (or WSL projec). To prevent version clashes, set up a
virtual environment to install the Python packages used by this project.
3. Run `make setup` to set up the virtual environment and install libraries.
4. Next run `pip install .` to set up the environment for running tests.

You also need to set up the variables used for environment-specific settings:
1. Copy the [dotenv template file](./docs/dotenv_template) to somewhere above the source code and rename to `.env`. You will need to fill in missing values.

## Running REPORT-API

1. Build the service by `docker build --tag reportservice`.
2. Run the docker `docker run -p 5000:5000 reportservice`.
3. Get into the docker `docker run -it  reportservice sh`.
4. View the [OpenAPI Docs](http://127.0.0.1:5000/api/v1).

## Running Liniting

1. Run `make flake8` or `flake8 src/report_api tests`.
2. Run `make pylint` or `pylint --rcfile=setup.cfg --disable=C0301,W0511 src/report_api test`

## Running Unit Tests

1. Tests are run from the Status bar at the bottom of the workbench in VS Code or `pytest` command.
2. Next run `make coverage` to generate the coverage report, which appears in the *htmlcov* directory.

## Openshift Environment

View the [document](https://github.com/bcgov/sbc-auth/blob/development/docs/build-deploy.md).

