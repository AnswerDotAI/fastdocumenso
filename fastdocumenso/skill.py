"""Send documents for e-signature via the Documenso v2 API. Envelope, recipient, field, and audit operations are exposed as async functions.

Use the preconfigured `documenso` client. It needs `$DOCUMENSO_API_KEY`. Operations are async. Await them. This skill trusts only a read, create and sign allowlist. Delete and cancel calls are blocked by safepyrun.

# Allowed operations

- `documenso.envelope.envelope_create`
- `documenso.envelope.envelope_get`
- `documenso.envelope.envelope_find`
- `documenso.envelope.envelope_recipient_create_many`
- `documenso.envelope.envelope_field_create_many`
- `documenso.envelope.envelope_distribute`
- `documenso.envelope.envelope_item_download`
- `documenso.envelope.envelope_audit_log_find`

# Envelope signing workflow

Recipients and their fields go inline in the create payload. That makes the whole setup 2 calls:

    env = await documenso.envelope.envelope_create(                # -> {'id': 'envelope_xxx'}
        payload={'title': 'Test', 'type': 'DOCUMENT',
                 'recipients': [{'email': 'a@b.com', 'name': 'A', 'role': 'SIGNER',
                                 'fields': [{'type': 'SIGNATURE', 'page': 1, 'positionX': 60,
                                             'positionY': 80, 'width': 25, 'height': 5}]}]},
        files=('doc.pdf', pdf_bytes, 'application/pdf'))
    eid = env['id']
    res = await documenso.envelope.envelope_distribute(envelope_id=eid)  # sends real email
    # -> {'success': True, 'id': 'envelope_xxx', 'recipients': [{'id','name','email','token',
    #     'role','signingOrder','signingUrl'}]}
    signing_url = res['recipients'][0]['signingUrl']               # https://app.documenso.com/sign/{token}

Use the step-by-step alternative when adding recipients or fields to an existing envelope. Each call feeds the next. `envelope_get` is the only source of the envelope item id:

    d = await documenso.envelope.envelope_get(envelope_id=eid)     # -> full record: status, title,
                                                                   # recipients, fields, envelopeItems,
                                                                   # secondaryId, team, user, timestamps
    item_id = d['envelopeItems'][0]['id']                          # 'envelope_item_xxx'

    r = await documenso.envelope.envelope_recipient_create_many(   # -> {'data': [{...}]}
        envelope_id=eid,
        data=[{'email': 'a@b.com', 'name': 'A', 'role': 'SIGNER'}])
    rid = r['data'][0]['id']                                       # int, e.g. 3171028

    await documenso.envelope.envelope_field_create_many(           # -> {'data': [{...}]}
        envelope_id=eid,
        data=[{'recipientId': rid, 'envelopeItemId': item_id, 'type': 'SIGNATURE',
               'page': 1, 'positionX': 60, 'positionY': 80, 'width': 25, 'height': 5}])

    res = await documenso.envelope.envelope_distribute(envelope_id=eid)  # same shape as above

# Checking status and downloading

    d = await documenso.envelope.envelope_get(envelope_id=eid)   # d['status']: DRAFT / PENDING / COMPLETED / REJECTED / CANCELLED
    # Dashboard URL: https://app.documenso.com/t/{d['team']['url']}/documents/{d['secondaryId'].split('_')[1]}
    signed = await documenso.envelope.envelope_item_download(envelope_item_id=item_id)  # bytes; version='original'|'signed'|'pending' (default 'signed')

# Audit logs

    logs = await documenso.envelope.envelope_audit_log_find(envelope_id=eid, per_page=100)
    # -> {'data': [...], 'count': int, 'currentPage': int, 'perPage': int, 'totalPages': int}

# Finding envelopes

    found = await documenso.envelope.envelope_find(status='PENDING', per_page=100,
                    order_by_column='createdAt', order_by_direction='desc')
    # -> {'data': [...], 'count': int, 'currentPage': int, 'perPage': int, 'totalPages': int}

Filters: `query`, `status` (DRAFT/PENDING/COMPLETED/REJECTED/CANCELLED), `type` (DOCUMENT/TEMPLATE), `source`, `folder_id`, `template_id`, `has_expired_recipients`. There is no date filter. Sort by `createdAt` descending and cut client-side.

# Gotchas

- `distribute` sends real emails to recipients. Call it only when you intend the emails to go out.
- Field coordinates (`positionX`/`positionY`/`width`/`height`) are percentages of the page, origin top-left.
- Multipart file params: pass as `(filename, bytes, mimetype)` tuple.
- `payload` is a plain dict. The client JSON-encodes it for multipart.
- `envelope_create` returns `{'id': ...}` and nothing else. Call `envelope_get` for item ids, recipients, fields, status, and `team['url']`.
- `envelope_distribute` returns `{'success': True, 'id': ..., 'recipients': [...]}`. It has no `status` key. The signing URL is `res['recipients'][0]['signingUrl']`.
- Return shapes are annotated inline above. If one is not annotated, print the whole dict rather than guessing a key.
- Never put a side-effecting call (`distribute`) and speculative inspection in the same cell. If the cell raises, its variables are discarded even though the network call already went through. Capture first, inspect separately.
- Field types: SIGNATURE, FREE_SIGNATURE, INITIALS, NAME, EMAIL, DATE, TEXT, NUMBER, RADIO, CHECKBOX, DROPDOWN. Roles: SIGNER, CC, VIEWER, APPROVER, ASSISTANT. Statuses: DRAFT, PENDING, COMPLETED, REJECTED, CANCELLED.
- Ids use three schemes: envelope and item ids are opaque strings (`envelope_xxx`), recipient and field ids are ints, and `secondaryId` holds the legacy numeric document id."""
from pyskills.core import allow
from fastdocumenso.core import documenso_client

__all__ = ['documenso']

documenso = documenso_client()

allow(documenso.envelope.envelope_create,
      documenso.envelope.envelope_get,
      documenso.envelope.envelope_find,
      documenso.envelope.envelope_recipient_create_many,
      documenso.envelope.envelope_field_create_many,
      documenso.envelope.envelope_distribute,
      documenso.envelope.envelope_item_download,
      documenso.envelope.envelope_audit_log_find)
