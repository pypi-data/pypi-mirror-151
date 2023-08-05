"""
Subpackage containing most schemas for DNADNA config formats.

Some schemas (particularly for plugins) are defined/generated in the code.
These schemas can be referenced using the ``jsonschema-pyref`` package.
"""

from ..utils.plugins import _PluginSchemaResolver


plugins = _PluginSchemaResolver()
