---
name: fastdocumenso
description: Check Documenso e-signature status. Use when asked who has signed a document, which signature requests are pending, or for the audit trail of an envelope.
---
Install: `pip install git+https://github.com/AnswerDotAI/fastdocumenso`

The token is `DOCUMENSO_API_KEY`. Use it from the environment if set; otherwise read it from `documenso.env` in the shared folder; otherwise ask the user.

Read the skill docstring first and follow it. It lists the allowed operations, return shapes and gotchas:

    python -c "import fastdocumenso.skill as s; print(s.__doc__)"

Write one short script per question and run it with `python`. Operations are async, so wrap them in `asyncio.run(...)`. Start from the "Who has signed" recipe in the docstring.

Never call delete, cancel or update operations.
