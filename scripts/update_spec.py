#!/usr/bin/env python
import httpx, pathlib, pprint
from dataclasses import replace, asdict, fields
from dataclasses import replace
from fastcore.utils import dict2obj
from fastspec.spec import SpecParser
from pathlib import Path

SPEC_URL = 'https://app.documenso.com/api/v2/openapi.json'
OUT = pathlib.Path(__file__).parent.parent / 'fastdocumenso' / '_spec.py'

raw = httpx.get(SPEC_URL, follow_redirects=True).raise_for_status().json()
parser = SpecParser.from_openapi(dict2obj(raw))

# Manually add files to file_params because fastspec ignores that
_FILE_OPS = {'envelope_item_create_many': 'files', 'envelope_create': 'files', 'envelope_use': 'files',
             'document_create': 'file', 'template_create_template': 'file'}
parser.ops = [replace(o, file_params=[_FILE_OPS[o.name]]) if o.name in _FILE_OPS else o for o in parser.ops]
def _to_dict(self):
    def _op(o):
        d = {k:v for k,v in asdict(o).items() if v}
        if 'param_types' in d: d['param_types'] = {k:t.__name__ for k,t in d['param_types'].items() if t}
        return d
    return dict(base_url=self.base_url, ops=[_op(o) for o in self.ops])
SpecParser.to_dict = _to_dict
def _save(self, path):
    txt = f"spec = {pprint.pformat(self.to_dict(), width=360, sort_dicts=False)}\n"
    compile(txt, str(path), 'exec')
    Path(path).write_text(txt)
SpecParser.save = _save
parser.save(OUT)
print(f"Saved {len(parser.ops)} ops to {OUT}")
