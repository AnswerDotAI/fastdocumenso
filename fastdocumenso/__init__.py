"""Documenso v2 API client with pyskill for e-signature workflows

Modules:

- `fastdocumenso.core`: Async Documenso v2 API client built on fastspec
- `fastdocumenso.skill`: Send documents for e-signature via the Documenso v2 API — envelope, recipient, field, and audit operations as self-documenting async functions."""

__version__ = "0.2.0"
from .core import *

