# -*- coding: utf-8 -*-
"""Allow executing through `python -m semantic_version_check`.

Allow Semantic Version Check to be executable through
`python -m semantic_version_check`.
"""
from __future__ import absolute_import

from semantic_version_check.cli import main

if __name__ == "__main__":  # pragma: no cover
    main(prog_name='semantic-version-check')
