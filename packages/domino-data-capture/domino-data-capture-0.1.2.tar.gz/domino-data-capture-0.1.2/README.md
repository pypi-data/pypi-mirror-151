# Domino Data Capture
Domino Data capture repository which captures user provided prediction data

# How to install
This python package is hosted in `pypi`. Use command `pip install domino-data-capture` to install.


# How to use
Please refer to `library_usage.py` for a complete usage example

## 🛡 License

[![License](https://img.shields.io/github/license/cerebrotech/data-access-sdk)](https://github.com/cerebrotech/dmm-data-ingest-client/blob/master/LICENSE.txt)

This project is licensed under the terms of the `Apache Software License 2.0` license. See [LICENSE](https://github.com/cerebrotech/dmm-data-ingest-client/blob/master/LICENSE.txt) for more details.

# Important make rules
Here are the available make rules that will help you in easing your development work
```shell

make install-poetry      -> Installs poetry
make poetry-remove       -> Uninstalls poetry
make install             -> Installs poetry dependencies
make pre-commit-install  -> Install pre commit hooks
make codestyle           -> Runs codestyle check with black and isort
make formatting          -> Runs codestyle
make test                -> Runs tests
make check-codestyle     -> Checks codestyle
make check-safety        -> Checks safety and generates full report
make lint                -> Runs linting check with black
make build               -> Builds python artifacts
make publish             -> Publishes atrifacts to pypi
``` 

# Build and Release process

Build and Release happens through poetry. Refer to the below commands.

```shell
poetry build            -> Builds artefacts
poetry publish          -> Publishes artefacts to pypi
```

# Support policy
  * For support policy please refer to the [readme.txt](readme.txt) present in this repo.