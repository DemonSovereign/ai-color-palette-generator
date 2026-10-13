# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | yes       |
| < 0.3   | no        |

## Reporting a vulnerability

Email `security@ai-color-palette-generator.dev` with:

- a description of the issue,
- a minimal reproducer,
- the version and platform (Windows 10/11, Python 3.11+),
- whether you are willing to coordinate disclosure.

We aim to acknowledge within 72 hours and to ship a patched release within
14 days for high-severity issues.

## Scope

In scope:

- Arbitrary code execution via malformed palette files (`.ase`, `.gpl`, `.json`).
- Path traversal in the export service when writing to `exports/`.
- Unsafe deserialization in `palette_gen.utils.cache`.

Out of scope:

- Issues that require an attacker to already control the user's Python
  environment.
- Denial of service via extremely large images (documented limit is 8192x8192).

## Hardening notes

Model weights in `models/weights/` are loaded via `torch.load(..., weights_only=True)`.
If you are auditing, start at `palette_gen/services/extraction_service.py`.