---
name: survey-navigator
description: Use this skill when the user provides a survey, review, tutorial, or position paper and wants a field map, taxonomy, reference triage, reading roadmap, and Zotero or Obsidian organization plan without pretending the assistant is a fully autonomous scientist.
version: 0.1.0
---

# Survey Navigator

Use this skill to turn one survey-style paper into a **human-reviewed navigation package**:

```text
survey intake -> survey map -> reference triage -> optional reference enrichment -> reading roadmap -> Zotero plan -> Obsidian export plan
```

## Goal

Start from a survey, review, tutorial, or position paper and produce:
- a field structure,
- a paper classification table,
- role-based reading routes,
- and a concrete Zotero / Obsidian management plan.

This skill is **human-in-the-loop**. It helps the researcher see the field faster, but it does not replace judgment about which papers matter, which taxonomy is correct, or which claims are stable enough to promote.

## Intake sources

Accept any of these as the starting object:
- PDF
- Markdown notes
- arXiv page or arXiv ID
- DOI
- URL
- Zotero item
- Zotero collection

## Default workflow

### 1. Survey intake
- identify the survey title, source type, and scope
- confirm whether the paper is a survey, review, tutorial, or position paper
- record access limits such as abstract-only, partial text, or no reference pages

### 2. Survey map
- extract the survey topic, section structure, taxonomy, core questions, method categories, application categories, and open problems
- separate **what the survey explicitly says** from **assistant inference**
- keep weak or uncertain branches marked as tentative

### 3. Reference extraction
- extract reference metadata when available: `title`, `authors`, `year`, `venue`, `doi`, `arxiv`, `url`
- if a field cannot be verified from the provided source, write `unknown`
- do not invent citation metadata

### 4. Paper triage
- place cited papers under taxonomy branches
- assign paper-role labels such as `foundational`, `representative`, `recent`, `method`, `system`, `benchmark`
- assign reading-priority labels such as `must-read` or `optional`
- keep ambiguous assignments explicit instead of forcing false precision

### 5. Optional reference enrichment
- use Semantic Scholar as the preferred optional metadata resolver when title-only or partial references need more metadata
- prefer Semantic Scholar before any Google Scholar fallback because Google Scholar has no official public API
- if `S2_API_KEY` exists, use it for higher-confidence or higher-volume enrichment
- without `S2_API_KEY`, treat enrichment as low-frequency and best-effort only
- if enrichment fails, keep `unknown` fields and fall back to a manual import plan
- do not pretend enrichment has completed Zotero import or PDF download

### 6. Reading roadmap
- build three routes:
  - `beginner path`
  - `research path`
  - `engineering path`
- explain why each paper appears in the route and what the reader should extract from it

### 7. Zotero plan
- if Zotero MCP is available, prefer:
  - `zotero_create_collection`
  - `zotero_add_items_by_identifier`
  - `zotero_reconcile_collection_duplicates`
- propose tags and collection structure before bulk import when scope is still uncertain
- if Zotero MCP is unavailable, produce a manual import plan with identifiers, tags, and dedupe steps

### 8. Obsidian export
- keep the survey source note under `Sources/Papers/`
- route durable synthesis into `Knowledge/`
- treat `Maps/literature.canvas` as the default graph destination
- do not generate extra canvases unless explicitly requested

## Default outputs

- `survey-map.md`
- `paper-triage-table.md`
- `enriched-reference-table.md` when enrichment is attempted
- `reading-roadmap.md`
- `zotero-import-plan.md`
- `obsidian-export-plan.md`
- optional `citation-graph.json` only as a lightweight schema-driven artifact

## Rules

- Keep human decisions at the center.
- Mark missing metadata as `unknown`.
- Distinguish source-grounded extraction from assistant inference.
- Treat reference enrichment as optional and best-effort, not as a guaranteed resolver pass.
- Prefer Semantic Scholar over Google Scholar for metadata enrichment; use Google Scholar only as optional third-party or manual fallback.
- Never claim Zotero import, PDF attachment, or PDF download succeeded unless the current run actually performed and verified it.
- Do not claim OCR, MinerU, or parser integrations unless they are actually available in the current environment.
- Prefer reusable Markdown outputs over hidden reasoning.
- Route survey-derived source notes through `Sources/Papers` before promoting stable synthesis into `Knowledge` or `Writing`.

## Read next

- `README.md`
- `references/WORKFLOW.md`
- `references/OBSIDIAN-ROUTING.md`
- `references/semantic-scholar-resolver.md`
- `workflows/reference-enrichment.md`
- `templates/`
- `examples/graph-based-agent-memory-example.md`
