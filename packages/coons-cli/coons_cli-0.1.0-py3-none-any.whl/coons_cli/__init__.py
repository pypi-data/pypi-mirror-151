from importlib import metadata
from .cli import cli

version = metadata.version(__package__)
__all__ = [version, cli]