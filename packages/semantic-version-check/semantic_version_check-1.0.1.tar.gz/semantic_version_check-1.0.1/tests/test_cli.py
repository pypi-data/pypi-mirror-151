import pytest


@pytest.fixture
def main():
    from semantic_version_check.cli import main

    return main


"""
Example:
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2
< 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0
"""


@pytest.mark.parametrize(
    'version',
    (
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
@pytest.mark.runner_setup(mix_stderr=False)
def test_correct_version(version, main, cli_runner):
    result = cli_runner.invoke(
        main,
        args=[version],
        catch_exceptions=False,
    )
    assert result.exit_code == 0


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
@pytest.mark.runner_setup(mix_stderr=False)
def test_incorrect_version(version, main, cli_runner):
    result = cli_runner.invoke(
        main,
        args=[version],
        catch_exceptions=False,
    )
    assert result.exit_code == 1
