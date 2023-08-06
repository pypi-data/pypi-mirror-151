=================
Why this Package?
=================

So, why would one opt for this Package?

It is useful in automation scenarios, since it can be run through
its cli (eg using a `bash` shell) and "exits" with 0 or 1 accordingly.

It is useful whenever you are writing python and want to have a single source of truth
for parsing and checking a string according to Semantic Version.

Specifically, the package exposes a regular expression
(`from semantic_version_check import regex`) that can serve as a single source of truth
to your python projects, whenever you need to do some SemVer parsing of string.

Also, it is easy to *install* using `pip`.

Finally, the package is well-tested against multiple
Python Interpreter versions (from 3.6 to 3.10),
tested on both *Linux* (Ubuntu) and *Darwin* (Macos) platforms.

This package's releases follow **Semantic Versioning** too :)
