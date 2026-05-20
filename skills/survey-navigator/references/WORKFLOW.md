# Survey Navigator Workflow

## 1. Intake the survey object

Accepted starting points:
- local PDF
- Markdown note
- DOI
- arXiv ID or page
- URL
- Zotero item
- Zotero collection

Record:
- source type
- title if known
- access quality: full text | partial text | abstract-only | reference-list-only
- downstream constraint: dry-run | planning-only | Zotero-write allowed | Obsidian-write allowed

## 2. Build the survey map

The minimum survey map should capture:
- field or subfield name
- survey scope and stated motivation
- major sections
- taxonomy branches
- core questions
- method categories
- system or tooling categories when present
- application categories
- benchmarks or evaluation regimes when present
- open problems and limitations

Keep two layers visible:
- `source-grounded`: directly supported by the survey
- `assistant-inferred`: organizational help derived from the source

## 3. Extract reference metadata conservatively

For each cited paper, prefer these fields:

```text
title
authors
year
venue
doi
arxiv
url
```

Rules:
- if the source does not provide a field, write `unknown`
- if the survey uses abbreviated citations and the full metadata is unavailable, keep the record partial
- do not upgrade partial records into fully specified citations without evidence

## 4. Triage papers by role and reading value

Each paper can have:
- one primary taxonomy branch
- optional secondary branches
- one or more role labels
- one reading priority

Recommended role labels:
- `foundational`
- `representative`
- `recent`
- `method`
- `system`
- `benchmark`

Recommended priority labels:
- `must-read`
- `optional`

If the evidence is weak, add a note such as:
- `classification uncertain`
- `metadata incomplete`
- `mentioned without enough context`

## 5. Build the reading roadmap

Create three routes:

### Beginner path
- favor orientation papers
- include a small number of foundational or representative items
- explain the field concepts to extract from each item

### Research path
- favor taxonomy-defining, method-defining, or debate-defining items
- identify gaps and unresolved tensions
- note what evidence is still missing

### Engineering path
- favor systems, benchmarks, implementation-heavy papers, or reproducible artifacts
- highlight practical takeaways, tooling assumptions, and deployment constraints

## 6. Make the Zotero plan

When Zotero MCP is available:
- suggest a top collection name derived from the survey topic
- prefer `zotero_add_items_by_identifier`
- batch imports conservatively
- run `zotero_reconcile_collection_duplicates` after import

Suggested sub-collections:
- `Core Papers`
- `Foundational`
- `Methods`
- `Systems`
- `Benchmarks`
- `Applications`
- `To-Read`

Suggested tags:
- survey topic tag
- taxonomy branch tag
- role tag
- priority tag

When Zotero MCP is not available:
- emit a manual import ledger with DOI / arXiv / URL
- keep unresolved items in a manual follow-up section

## 7. Make the Obsidian export plan

Default routing:
- survey source note -> `Sources/Papers/`
- survey synthesis -> `Knowledge/`
- graph artifact -> `Maps/literature.canvas`

Do not:
- create extra canvases by default
- promote weak references into stable knowledge
- pretend abstract-only records support durable claims
