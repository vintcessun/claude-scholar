# Semantic Scholar Resolver Notes

Use this reference when `survey-navigator` needs an **optional metadata enrichment** step for partial or weak references.

## Role

Semantic Scholar is the preferred optional resolver for:
- title-only references
- incomplete author/year records
- weak venue information
- missing abstract or citation-count context

It is **not** a mandatory dependency for `survey-navigator`.

## Why Semantic Scholar first

- It has an official Graph API.
- It is stronger than Google Scholar for structured programmatic metadata.
- It can return ML- and AI-relevant citation graph signals that are useful during triage.

## Why not Google Scholar by default

- Google Scholar has no official public API.
- Scraping-based access is brittle and may violate ToS.
- Treat it only as:
  - a manual discovery fallback, or
  - an explicit third-party-provider fallback chosen by the user

## Authentication

- Default mode: no API key required
- Preferred env var when available: `S2_API_KEY`

If `S2_API_KEY` exists:
- use it for higher-volume or more reliable enrichment

If `S2_API_KEY` does not exist:
- keep queries low-frequency
- treat failures or empty results as normal
- do not over-promise coverage

## Enrichment fields

When enrichment is attempted, prefer these fields:

```text
title
authors
year
venue
abstract
citationCount
influentialCitationCount
externalIds
url
openAccessPdf
fieldsOfStudy
```

Rules:
- unresolved fields must be `unknown`
- do not fabricate DOI, arXiv, venue, abstract, or citation counts
- `externalIds` can contain DOI, ArXiv, CorpusId, ACL, MAG, PubMed, or other IDs only if actually returned

## Failure behavior

If Semantic Scholar fails or returns weak matches:
- preserve the original extracted reference row
- keep unresolved fields as `unknown`
- mark the row as `manual-review`
- continue to `zotero-import-plan.md` with a manual import path

## Safe wording

Good:
- `Semantic Scholar enrichment attempted`
- `best-effort metadata enrichment`
- `manual review still required`
- `no verified DOI returned`

Bad:
- `resolved all references`
- `import completed`
- `PDF attached`
- `citation graph confirmed`
