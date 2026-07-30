"""Send documents for e-signature via the Documenso v2 API — envelope, document, and audit operations as self-documenting async functions.

Create a client with `documenso_client()` (needs `$DOCUMENSO_API_KEY`). Operations are async — await them. This skill is locked to a read+create+sign whitelist for safe testing on production; delete and cancel are not available.

# Envelope signing workflow

    cli = documenso_client()
    env = await cli.envelope.envelope_create(payload={'title': 'Test', 'type': 'DOCUMENT'}, files=('doc.pdf', pdf_bytes, 'application/pdf'))
    await cli.envelope.envelope_recipient_create_many(envelope_id=env['id'], data=[{'email': 'a@b.com', 'name': 'A', 'role': 'SIGNER'}])
    await cli.envelope.envelope_field_create_many(envelope_id=env['id'], data=[{'recipientId': rid, 'envelopeItemId': item_id, 'type': 'SIGNATURE', 'page': 1, 'positionX': 60, 'positionY': 80, 'width': 25, 'height': 5}])
    await cli.envelope.envelope_distribute(envelope_id=env['id'])

# Checking status and downloading

    d = await cli.envelope.envelope_get(envelope_id=env['id'])   # d['status']: DRAFT / PENDING / COMPLETED
    signed = await cli.envelope.envelope_item_download(envelope_item_id=item_id)  # bytes

# Audit logs

    logs = await cli.envelope.envelope_audit_log_find(envelope_id=env['id'], per_page=100)

# Finding existing documents

    docs = await cli.document.document_find(per_page=10)
    doc = await cli.document.document_get(document_id=123)

# Gotchas

- `distribute` sends real emails to recipients — only call when intended.
- Field coordinates (`positionX`/`positionY`/`width`/`height`) are percentages of the page, origin top-left.
- Multipart file params: pass as `(filename, bytes, mimetype)` tuple.
- `payload` is a plain dict — the client JSON-encodes it for multipart.
- Delete and cancel operations are not available in this skill."""
from pyskills.core import allow
from fastspec.oapi import OpGroup, OpFunc
from fastdocumenso.core import documenso_client, documenso_spec

__all__ = ['documenso_client', 'documenso_spec']

allow(documenso_client, documenso_spec,
      {OpGroup: [...], OpFunc: ['__call__']})
