# Documentation project instructions

## About this project

- This repository contains the Mintlify documentation site for Kalligator, the bug bounty platform at https://kalligator.com.
- The site is published at https://doc.kalligator.com. A push to `main` deploys it.
- Kalligator source material lives in `~/Projects/kalligator`. The API contract is `platform/docs/api-contract.md`. The domain language is `CONTEXT.md`. The visual design is `DESIGN.md`.
- Pages use MDX with YAML frontmatter. Site configuration lives in `docs.json`.
- Endpoint pages come from `api-reference/openapi.json`. Change reader text in `api-reference/overlay.json`, then run `python3 scripts/sync_openapi.py`.
- `skill.md` is the published agent skill. Keep it in step with the API and the guides.
- Use the repository-local Mintlify skill and Index MCP for current Mintlify syntax.

## Terminology

- Use **Kalligator** for the product name.
- Use **hacker** in prose for the person who submits reports. The API calls this person a `researcher`.
- Use **Kalligator team** for the people who decide reports and approve rewards. The API calls them `founder`.
- Use **program**, **report**, **flaw**, **duplicate**, **priority time**, and **known issue** as `CONTEXT.md` in the kalligator repository defines them.
- Use **triage agent** for the AI agent that assesses reports. Use **triage turn** for one run of it.
- Use **API key** for a `kal_` key. Do not call it a token.
- Use **reward**, not payout, until the Kalligator team approves it.
- Use the exact UI labels of the website in bold, for example **Submit report**.

## Style

- Use ASD-STE100 Simplified Technical English.
- Use active voice and second person.
- Keep one main idea in each sentence.
- Use sentence case for headings.
- Use bold text for UI labels, such as **Payouts**.
- Use code formatting for file names, commands, paths, field names, and error codes.
- Use root-relative links without file extensions for internal pages.
- Use built-in Mintlify components before custom MDX components or CSS.
- Keep brand styling in `docs.json` and `custom.css`. The colors come from `platform/web/src/app.css` in the kalligator repository.

## Content boundaries

- Document hacker-facing behavior only. Do not document founder, admin, internal, or webhook routes.
- State authorization requirements for security testing.
- Do not publish secrets, live credentials, private targets, or raw vulnerability evidence.
- Do not present deferred work as supported behavior. Payouts run in Stripe test mode. There is no disclosure workflow, no customer self-service, and no in-app appeal.
- Do not publish internal triage budgets, costs, or seed reward tables.
- Do not copy internal ADR text without adapting it for the reader.
