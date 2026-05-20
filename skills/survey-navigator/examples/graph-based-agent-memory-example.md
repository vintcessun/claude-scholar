# Example: Graph-based Agent Memory survey navigation

## Example prompt

```text
Use $survey-navigator on the survey "Graph-based Agent Memory: Taxonomy, Techniques, and Applications".

I want:
1. a field map,
2. a conservative `reference-list.json`,
3. a taxonomy of the cited papers,
4. a `citation-lineage.md` that reads like a related-work evolution map,
5. citation contexts as a machine-readable intermediate artifact,
6. a Zotero import plan,
7. an Obsidian export plan,
8. a reading roadmap for beginner / research / engineering tracks.

Do not fabricate citation metadata. If any field is missing from the survey or reference list, mark it as unknown.
Keep the output human-in-the-loop and make the uncertainty visible.
Do not pretend Zotero import or Obsidian write-back already happened.
```

## Expected output structure

### `reference-list.json`

```json
[
  {
    "title": "Example paper A",
    "authors": "unknown",
    "year": "2024",
    "venue": "arXiv",
    "doi": "unknown",
    "arxiv": "2401.xxxxx",
    "url": "unknown"
  }
]
```

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

### `citation-lineage.md`

```md
# Citation Lineage

## 1. Foundational Papers
- Problem addressed: define why memory matters for LLM agents before graph-specific design.
- Relation to previous stage: starting point.
- Representative papers:
  - [8] Cognitive architectures for language agents — frames memory as part of the broader agent architecture.

## 2. Structural Memory
- Problem addressed: move from flat memory views toward explicit structure.
- Relation to previous stage: extends foundational agent-memory ideas into more organized representations.
- Representative papers:
  - [20] On the structural memory of llm agents — clarifies why structured memory is not just storage.

## 3. Graph Memory
- Problem addressed: represent relations, time, and hierarchy in memory.
- Relation to previous stage: specializes structural memory into graph-oriented formulations.
- Representative papers:
  - [18] Zep: a temporal knowledge graph architecture for agent memory — representative temporal graph direction.

## 4. Retrieval / Reasoning
- Problem addressed: make stored memory usable for recall and long-horizon reasoning.
- Relation to previous stage: turns graph memory from representation into operational support.
- Representative papers:
  - [17] Hierarchical memory for high-efficiency long-term reasoning in llm agents
  - [35] SGMem: Sentence graph memory for long-term conversational agents
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

### `citation_contexts.json`

```json
[
  {
    "citation_number": 18,
    "section": "I. INTRODUCTION",
    "subsection": "unknown",
    "surrounding_text": "..."
  }
]
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

## Example artifact

See [graph-based-agent-memory-citation-lineage.md](./graph-based-agent-memory-citation-lineage.md) for a compact related-work evolution example based on the current Graph-based Agent Memory survey workflow.
