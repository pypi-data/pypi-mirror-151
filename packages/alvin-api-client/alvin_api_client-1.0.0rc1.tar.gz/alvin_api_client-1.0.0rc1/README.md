# alvin-api-client

## Release process and development guide 

Similar to the `alvin_cli` we are following semantic commits and proper workflow for development. The docs for that can be found [here](.github/docs/README.md).

In most of the cases if you are not doing any code changes to the `alvin-api-client` directly, you just mainly have to focus on running the script under `./scripts/generate-code` to 
generate the latest version of `api-client` pulling all the updates and changes from the backend. Based on the pull request and commits defined in the [docs](.github/docs/README.md) the 
updated version would be released on PyPi. 


The `api-client` code is an internal development and is not meant for public release for now. 


## Internal Documentation

This is a python client to the Alvin API.

It has been automatically generated using the [Openapi Generator](https://github.com/openapitools/openapi-generator).

- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Development 

### Code Generation

Primarily, we automatically generate the `production` client code based on the API specifications
All production code resides in the `src` directory.

The `test` code is maintained and developed, by writing code!
All test code resides in the `tests` directory.

We generate the python client package by running the `generate-code` script.

For example, if there are changes to the Alvin API specifications, then we can (git) `commit` to
an updated client code, by re-running the `generate-code` script.

The `generate-code` script resides in the `scripts` directory along with the `gen-openapi-config.yaml` file, which holds configuration settings controlling the generation process.

Please be mindful that you may need to manually configure generator with the desired version (eg 1.0.0) for the api client package, by changing value of the `packageVersion` setting in the `gen-openapi-config.yaml` file.

### Operations

For python development operations (such as running unit tests, deploying to pypi, etc) we are
using the `tox` automation tool, exposed through the `tox` cli.

Please install with `pip install --user tox`

Tox allows running arbitrary python commands, against various python interpreters, on automatically created virtual environments using a declarative configuration file.
It can also serve as "frontend" between local and remote CI execution.

You can see what commands do execute in which environments we defined in ourhe tox.ini file.

Following, we showcase a few usefull tox commands in the cli.

To see all available tox environments:
```sh
tox -av
```

To run the default sequence of tox environments:
```sh
tox
```

To run the dev-test environment:
```sh
tox -e dev-test
```

## Testing

Currently, an Alvin API service is expected to be served on localhost, for the test suite to run.

The test suite is currently configured to look for the actual API service on localhost port 8000.

Ideally, we would like every endpoint to be covered with at least one test case (input data, arguments, expected data, assertion checks).

### running unit-tests while doing development

We want to have a dedicated `dev` environment with all necessary dependencies installed,
where our source code also gets installed and tested.

We achieve that by running:
```sh
tox -e dev-test -vv
```

We could also do the same and measure code coverage statistics by running:
```sh
tox -e dev-test-cov -vv
```

Note that the package is installed in edit mode (as in `pip install -e`) to avoid re-building, everytime we make a change in the code. In otherwords, in the `dev-test`
environment the changes made locally in the code are reflected immediately in the environment.

Thus subsequent executions of `tox -e dev-test` shall not trigger `pip install`!

Also note that the `python3` binary will be used found in PATH, unless you want to override
it using the TOXPYTHON environment variable (ie `TOXPYTHON=python3.9 tox -e dev-test`).

For more on `tox` see the [docs](https://tox.wiki/en/latest/).


## Deploy to pypi

For deploying to a pypi index server, you can use a series
of tox environments to check, build and then deploy the wheel/source distributions (build output).

We need the `ALVIN_API_CLIENT_VERSION` environment variable for specifying the release version.

### Deploy to pypi.org

You can use `tox` to automate the process of deploying a python package to pypi.org index server.

Example code for deploying version 0.5.0 to pypi.org:
```sh
export ALVIN_API_CLIENT_VERSION=0.5.0
export TWINE_USERNAME=<username>
export TWINE_PASSWORD=<password>

PYPI_SERVER=pypi tox -e check,build,deploy
```

### Deploy to test-pypi

In case you want to use the test-pypi as a "staging" server, you can use the default behaviour.

Example code for deploying version 0.5.0 to test-pypi:
```sh
export ALVIN_API_CLIENT_VERSION=0.5.0
export TWINE_USERNAME=<username>
export TWINE_PASSWORD=<password>

tox -e check,build,deploy
```


## Requirements.

Python >= 3.6

## Installation & Usage

This package when available through pypi should be installed as follows:

```sh
pip install alvin-api-client
```

(of course for development purposes it should be installed in an appropriate virtual environment, otherwise you may need to run `pip` for the `user` with `pip install --user`, or with root permission with `sudo pip install`)

You can then import the package as follows:
```python
import alvin_api_client
```


## Getting Started

One example to invoke the GET method of the "client-config" endpoint:

```python
from pprint import pprint
from alvin_api_client import ApiClient, Configuration
from alvin_api_client.api.default_api import DefaultApi

with ApiClient(Configuration(host='http://localhost:8080')) as api_client:
    api_instance = DefaultApi(api_client)
    response = api_instance.get_client_config_api_v1_client_config_get()
    pprint(response)
```



## Notes for Large OpenAPI documents
If the OpenAPI document is large, imports in alvin_api_client.apis and alvin_api_client.models may fail with a
RecursionError indicating the maximum recursion limit has been exceeded. In that case, there are a couple of solutions:

Solution 1:
Use specific imports for apis and models like:
- `from alvin_api_client.api.default_api import DefaultApi`
- `from alvin_api_client.model.pet import Pet`

Solution 2:
Before importing the package, adjust the maximum recursion limit as shown below:
```
import sys
sys.setrecursionlimit(1500)
import alvin_api_client
from alvin_api_client.apis import *
from alvin_api_client.models import *
```
Note: these notes have been generated by OpenApiGenerator