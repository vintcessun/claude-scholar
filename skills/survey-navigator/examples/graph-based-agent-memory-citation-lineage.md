# Citation Lineage

## Source

- Survey title: Graph-based Agent Memory: Taxonomy, Techniques, and Applications
- Source type: real PDF intake
- Evidence basis:
  - real section structure
  - `citation_contexts.json`
  - `paper-triage-table.md`
  - `survey-map.md`
- Confidence note: this artifact is a conservative related-work summary built from the current real PDF workflow. It is human-readable by design and does not attempt sentence-perfect citation reconstruction.

## 1. Foundational Papers

- Problem addressed: explain why agent memory is a core module in LLM-based agents before the survey narrows into graph-based formulations.
- Relation to previous stage: starting point.
- Representative papers:
  - [8] Cognitive architectures for language agents — establishes a broader architecture view in which memory is one subsystem rather than an isolated store.
  - [9] Personal LLM agents: Insights and survey about the capability, efficiency and security — widens the framing toward personalization, efficiency, and safety concerns that later memory systems must handle.

## 2. Structural Memory

- Problem addressed: move from unstructured memory buffers toward explicit internal organization.
- Relation to previous stage: extends the foundational motivation by asking how memory should be structured, not only why it is needed.
- Representative papers:
  - [20] On the structural memory of llm agents — provides a direct bridge from generic agent memory to structured memory design.
  - [81] MemoryBank: Enhancing large language models with long-term memory — serves as a useful contrast point between long-term memory utility and explicitly graph-based structure.

## 3. Graph Memory

- Problem addressed: represent entities, relations, temporal order, and hierarchy in a form that can support longer-lived agent behavior.
- Relation to previous stage: specializes structural memory into graph-oriented representations that can encode richer relationships.
- Representative papers:
  - [18] Zep: a temporal knowledge graph architecture for agent memory — the clearest cross-section representative paper in the survey for temporal graph memory.
  - [28] Optimus-1: Hybrid multimodal memory empowered agents excel in long-horizon tasks — shows a hybrid memory direction that combines graph-style structure with multimodal and long-horizon needs.

## 4. Retrieval / Reasoning

- Problem addressed: turn stored memory into actionable recall for reasoning, continuity, and task execution.
- Relation to previous stage: shifts from representation design to operational use of memory in inference and planning.
- Representative papers:
  - [17] Hierarchical memory for high-efficiency long-term reasoning in llm agents — emphasizes long-term reasoning efficiency.
  - [35] SGMem: Sentence graph memory for long-term conversational agents — shows how graph memory can support long-term conversational continuity.
  - [31] Mem 0: Building production-ready ai agents with scalable long-term memory — connects retrieval and production constraints.

## 5. Reflective / Evolutionary Memory

- Problem addressed: keep memory updated through reflection, self-evolution, and accumulated interaction history.
- Relation to previous stage: extends retrieval-centric systems into adaptive systems that revise and grow memory over time.
- Representative papers:
  - [31] Mem 0: Building production-ready ai agents with scalable long-term memory — appears across extraction, storage, retrieval, evolution, and open-source sections.
  - [81] MemoryBank: Enhancing large language models with long-term memory — relevant to long-term accumulation and maintenance.

## 6. Benchmarks

- Problem addressed: evaluate whether better memory structures and update schemes actually improve long-context or continual-learning behavior.
- Relation to previous stage: moves from building memory systems to measuring them.
- Representative papers:
  - [129] MemoryBench: A benchmark for memory and continual learning in llm systems — a direct benchmark anchor in the survey.

## 7. Applications

- Problem addressed: demonstrate where graph-based or structured agent memory matters in practice.
- Relation to previous stage: tests whether the memory design lines above survive contact with real tasks and domains.
- Representative papers:
  - [35] SGMem: Sentence graph memory for long-term conversational agents — conversational agents.
  - [44] FinMem: A performance-enhanced llm trading agent with layered memory and character design — financial agents.
  - [180] AgentMental: An interactive multi-agent framework for explainable and adaptive mental health assessment — medical and health agents.

## 8. Open Problems

- Problem addressed: identify what still blocks reliable, scalable, and trustworthy graph-based agent memory.
- Relation to previous stage: reflects on the limits exposed by both technical designs and real-world applications.
- Survey anchors:
  - memory graph quality
  - scalability and efficiency
  - privacy and security
  - dynamic schema learning and knowledge transfer
  - interpretability and trustworthy operation
  - theoretical foundations
  - memory coordination in multi-agent systems

## Notes

- `citation-lineage.md` is not a reading order.
- `reading-roadmap.md` should still be used for beginner / research / engineering paths.
- `citation_contexts.json` remains the machine-oriented intermediate artifact for citation-to-section grounding.
