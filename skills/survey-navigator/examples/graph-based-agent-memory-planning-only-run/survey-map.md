# Survey Map

## Source
- Survey title: Graph-based Agent Memory: Taxonomy, Techniques, and Applications
- Source type: markdown-example
- Access quality: structure-only
- Source locator: `skills/survey-navigator/examples/graph-based-agent-memory-example.md`
- Confidence note: This run does not use a real survey PDF or full-text Markdown. It uses the repo example as a structure-based workflow test.

## Scope
- Field / subfield: graph-based memory for LLM agents and related long-context retrieval or agent-memory systems
- Survey type: survey
- Stated motivation: organize the design space of graph-based agent memory, memory operations, application settings, and open problems
- Claimed coverage window: unknown

## Section Structure
1. Field orientation and survey framing
2. Memory representation taxonomy
3. Memory operations taxonomy
4. Application settings
5. Open problems and limits

## Taxonomy

### Memory representation
- Definition: how an agent stores persistent or semi-persistent knowledge in graph-like structures
- Representative subtopics: knowledge graphs; event graphs; hybrid memory graphs
- Source-grounded evidence: listed directly in the example file
- Assistant inference: this branch likely separates symbolic graph stores from hybrid graph-plus-vector or graph-plus-summary memory layers

### Memory operations
- Definition: how memory is retrieved, updated, consolidated, and forgotten over time
- Representative subtopics: retrieval; update; consolidation; forgetting
- Source-grounded evidence: listed directly in the example file
- Assistant inference: these operations likely connect memory quality to long-horizon planning and stale-memory control

### Application settings
- Definition: where graph-based agent memory is used in practice
- Representative subtopics: long-horizon planning; tool-using agents; multi-agent coordination
- Source-grounded evidence: listed directly in the example file
- Assistant inference: evaluation probably differs across simulated agents, retrieval-heavy QA systems, and embodied or tool-using environments

## Core Questions
- Q1: What graph structure is most useful for persistent agent memory?
- Q2: How should agents retrieve, update, and prune graph memory without drifting or growing unbounded?
- Q3: Which application settings actually benefit from graph memory rather than simpler retrieval stacks?

## Method Categories
- Category: graph memory representation
  - Summary: represent entities, events, and relations in explicit graph form
  - Strength: makes memory structure and relation paths inspectable
  - Limitation: requires graph construction and maintenance quality
- Category: retrieval and reasoning over memory
  - Summary: retrieve relevant subgraphs or paths to support planning and generation
  - Strength: can expose multi-hop relations better than flat chunk retrieval
  - Limitation: retrieval and traversal can be brittle when graphs are sparse or noisy

## System Categories
- Category: agent memory stack
  - Summary: combine memory storage, retrieval, update, and summarization inside the agent loop
  - Strength: supports persistent behavior over long tasks
  - Limitation: increases orchestration complexity and failure modes
- Category: graph-augmented retrieval system
  - Summary: use graph indexing or graph reasoning to improve long-context or knowledge-intensive tasks
  - Strength: may improve structured access to distributed evidence
  - Limitation: can require additional indexing and evaluation infrastructure

## Application Categories
- Category: long-horizon planning
  - Summary: reuse memory across multi-step tasks and long sessions
  - Typical use: task history, goals, and world-state updates
- Category: tool-using agents
  - Summary: retain tool outputs and relations between tasks, tools, and observations
  - Typical use: persistent workspaces or research assistants
- Category: multi-agent coordination
  - Summary: share or synchronize memory across collaborating agents
  - Typical use: role coordination and shared context graphs

## Benchmarks / Evaluation
- Benchmark or evaluation regime: long-context task evaluation
  - Purpose: test whether memory improves retrieval and task completion over long horizons
  - Notes: structure-only inference; no verified benchmark list extracted from the real survey
- Benchmark or evaluation regime: agent-task case studies
  - Purpose: compare memory usefulness in planning, tool use, or simulated social settings
  - Notes: structure-only inference; concrete benchmark names remain `unknown`

## Open Problems
- Open problem: scalable memory maintenance
  - Why it remains open: graph memory can grow faster than retrieval quality or update reliability
  - Evidence status: source-grounded from the example at a high level
- Open problem: noisy or stale memory pruning
  - Why it remains open: persistent memory quality degrades without explicit forgetting or repair
  - Evidence status: source-grounded from the example at a high level
- Open problem: evaluation beyond short benchmark tasks
  - Why it remains open: short tasks may not reveal long-term memory usefulness or failure
  - Evidence status: source-grounded from the example at a high level

## Boundaries And Uncertainty
- Missing sections: no real abstract, no full section list, no verified reference pages, no claimed coverage dates
- Weak evidence areas: benchmarks, venues, exact citation roles, and survey-specific terminology beyond the example
- Items requiring human review: whether the candidate references below are actually cited in the target survey; any DOI, venue, or import decisions
