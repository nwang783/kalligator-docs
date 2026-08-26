# Documentation project instructions

## About this project

- This repository contains the Mintlify documentation site for Kalligator.
- Kalligator source material lives in `../mobile-lab`.
- Pages use MDX with YAML frontmatter.
- Site configuration lives in `docs.json`.
- Use the repository-local Mintlify skill and Index MCP for current Mintlify syntax.

## Terminology

- Use **Kalligator** for the product name.
- Use **Account**, not user profile.
- Use **Team**, not tenant or organization.
- Use **Project**, not engagement or workspace.
- Use **Chat**, not session, trace, or transcript.
- Use **Package**, not plugin.
- Use **Android Test Device**, not target.
- Use **Observation** for a research fact.
- Use **Finding** for a vulnerability claim supported by Observations.
- Keep stable `mobile-lab`, `mobilelab`, and `kaligator` technical identifiers unchanged.

## Style

- Use ASD-STE100 Simplified Technical English.
- Use active voice and second person.
- Keep one main idea in each sentence.
- Use sentence case for headings.
- Use bold text for UI labels, such as **Settings**.
- Use code formatting for file names, commands, paths, and identifiers.
- Use root-relative links without file extensions for internal pages.
- Use built-in Mintlify components before custom MDX components or CSS.

## Content boundaries

- Document supported product behavior and reader workflows.
- State authorization requirements for security testing.
- Do not publish secrets, live credentials, private targets, or raw vulnerability evidence.
- Do not present deferred work as supported behavior.
- Do not copy internal ADR text without adapting it for the reader.
