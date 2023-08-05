#!/usr/bin/env python
"""
A minimal ``setup.py`` is still required when using setuptools.

See ``setup.cfg`` for package configuration.
"""

from setuptools import setup
from setuptools_scm import get_version

version = get_version(
    write_to='dnadna/_version.py',
    local_scheme='node-and-timestamp'
)

# Passing version here is necessary for conda/meta.yaml to read the version
# properly; this is sort of an anti-pattern but it shouldn't affect PEP
# 517-compatible builds
setup(version=version)
