# Example: Graph-based Agent Memory survey navigation

## Example prompt

```text
Use $survey-navigator on the survey "Graph-based Agent Memory: Taxonomy, Techniques, and Applications".

I want:
1. a field map,
2. a taxonomy of the cited papers,
3. a reading roadmap for beginner / research / engineering tracks,
4. a Zotero import plan,
5. an Obsidian export plan.

Do not fabricate citation metadata. If any field is missing from the survey or reference list, mark it as unknown.
Keep the output human-in-the-loop and make the uncertainty visible.
```

## Expected output structure

### `survey-map.md`

```md
# Survey Map

## Source
- Survey title: Graph-based Agent Memory: Taxonomy, Techniques, and Applications
- Source type: pdf
- Access quality: partial text

## Scope
- Field / subfield: agent memory for LLM agents with graph-based structures
- Survey type: survey

## Taxonomy
### Memory representation
- knowledge graphs
- event graphs
- hybrid memory graphs

### Memory operations
- retrieval
- update
- consolidation
- forgetting

### Application settings
- long-horizon planning
- tool-using agents
- multi-agent coordination

## Open Problems
- scalable memory maintenance
- noisy or stale memory pruning
- evaluation beyond short benchmark tasks
```

### `paper-triage-table.md`

```md
| Taxonomy branch | Title | Authors | Year | Venue | DOI | arXiv | URL | Role labels | Priority | Why it matters | Metadata status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| memory representation | Example paper A | unknown | 2024 | arXiv | unknown | 2401.xxxxx | unknown | foundational; method | must-read | defines one graph memory formulation | partial |
| application settings | Example paper B | unknown | 2025 | unknown | unknown | unknown | https://example.org | system; recent | optional | shows deployment-style agent memory use | unknown-heavy |
```

### `reading-roadmap.md`

```md
# Reading Roadmap

## Beginner Path
- Start from the survey itself to learn the taxonomy and terminology.
- Read one foundational graph-memory formulation paper.
- Read one representative application paper for long-horizon agents.

## Research Path
- Read the survey, then the taxonomy-defining papers for memory representation.
- Follow with papers that expose unresolved retrieval, update, and evaluation tensions.
- End with recent works that challenge or extend the survey taxonomy.

## Engineering Path
- Read the survey sections on systems and evaluation.
- Focus on implementation-heavy papers with reproducible components.
- Compare benchmark setup, memory cost, and failure modes before building.
```

### `zotero-import-plan.md`

```md
# Zotero Import Plan

## Target Collection
- Proposed top collection: Agent Memory Surveys
- Proposed sub-collections:
  - Core Papers
  - Methods
  - Systems
  - Benchmarks
  - To-Read

## Import Queue
| Title | Identifier type | Identifier | Proposed collection | Tags | Import status | Notes |
|---|---|---|---|---|---|---|
| Graph-based Agent Memory: Taxonomy, Techniques, and Applications | url | unknown | Core Papers | survey; graph-memory; must-read | pending | create source note first |
```

### `obsidian-export-plan.md`

```md
# Obsidian Export Plan

## Source Note
- Destination: Sources/Papers/graph-based-agent-memory-taxonomy-techniques-and-applications.md

## Knowledge Notes
- Knowledge/Agent Memory Survey Map.md
- Knowledge/Agent Memory Reading Roadmap.md
- Knowledge/Agent Memory Paper Triage.md

## Graph Routing
- Default graph target: Maps/literature.canvas
```

## What this example is for

- It demonstrates format and workflow shape.
- It does not claim the real survey has already been fully parsed.
- It keeps missing metadata visible instead of guessed.
