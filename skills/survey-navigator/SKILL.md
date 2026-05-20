---
name: survey-navigator
description: Use this skill when the user asks to read a survey, review, tutorial, or position paper, extract taxonomy or references, organize cited papers, build a reading roadmap, or plan Zotero/Obsidian literature management without pretending the assistant is a fully autonomous scientist.
version: 0.1.0
---

# Survey Navigator

Use this skill to turn one survey-style paper into a **human-reviewed navigation package**:

```text
survey intake -> survey map -> reference triage -> citation lineage -> related-work evolution -> reading roadmap -> Zotero plan -> Obsidian export plan
```

## Activation cues

Use this skill by default when the user provides or mentions a survey-like paper and asks for any combination of:
- read this survey
- summarize this review
- extract the taxonomy
- extract or organize the references
- tell me what to read next
- build a reading roadmap
- organize the cited papers
- make a Zotero plan
- make an Obsidian plan
- help me整理综述 / 阅读路线 / 引用论文 / 文献整理

Also activate this skill when the user does **not** explicitly say `survey-navigator`, but the request clearly means:
- "读这个综述"
- "帮我整理这篇 survey 的引用论文"
- "给我做阅读路线"
- "把这篇综述接到 Zotero / Obsidian"

If the request mixes survey reading, cited-paper organization, reading roadmap design, and literature-management planning, prefer this skill first.

## Goal

Start from a survey, review, tutorial, or position paper and produce:
- a field structure,
- a conservative reference list,
- a paper classification table,
- a human-readable citation lineage or related-work evolution note,
- role-based reading routes,
- machine citation contexts when the source allows,
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
- emit `reference-list.json` as the default machine-readable reference artifact
- if a field cannot be verified from the provided source, write `unknown`
- do not invent citation metadata

### 3.5 Citation lineage or citation contexts
- capture citation-to-section context in `citation_contexts.json` when citations can be extracted programmatically
- build `citation-lineage.md` as a human-readable related-work artifact from citation contexts, survey sections, and grouped papers
- if machine citation linking is weak but grouped-paper evidence is still usable, `citation-lineage.md` may still be produced conservatively
- if citation linking is not possible from the current source, say so explicitly instead of pretending it was completed

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
- keep `reading-roadmap.md` distinct from `citation-lineage.md`:
  - `citation-lineage.md` explains related-work evolution
  - `reading-roadmap.md` explains reading order for a concrete user goal

### 7. Zotero plan
- if Zotero MCP is available, prefer:
  - `zotero_create_collection`
  - `zotero_add_items_by_identifier`
  - `zotero_reconcile_collection_duplicates`
- propose tags and collection structure before bulk import when scope is still uncertain
- if Zotero MCP is unavailable, produce a manual import plan with identifiers, tags, and dedupe steps
- never claim Zotero import happened unless the current run actually performed and verified it

### 8. Obsidian export
- keep the survey source note under `Sources/Papers/`
- route durable synthesis into `Knowledge/`
- treat `Maps/literature.canvas` as the default graph destination
- do not generate extra canvases unless explicitly requested
- never claim Obsidian write-back happened unless the current run actually performed and verified it

## Default outputs

- `survey-map.md`
- `reference-list.json`
- `paper-triage-table.md`
- `citation-lineage.md`
- `citation_contexts.json` when source quality allows
- `reading-roadmap.md`
- `zotero-import-plan.md`
- `obsidian-export-plan.md`
- `enriched-reference-table.md` when enrichment is attempted
- optional `citation-graph.json` only as a lightweight schema-driven artifact

Unless the user explicitly narrows scope, treat the list above as the default complete workflow package.

## Natural-language trigger examples

These requests should usually trigger `survey-navigator` even if the user never names the skill:

- "读一下这篇综述，帮我整理 taxonomy 和后续阅读路线。"
- "把这篇 survey 的引用论文拉出来，按主题分类。"
- "我想围绕这篇 review 做文献整理，后面还要接 Zotero 和 Obsidian。"
- "先别写代码，帮我把这个综述做成可执行的阅读工作流。"
- "根据这篇教程论文，给我出 survey map、reference list 和 reading roadmap。"
- "整理这篇综述的引用论文，并给出 Zotero 导入计划。"

## Fallback behavior

- If only abstract or partial text is available, still produce a reduced package and mark missing sections as partial or `unknown`.
- If the paper is clearly not a survey, review, tutorial, or position paper, say so and either:
  - continue in a reduced survey-like mode if the user still wants field navigation, or
  - hand off to a more appropriate paper-reading workflow.
- If metadata enrichment is weak or unavailable, keep `unknown` fields and continue with a manual planning path.
- If Zotero MCP or Obsidian write-back is unavailable, stay in planning-only mode and emit plans instead of pretending execution.
- If `citation_contexts.json` cannot be grounded, say so explicitly and only produce `citation-lineage.md` when the remaining evidence still supports a conservative related-work summary.

## Rules

- Keep human decisions at the center.
- Mark missing metadata as `unknown`.
- Distinguish source-grounded extraction from assistant inference.
- Treat reference enrichment as optional and best-effort, not as a guaranteed resolver pass.
- Prefer Semantic Scholar over Google Scholar for metadata enrichment; use Google Scholar only as optional third-party or manual fallback.
- Never claim Zotero import, PDF attachment, or PDF download succeeded unless the current run actually performed and verified it.
- Do not claim OCR, MinerU, or parser integrations unless they are actually available in the current environment.
- Do not pretend a full workflow completed when only a subset of outputs could be produced from the current source quality.
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
