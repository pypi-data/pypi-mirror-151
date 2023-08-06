import sys

import click

from semantic_version_check.main import SemanticVersionFormatError, version_check


@click.command()
@click.argument('version')
def main(version):

    try:
        version_check(version)
    except SemanticVersionFormatError:
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
