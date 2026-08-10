"""Async Documenso v2 API client built on fastspec.

Create a client with `documenso_client()` and call generated operations:
`await cli.envelope.envelope_create(...)`, `await cli.document.document_get(...)`, etc.
"""
import os, json
from fastcore.utils import *
from fastspec.spec import SpecParser
from fastspec.oapi import OpenAPIClient, OpGroup, OpFunc

from fastdocumenso._spec import spec as _spec

_ALLOWED_OPS = {
    'envelope_create', 'envelope_get', 'envelope_recipient_create_many',
    'envelope_field_create_many', 'envelope_distribute', 'envelope_item_download',
    'envelope_audit_log_find', 'document_find', 'document_get',
}
__all__ = ['documenso_client', 'documenso_spec']

def documenso_spec()->SpecParser:
    "Documenso v2 API spec snapshot"
    spec = SpecParser.from_dict(_spec)
    spec.ops = [o for o in spec.ops if o.name in _ALLOWED_OPS]
    return spec

def _encode_form(d):
    "Documenso multipart endpoints expect dict/list parts (e.g. `payload`) as JSON strings"
    return {k: json.dumps(v) if isinstance(v,(dict,list)) else v for k,v in d.items()}

def documenso_client(
    api_key:str|None=None,  # Documenso API token; defaults to $DOCUMENSO_API_KEY
    base_url:str|None=None, # defaults to $DOCUMENSO_API_URL or the documenso.com cloud
)->OpenAPIClient:           # groups as attributes, ops as awaitable methods
    "Async Documenso v2 API client"
    spec = documenso_spec()
    spec.base_url = base_url or os.environ.get('DOCUMENSO_API_URL', spec.base_url)
    return OpenAPIClient(spec, headers={'Authorization': api_key or os.environ['DOCUMENSO_API_KEY']}, form_encoder=_encode_form)
