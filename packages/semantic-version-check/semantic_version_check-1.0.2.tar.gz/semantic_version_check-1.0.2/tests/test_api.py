import pytest


@pytest.fixture
def version_check():
    from semantic_version_check import version_check

    return version_check


@pytest.fixture
def reg_missmath():
    from semantic_version_check.main import SemanticVersionFormatError

    return SemanticVersionFormatError


@pytest.fixture
def regex():
    from semantic_version_check import regex

    return regex


@pytest.mark.parametrize(
    'version',
    (
        '1.2.0',
        '1.0.0',
        '200.5.0',
        '0.5.0',
        '0.0.1',
        '1.0.0-alpha',
        '0.0.1-alpha.1',
        '3.1.5-alpha.beta',
        '1.34.6-beta.11',
        '1.0.0-alpha-beta',
        '1.0.0-alpha-beta-a-b',
        '1.0.0-alpha-beta.1.2.3-1-a-s',
        '1.34.6-beta.11-1',
        '2.0.12-rc.1',
    ),
)
def test_version_check(version, version_check):
    match_object = version_check(version)
    assert match_object is not None
    assert match_object.group(1)
    assert match_object.group(2)
    assert match_object.group(3)


@pytest.mark.parametrize(
    'version',
    (
        '1.0',
        '200',
        '1',
        '0.5',
        '1.0-alpha',
        '1.0.0.alpha',
        '0.1-alpha.1',
        '3-alpha.beta',
        '34.6-beta.11',
        '2.0.12.1-rc.1',
    ),
)
def test_wrong_version(version, version_check, regex, reg_missmath):
    import re

    with pytest.raises(
        reg_missmath,
        match="Regex '{regex}' did not match string '{string}'".format(
            regex=re.escape(regex.pattern), string=version
        ),
    ):
        version_check(version)
