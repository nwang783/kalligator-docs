# Kalligator documentation

This repository contains the Mintlify documentation site for Kalligator.

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

Product source material lives in `../mobile-lab`. Keep public documentation focused on supported reader workflows. Do not copy internal ADRs without adapting them for the reader.
