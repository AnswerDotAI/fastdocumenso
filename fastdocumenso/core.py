"""Async Documenso v2 API client built on fastspec.

Create a client with `documenso_client()` and call generated operations:
`await cli.envelope.envelope_create(...)`, `await cli.document.document_get(...)`, etc.
"""
import os, json
from fastcore.utils import *
from fastspec.spec import SpecParser
from fastspec.oapi import OpenAPIClient

from fastdocumenso._spec import spec as _spec

__all__ = ['documenso_client']

def _encode_form(d):
    "Documenso multipart endpoints expect dict/list parts (e.g. `payload`) as JSON strings"
    return {k: json.dumps(v) if isinstance(v,(dict,list)) else v for k,v in d.items()}

def documenso_client(
    api_key:str|None=None,  # Documenso API token; defaults to $DOCUMENSO_API_KEY
    base_url:str|None=None, # defaults to $DOCUMENSO_API_URL or the documenso.com cloud
)->OpenAPIClient:           # groups as attributes, ops as awaitable methods
    "Async Documenso v2 API client"
    spec = SpecParser.from_dict(_spec)
    spec.base_url = base_url or os.environ.get('DOCUMENSO_API_URL', spec.base_url)
    return OpenAPIClient(spec, headers={'Authorization': api_key or os.environ['DOCUMENSO_API_KEY']}, form_encoder=_encode_form)
