---
name: kalligator
description: Submit and manage security reports on Kalligator, a bug bounty platform with AI triage, through its API. Use when a task involves a Kalligator account, API key, program, report draft, evidence upload, submission, triage reply, or payout status.
---

# Kalligator

Kalligator is a bug bounty platform. A hacker (`researcher` in the API) submits a report on a program. An AI triage agent tries to reproduce it and can ask questions. The Kalligator team (`founder` in the API) makes the final decision and approves the reward.

You act for one hacker through the hacker API. Full docs: https://doc.kalligator.com/llms.txt. Add `.md` to any docs URL to get Markdown.

## Guardrails

- **Scope is your authorization.** Send test traffic only to assets that the program `scope` names. Obey `exclusions` and `rules`. Use the program's test accounts and synthetic data. Stop a test that could affect a real person, real data, or service availability.
- **The human approves submission.** Show the human the final title, asset, description, and file list, and get a clear yes before `POST .../submit`. Skip this only if the human told you to submit without review.
- **Keys stay secret.** Read the key from `KALLIGATOR_API_KEY`. Keep it out of output, logs, reports, messages, and files.
- **Evidence is minimal.** Mask secrets and personal data in reports and files. Show only what proves the flaw.

## API basics

- Base URL: `https://kalligator.com/api`. Schema: `https://kalligator.com/api/openapi.json`.
- Header: `Authorization: Bearer $KALLIGATOR_API_KEY` (key starts with `kal_`).
- JSON in and out. Paths have no trailing slash. Times are ISO 8601 UTC.
- Errors are `{"detail": "...", "code": "..."}`. Branch on `code`.
- You make report IDs and file IDs: new UUIDv4 values. Store them and reuse them on retry.
- Each report has a `revision`. Send the latest one with each change. Store the new one from each response, file uploads included.

## Step 1: Check the account

`GET /api/me` and `GET /api/stripe/status`.

Done when `email_verified` (from `/api/me`) is `true`, `ready` (from `/api/stripe/status`) is `true`, and `active_reports` is less than `active_limit` (5). Check the email first: `/api/stripe/status` returns `403 email_unverified` for an unverified account.

If a check fails, the human must act in a browser. An API key cannot do these steps (`403 session_required`):

| Missing | Tell the human |
| --- | --- |
| No API key | Sign up at https://kalligator.com/account, verify the email, open **API keys**, and create a key. Put it in `KALLIGATOR_API_KEY`. |
| `email_verified: false` | Open the link in the verification email, or select **Resend verification email** in **Profile**. |
| `ready: false` | Open **Payouts** on the account page and complete Stripe setup. `detail` names the next step. |
| `active_reports` = 5 | Wait for a decision, or withdraw a report. |

## Step 2: Choose a program and read its policy

`GET /api/programs?intake=open`, then `GET /api/programs/{program_id}`.

Done when you have read `scope`, `exclusions`, `rules`, `eligibility`, and `disclosure`, and the target asset is in `scope`. Also check `intake` is `open` and `pool_paused` is `false`. A private program is visible only to invited hackers: a `404` means not found or not invited.

## Step 3: Write the draft

`PUT /api/reports/{report_id}` with a new UUIDv4 and `revision: 0`:

```json
{
  "program_id": "acme-web",
  "title": "Stored XSS in project name on the dashboard",
  "asset": "https://app.example.com/dashboard",
  "description": "## Steps to reproduce\n\n1. ...\n\n## Expected behavior\n\n...\n\n## Actual behavior\n\n...\n\n## Security impact\n\n...",
  "cvss_vector": "",
  "revision": 0
}
```

- One flaw per report: one root cause with one impact. Make a separate report for each other flaw.
- Write text under all four headings. Number the steps. Give exact requests, parameters, and test accounts.
- Label each claim as demonstrated or inferred.
- `cvss_vector` is optional: a CVSS 3.1 base vector, or `""`. Triage treats it as unverified.
- Limits: `title` 180, `asset` 1000, `description` 30000 characters.

Done when the response `status` is `draft` and you stored its `revision`.

## Step 4: Upload evidence

`PUT /api/reports/{report_id}/files/{file_id}?name=<file name>&revision=<revision>` with the raw bytes as the body and the MIME type as `Content-Type`. The response is the report with a new `revision`.

Link each file in the description: `[request.txt](/reports/{report_id}/files/{file_id})`, then save the draft again. Use PDF or plain text: triage cannot open Office documents. Limits: 10 files, 10 MiB each, not empty.

Done when every file in `attachments` has `state: "ready"`.

## Step 5: Submit

Get the human's approval (see Guardrails). Then `POST /api/reports/{report_id}/submit` with `{"revision": <revision>}`.

Done when `status` is `triaging`. To repeat the call with the same `revision` is safe.

## Step 6: Follow triage

Poll `GET /api/reports?updated_since=<newest updated_at seen>` at most once a minute. Use the `Z` form, URL-encode it, and read every page by `next_cursor`.

| `status` | Action |
| --- | --- |
| `triaging`, `paused`, `human_review` | Wait. A message is optional and starts no turn. |
| `needs_info` | `GET /api/reports/{id}/messages`, answer the newest `agent` question exactly, then `POST /api/reports/{id}/messages` with `{"body": "...", "files": [...]}`. |
| `accepted` | Read `decision.message`. `payout` appears after the team approves the reward. Payout changes do not change `updated_at`: read the report to follow them. |
| `rejected`, `duplicate`, `insufficient_info` | Read `decision.message` and tell the human. Appeals go by email to nathan@kalligator.com. |
| `withdrawn` | No action. |

A reply in `needs_info` starts the next triage turn. A message adds a new entry on each call: read the thread before you send again. To attach a file to a message, upload it first with the file route, then send its ID in `files`.

Done when the report has a final status and you told the human the outcome.

## Errors

| `code` | Action |
| --- | --- |
| `rate_limited` (429), `busy` (503) | Wait `Retry-After` seconds, then retry the same request. |
| `stripe_unavailable`, `storage_unavailable` (503) | Wait about a minute, then retry the same request. |
| `revision_conflict` (409) | Read `current` from the body, merge your change, retry with `current.revision`. |
| `email_unverified`, `stripe_not_ready` (403) | Return to Step 1. |
| `session_required` (403) | The human must do this on the website. |
| `read_only_key` (403) | The human must create a write key. |
| `incomplete_report` (422) | Fill every description heading, the title, and the asset. |
| `files_pending` (409) | Finish or remove unfinished uploads. |
| `file_referenced` (409) | Remove the file's link from the text before you remove the file. |
| `active_limit`, `program_closed`, `pool_low` (409), `stripe_unconfigured` (503) | Stop and tell the human. |
| `invalid_state` (409) | Re-read the report status; the action does not fit it. |
| `unauthenticated` (401) | The key is missing, deleted, or expired. Ask the human for a new key. |

## Reference

- Report lifecycle and status rules: https://doc.kalligator.com/policies/report-lifecycle.md
- Duplicates and priority time: https://doc.kalligator.com/policies/duplicates.md
- Rules of engagement: https://doc.kalligator.com/policies/rules-of-engagement.md
- All error codes: https://doc.kalligator.com/api-reference/errors.md
- Limits: https://doc.kalligator.com/api-reference/limits.md
- Retries and polling: https://doc.kalligator.com/api-reference/retries-and-polling.md
