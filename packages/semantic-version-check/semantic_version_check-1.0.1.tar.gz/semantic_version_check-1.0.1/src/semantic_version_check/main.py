import re
from typing import Callable, Match, Pattern

regex = re.compile(
    r'^(?P<major>0|[1-9]\d*)'
    r'\.'
    r'(?P<minor>0|[1-9]\d*)'
    r'\.'
    r'(?P<patch>0|[1-9]\d*)'
    r'(?:-'
    r'(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+'
    r'(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)


class RegExMatcher:
    @staticmethod
    def match(regex: Pattern, string: str) -> Match:
        match_result = regex.match(string)
        if not match_result:
            raise SemanticVersionFormatError(
                "Regex '{regex}' did not match string '{string}'".format(
                    regex=regex.pattern, string=string
                )
            )
        return match_result


# Simple Adapter
class VersionCheck:
    def __init__(self, regex_matcher: Callable[[Pattern, str], Match]):
        self._regex_matcher = regex_matcher

    def __call__(self, string):
        return self._regex_matcher(regex, string)


class SemanticVersionFormatError(Exception):
    pass


# Simple callable
version_check = VersionCheck(RegExMatcher.match)
