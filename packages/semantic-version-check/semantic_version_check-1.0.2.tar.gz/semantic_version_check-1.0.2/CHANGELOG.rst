=========
Changelog
=========

1.0.2 (2022-05-18)
==================

Changes
^^^^^^^

documentation
"""""""""""""
- fix cli usage guide


1.0.1 (2022-05-18)
==================

Changes
^^^^^^^

fix
"""
- readme


1.0.0 (2022-05-18)
==================

This is first fully featured and stable version of the `semantic_version_check` Python Package.

It features the `check-semantic-version` cli, suitable for quick invocation through a console or running on a CI service.
It also features the installable `semantic_version_check` python module (aka package or library)
that provides the `check` as python code.

Changes
^^^^^^^

feature
"""""""
- check a string's to verify if it matches the Semantic Version format


0.0.1 (2022-05-18)
==================

| This is the first ever release of the **semantic_version_check** Python Package.
| The package is open source and is part of the **semantic-version-checker** Project.
| The project is hosted in a public repository on github at https://github.com/boromir674/semantic-version-check
| The project was scaffolded using the `Cookiecutter Python Package`_ (cookiecutter) Template at https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

| Scaffolding included:

- **CI Pipeline** running on Github Actions at https://github.com/boromir674/semantic-version-check/actions
  - `Test Workflow` running a multi-factor **Build Matrix** spanning different `platform`'s and `python version`'s
    1. Platforms: `ubuntu-latest`, `macos-latest`
    2. Python Interpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`

- Automated **Test Suite** with parallel Test execution across multiple cpus.
  - Code Coverage
- **Automation** in a 'make' like fashion, using **tox**
  - Seamless `Lint`, `Type Check`, `Build` and `Deploy` *operations*


.. LINKS

.. _Cookiecutter Python Package: https://python-package-generator.readthedocs.io/en/master/
