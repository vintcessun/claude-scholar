# `survey-navigator` skill

Survey-first literature navigation for researchers who want to start from one review paper and build a usable map of the field.

## What it does

`survey-navigator` turns a survey, review, tutorial, or position paper into a compact navigation package:

- `survey-map.md` for the field structure and taxonomy
- `paper-triage-table.md` for cited-paper classification
- `enriched-reference-table.md` for optional metadata enrichment
- `reading-roadmap.md` for role-based reading plans
- `zotero-import-plan.md` for collection, import, tag, and dedupe actions
- `obsidian-export-plan.md` for KB routing into `Sources/Papers`, `Knowledge`, and `Maps`

It is designed for **survey-driven orientation**, not for autonomous literature judgment. The user still decides which taxonomy is valid, which branches matter, and which papers deserve deep reading.

## Typical use cases

Use this skill when the user says things like:

- "I have one survey paper. Help me understand the field."
- "Extract the taxonomy from this review and tell me what to read next."
- "Turn this survey's references into a Zotero import and reading plan."
- "Organize this tutorial paper into my Obsidian literature workflow."

## Scope boundaries

- It supports intake from PDF, Markdown, DOI, arXiv, URL, Zotero item, or Zotero collection.
- It supports an **optional** reference-enrichment step, with Semantic Scholar preferred over Google Scholar.
- It does not require an API key by default; without `S2_API_KEY`, enrichment should stay low-frequency and best-effort.
- It does not promise OCR, MinerU, or automatic PDF parsing beyond what the current environment already provides.
- It does not fabricate missing citation metadata.
- It does not pretend Zotero import or PDF download already happened unless the current run actually verified those actions.
- It does not replace the existing paper-note workflow under `zotero-obsidian-bridge` or `obsidian-literature-workflow`; it prepares a structured entrypoint into those workflows.

## File structure

```text
survey-navigator/
├── README.md
├── SKILL.md
├── references/
│   ├── OBSIDIAN-ROUTING.md
│   ├── semantic-scholar-resolver.md
│   └── WORKFLOW.md
├── workflows/
│   └── reference-enrichment.md
├── scripts/
│   └── enrich_references_semantic_scholar.py
├── templates/
│   ├── citation-graph.schema.json
│   ├── enriched-reference-table.md
│   ├── obsidian-export-plan.md
│   ├── paper-triage-table.md
│   ├── reading-roadmap.md
│   ├── survey-map.md
│   └── zotero-import-plan.md
└── examples/
    └── graph-based-agent-memory-example.md
```

## Output design

| Output | Purpose |
|---|---|
| `survey-map.md` | Extracts the survey's topic structure, taxonomy, open questions, and application map |
| `paper-triage-table.md` | Organizes cited papers by taxonomy branch, role, and reading priority |
| `enriched-reference-table.md` | Stores optional Semantic Scholar enrichment results while preserving `unknown` for unresolved fields |
| `reading-roadmap.md` | Splits the reading route into beginner, research, and engineering tracks |
| `zotero-import-plan.md` | Plans collection creation, identifier import, tags, and dedupe |
| `obsidian-export-plan.md` | Maps the survey package into the repo's Obsidian workflow |
| `citation-graph.schema.json` | Optional lightweight schema for graph export, not a required runtime dependency |

## Relationship to neighboring skills

- Use `research-ideation` when the user needs gap analysis or a research question after survey intake.
- Use `zotero-obsidian-bridge` when the cited papers need to become canonical paper notes under `Sources/Papers/`.
- Use `obsidian-literature-workflow` when survey findings need stable synthesis in `Knowledge/` or `Writing/`.
- Use `citation-verification` or `ml-paper-writing` only when the task moves from survey navigation into stronger citation verification or writing workflows.

## Optional enrichment behavior

- Preferred metadata resolver: Semantic Scholar
- API key: optional via `S2_API_KEY`
- No-key mode: low-frequency queries only
- Google Scholar: not a default provider; only manual or third-party fallback
- Failure mode: keep `unknown` metadata and emit a manual import plan instead of pretending completion

## Example

See [examples/graph-based-agent-memory-example.md](./examples/graph-based-agent-memory-example.md) for a prompt and expected output structure built around:

`Graph-based Agent Memory: Taxonomy, Techniques, and Applications`

## Optional helper

You can run the optional Semantic Scholar helper on a small reference list:

```bash
python skills/survey-navigator/scripts/enrich_references_semantic_scholar.py \
  --input skills/survey-navigator/examples/sample-references.json \
  --output D:/tmp/enriched-references.json
```

Notes:
- `S2_API_KEY` is optional.
- Without `S2_API_KEY`, use low-frequency best-effort queries.
- API/network failures should still produce an output JSON with `api_error`, `not_found`, or `manual`-style fallback states.
- This helper does not imply Zotero import or PDF download happened.
