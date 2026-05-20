# Reference Enrichment Workflow

This workflow is optional.

Use it only when the survey reference list is incomplete enough that better metadata would improve:
- paper triage,
- reading-order decisions,
- Zotero import planning,
- or later Obsidian linking.

## Inputs

Accepted starting points:
- reference rows extracted from the survey
- title-only reference lists
- partial metadata exported from a PDF or Markdown source
- a small JSON list of references prepared by the user

## Default order

```text
extracted references -> Semantic Scholar enrichment (optional) -> enriched-reference-table.md -> paper-triage-table.md -> zotero-import-plan.md
```

## Step 1: Decide whether enrichment is worth doing

Try enrichment when:
- many rows are title-only
- DOI / arXiv fields are mostly `unknown`
- venue or year ambiguity blocks Zotero import planning

Skip enrichment when:
- the survey already has high-quality metadata
- the task is only a structure-level dry-run
- the user wants planning only

## Step 2: Select the resolver

Preferred resolver:
- Semantic Scholar

Fallbacks:
- CrossRef for DOI-oriented follow-up
- arXiv for preprint-oriented follow-up
- Google Scholar only as manual or explicit third-party fallback

## Step 3: Authentication mode

If `S2_API_KEY` exists:
- use authenticated mode
- larger or repeated batches are more reasonable

If `S2_API_KEY` does not exist:
- use unauthenticated or low-frequency mode
- expect stricter rate limits
- stop early instead of pretending the batch is complete

## Step 4: Normalize output

Populate these fields:
- `title`
- `authors`
- `year`
- `venue`
- `abstract`
- `citationCount`
- `influentialCitationCount`
- `externalIds`
- `url`
- `openAccessPdf`
- `fieldsOfStudy`

Any unresolved field becomes:

```text
unknown
```

## Step 5: Gate the result

Do not treat enrichment as ground truth until the row still looks plausible after manual review.

Minimum sanity checks:
- title roughly matches the survey reference
- year is not obviously impossible
- venue is not contradictory
- any DOI or arXiv ID came from the resolver response, not guesswork

## Step 6: Downstream behavior

If enrichment is good enough:
- use the enriched rows to improve `paper-triage-table.md`
- use identifiers to strengthen `zotero-import-plan.md`

If enrichment is weak:
- keep the original triage rows
- keep `unknown` fields
- produce a manual import plan

## Hard boundaries

- Do not claim a Zotero item was imported unless the current run actually imported it.
- Do not claim a PDF was downloaded or attached unless verified in the current run.
- Do not fill missing citation counts, DOI, arXiv IDs, or venue names from memory.
