# Don't manually change, let poetry-dynamic-versioning-plugin handle it.
__version__ = "0.2.1"

from abc import abstractmethod

from .config import InvalidNameError, RegistryConfig
from .registry import Registry, RegistryDecorator, RegistryMeta
