# Security and disclosure

This is a sanitized academic infrastructure portfolio. It provides no authorization to probe third-party systems, discover private lab endpoints or test credentials.

Do not submit passwords, tokens, private keys, personal information or unsanitized configurations in an issue or pull request. If sensitive material is accidentally published, restrict access, rotate or revoke the affected secret and assess Git history and cached copies. Deleting the latest file is not enough.

The examples are educational starting points, not production hardening baselines. See [security decisions](docs/security.md) and [example limitations](examples/README.md).

Before publication:

1. Run all tests and `python tools/check_publication.py`.
2. Review the complete staged diff and file list.
3. Run an independent secret scanner when available.
4. Confirm ownership and permission for every included artifact.
5. Keep restricted handoffs and vault exports outside this repository.

No private lab certificates, secrets or screenshots are required to reproduce the offline examples.
