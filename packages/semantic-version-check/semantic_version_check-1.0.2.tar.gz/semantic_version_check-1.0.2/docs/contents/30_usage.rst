=====
Usage
=====

------------
Installation
------------

| **semantic_version_check** is available on PyPI hence you can use `pip` to install it.

It is recommended to perform the installation in an isolated `python virtual environment` (env).
You can create and activate an `env` using any tool of your preference (ie `virtualenv`, `venv`, `pyenv`).

Assuming you have 'activated' a `python virtual environment`:

.. code-block:: shell

  python -m pip install semantic-version-check


---------------
Simple Use Case
---------------

| One Use Case for the semantic_version_check is to invoke its cli, through a console
| and do SemVer check on a single input string.

Open a console and run:
  
.. code-block:: shell

  check-semantic-version 1.0.0
  echo $?
  echo "Exit code is 0 meaning operation succeeded"

  check-semantic-version 1.3
  echo $?
  echo "Exit code is 1, meaning operation failed"

Note: this use case may be useful for a CI pipeline.
