# Kalligator documentation

This repository contains the Mintlify documentation site for Kalligator, published at https://doc.kalligator.com.
Mintlify deploys the site automatically when you push to `main`.

## Preview

Install the Mintlify CLI, then start the local preview:

```bash
npm install --global mint
mint dev
```

Run these checks before you publish changes:

```bash
mint broken-links
mint a11y
mint validate
```

## API reference

The endpoint pages come from `api-reference/openapi.json`. Do not edit that file by hand.

- The Kalligator API owns the routes and types.
- `api-reference/overlay.json` owns the reader text: titles, descriptions, servers, and tags.

After an API change, update the overlay if necessary, then run:

```bash
python3 scripts/sync_openapi.py
```

The script fetches `https://kalligator.com/api/openapi.json`, applies the overlay, and writes `api-reference/openapi.json`.
It fails if an overlay entry does not match the schema, or if a route has no overlay entry.
To use a local API, pass `--source http://127.0.0.1:8787/api/openapi.json` or a file path.

## Agent skill

`skill.md` at the repository root is the Kalligator skill for hackers' agents.
Mintlify serves it at `/skill.md` and in the skill discovery endpoints, in place of the generated skill.
Update it when the API workflow or the error codes change.

Product source material lives in the `kalligator` repository (`platform/docs/api-contract.md`, `CONTEXT.md`, `DESIGN.md`).
