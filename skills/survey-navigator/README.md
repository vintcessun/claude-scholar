# `survey-navigator` skill

Survey-first literature navigation for researchers who want to start from one review paper and build a usable map of the field.

## What it does

`survey-navigator` turns a survey, review, tutorial, or position paper into a compact navigation package:

- `survey-map.md` for the field structure and taxonomy
- `reference-list.json` for conservative machine-readable reference extraction
- `paper-triage-table.md` for cited-paper classification
- `citation-lineage.md` for a human-readable related-work evolution map
- `citation_contexts.json` for machine-oriented citation-to-section linkage when available
- `reading-roadmap.md` for role-based reading plans
- `zotero-import-plan.md` for collection, import, tag, and dedupe actions
- `obsidian-export-plan.md` for KB routing into `Sources/Papers`, `Knowledge`, and `Maps`
- `enriched-reference-table.md` for optional metadata enrichment

It is designed for **survey-driven orientation**, not for autonomous literature judgment. The user still decides which taxonomy is valid, which branches matter, and which papers deserve deep reading.

## Typical use cases

Use this skill when the user says things like:

- "I have one survey paper. Help me understand the field."
- "Extract the taxonomy from this review and tell me what to read next."
- "Turn this survey's references into a Zotero import and reading plan."
- "Organize this tutorial paper into my Obsidian literature workflow."
- "读这个综述，帮我整理引用论文和阅读路线。"
- "把这篇 survey 接到 Zotero 和 Obsidian。"
- "围绕这篇 review 做文献整理。"

Even if the user does not mention `survey-navigator` by name, prefer this skill when the request includes:

- 综述
- review
- tutorial paper
- taxonomy
- 引用论文
- 阅读路线
- 文献整理
- Zotero
- Obsidian

## Scope boundaries

- It supports intake from PDF, Markdown, DOI, arXiv, URL, Zotero item, or Zotero collection.
- It supports an **optional** reference-enrichment step, with Semantic Scholar preferred over Google Scholar.
- It does not require an API key by default; without `S2_API_KEY`, enrichment should stay low-frequency and best-effort.
- It does not promise OCR, MinerU, or automatic PDF parsing beyond what the current environment already provides.
- It does not fabricate missing citation metadata.
- It does not pretend Zotero import or PDF download already happened unless the current run actually verified those actions.
- It does not pretend Obsidian write-back already happened unless the current run actually verified those actions.
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
│   ├── enrich_references_semantic_scholar.py
│   └── extract_real_pdf_intake.py
├── templates/
│   ├── citation-graph.schema.json
│   ├── citation-lineage.md
│   ├── enriched-reference-table.md
│   ├── obsidian-export-plan.md
│   ├── paper-triage-table.md
│   ├── reading-roadmap.md
│   ├── survey-map.md
│   └── zotero-import-plan.md
└── examples/
    ├── graph-based-agent-memory-example.md
    ├── sample-references.json
    ├── enriched-references.example.json
    └── ...
```

## Output design

| Output | Purpose |
|---|---|
| `survey-map.md` | Extracts the survey's topic structure, taxonomy, open questions, and application map |
| `reference-list.json` | Preserves conservative extracted references for downstream review, enrichment, or import planning |
| `paper-triage-table.md` | Organizes cited papers by taxonomy branch, role, and reading priority |
| `citation-lineage.md` | Human-readable related-work artifact that turns grouped papers into a field-evolution map |
| `citation_contexts.json` | Machine-oriented intermediate artifact that links citation numbers back to sections or subsections |
| `reading-roadmap.md` | Splits the reading route into beginner, research, and engineering tracks |
| `zotero-import-plan.md` | Plans collection creation, identifier import, tags, and dedupe |
| `obsidian-export-plan.md` | Maps the survey package into the repo's Obsidian workflow |
| `enriched-reference-table.md` | Stores optional Semantic Scholar enrichment results while preserving `unknown` for unresolved fields |
| `citation-graph.schema.json` | Optional lightweight schema for graph export, not a required runtime dependency |

Unless the user explicitly narrows the task, these outputs should be treated as the default complete workflow package.

Recommended interpretation:

- `citation-lineage.md` answers: "这条 related-work 线是怎么演化出来的？"
- `reading-roadmap.md` answers: "接下来应该按什么目标去读？"
- `citation_contexts.json` answers: "这些 citation 在 survey 的哪个 section 或 subsection 中出现？"

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

## Fallback behavior

- If the user only asks for "综述 / 阅读路线 / 引用论文 / 文献整理 / Zotero / Obsidian", this skill should still be the first choice.
- If only abstract-level access is available, emit a reduced package and mark missing details explicitly.
- If citation linking is unavailable, produce the rest of the workflow and state that `citation_contexts.json` could not be grounded from the current source.
- If grouped papers are available but machine citation linking is weak, `citation-lineage.md` can still be produced as a conservative related-work artifact.
- If Zotero MCP or Obsidian write-back is unavailable, stay in planning-only mode and produce plans only.
