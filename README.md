# fastdocumenso

Async [Documenso](https://documenso.com) v2 API client built on [fastspec](https://github.com/AnswerDotAI/fastspec), with a [pyskill](https://github.com/AnswerDotAI/pyskills) for AI-assisted e-signature workflows.

## Install

```bash
pip install -e .
```

Set your Documenso API token (from *User settings → API tokens*):

In SolveIt, set your env var DOCUMENSO_API_KEY=your-token

## Usage

```python
from fastdocumenso import documenso_client

cli = documenso_client()

# Create an envelope with a PDF
env = await cli.envelope.envelope_create(
    payload={'title': 'My NDA', 'type': 'DOCUMENT'},
    files=('doc.pdf', pdf_bytes, 'application/pdf'))

# Add a signer and a signature field
await cli.envelope.envelope_recipient_create_many(
    envelope_id=env['id'],
    data=[{'email': 'a@b.com', 'name': 'A', 'role': 'SIGNER'}])

await cli.envelope.envelope_field_create_many(
    envelope_id=env['id'],
    data=[{'recipientId': rid, 'envelopeItemId': item_id,
           'type': 'SIGNATURE', 'page': 1,
           'positionX': 60, 'positionY': 80, 'width': 25, 'height': 5}])

# Send the signing email
await cli.envelope.envelope_distribute(envelope_id=env['id'])

# Check status and download the signed document
d = await cli.envelope.envelope_get(envelope_id=env['id'])
signed = await cli.envelope.envelope_item_download(envelope_item_id=item_id)
```

## Operations

The full Documenso v2 spec has 89 operations. This client ships with a whitelist of 9 read+create+sign operations for safe testing:

| Group | Operations |
|---|---|
| envelope | `create`, `get`, `recipient_create_many`, `field_create_many`, `distribute`, `item_download`, `audit_log_find` |
| document | `find`, `get` |

To change the whitelist, edit `_ALLOWED_OPS` in `fastdocumenso/core.py`.

## Updating the spec

The spec snapshot is fetched from `https://app.documenso.com/api/v2/openapi.json`. When the API changes, re-run:

```bash
python scripts/update_spec.py
```

Note: `update_spec.py` also patches `file_params` for 5 envelope/document ops,
since Documenso's spec uses empty schemas instead of `format: binary` for file uploads.

## AI agent use

This package registers a pyskill (`fastdocumenso.skill`). AI hosts (solveit, etc.) can discover it via `list_pyskills()` and load it to automate signing workflows. The skill inherits the same whitelist — delete and cancel operations are not exposed.
