"""Compatibility package for project-level imports.

The runtime application package lives under ``app``.
This namespace exists to satisfy packaging/install workflows that
expect an import package matching the normalized project name.
"""

__all__ = ["__version__"]
__version__ = "0.2.0"
