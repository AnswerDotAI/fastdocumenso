#!/usr/bin/env python
import httpx, pathlib
from dataclasses import replace
from fastcore.utils import dict2obj
from fastspec.spec import SpecParser

SPEC_URL = 'https://app.documenso.com/api/v2/openapi.json'
OUT = pathlib.Path(__file__).parent.parent / 'fastdocumenso' / '_spec.py'

raw = httpx.get(SPEC_URL, follow_redirects=True).raise_for_status().json()
parser = SpecParser.from_openapi(dict2obj(raw))

# Documenso's spec uses empty item schemas for file uploads (not the standard `format: binary`),
# so we patch file_params in manually here
_FILE_OPS = {'envelope_item_create_many': 'files', 'envelope_create': 'files', 'envelope_use': 'files',
             'document_create': 'file', 'template_create_template': 'file'}
parser.ops = [replace(o, file_params=[_FILE_OPS[o.name]]) if o.name in _FILE_OPS else o for o in parser.ops]
parser.save(OUT)
print(f"Saved {len(parser.ops)} ops to {OUT}")

