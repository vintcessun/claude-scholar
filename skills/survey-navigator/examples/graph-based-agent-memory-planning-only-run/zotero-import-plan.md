# Zotero Import Plan

## Mode
- Zotero MCP available: no
- Write operations allowed: no
- Execution mode: planning-only
- Import strategy: manual DOI/arXiv import
- Plan type: manual

## Target Collection
- Proposed top collection: Agent Memory Surveys
- Proposed sub-collections:
  - Core Papers
  - Foundational
  - Methods
  - Systems
  - Benchmarks
  - Applications
  - To-Read

## Import Queue

| Title | Identifier type | Identifier | Proposed collection | Tags | Import status | Notes |
|---|---|---|---|---|---|---|
| Graph-based Agent Memory: Taxonomy, Techniques, and Applications | manual-review | unknown | Core Papers | survey; graph-memory; representative; must-read | pending | source object for this workflow; full citation still needed |
| Generative Agents: Interactive Simulacra of Human Behavior | manual-review | unknown | Applications | agent-memory; applications; representative; must-read | pending | verify whether cited by the survey before import |
| MemoryBank: Enhancing Large Language Models with Long-Term Memory | manual-review | unknown | Methods | memory-operations; methods; representative; must-read | pending | needs manual DOI/arXiv lookup |
| LONGMEM: Augmenting Large Language Models with Long-Term Memory | manual-review | unknown | Methods | memory-operations; methods; representative; must-read | pending | needs manual DOI/arXiv lookup |
| MemGPT: Towards LLMs as Operating Systems | manual-review | unknown | Systems | systems; representative; must-read | pending | needs manual DOI/arXiv lookup |
| HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models | manual-review | unknown | Methods | memory-representation; recent; method; must-read | pending | needs manual DOI/arXiv lookup |
| GraphReader: Building Graph-based Agent to Enhance Long-Context Abilities of Large Language Models | manual-review | unknown | Core Papers | graph-memory; recent; method; must-read | pending | likely high-priority verification target |
| RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval | manual-review | unknown | Benchmarks | retrieval; method; optional | pending | import only if kept as a comparison paper |
| Voyager: An Open-Ended Embodied Agent with Large Language Models | manual-review | unknown | Applications | applications; system; optional | pending | verify relevance to survey taxonomy |
| ReAct: Synergizing Reasoning and Acting in Language Models | manual-review | unknown | Foundational | foundational; method; optional | pending | import only if retained as a baseline |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | manual-review | unknown | Foundational | foundational; retrieval; optional | pending | import only if retained as a retrieval baseline |

## Tags
- topic: `graph-memory`
- taxonomy branch: `memory-representation`, `memory-operations`, `applications`, `retrieval`, `systems`
- role: `foundational`, `representative`, `recent`, `method`, `system`, `benchmark`
- priority: `must-read`, `optional`

## Dedupe Plan
- Preferred cleanup step: manual title check after import because no Zotero MCP execution is available in this run
- Duplicate risk: high for broad baseline papers that may already exist in a general LLM-agent collection
- Manual review needed: yes, for every item before import

## Manual Follow-Up
- Items with `unknown` DOI/arXiv: all rows in this planning-only test
- URL-only items: none confirmed
- Items requiring local PDF search: all rows if the user later wants attachment-level completeness
