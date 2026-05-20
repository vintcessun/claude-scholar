# Reading Roadmap

## Reading Goal
- Topic: graph-based agent memory and related long-term memory systems for LLM agents
- Starting survey: Graph-based Agent Memory: Taxonomy, Techniques, and Applications
- Decision focus: decide whether graph-based memory is a distinct design space worth deeper reading beyond generic RAG or agent baselines

## Beginner Path

### Step 1
- Paper: Graph-based Agent Memory: Taxonomy, Techniques, and Applications
- Why now: establishes the working taxonomy for this test
- What to extract: memory representation branches, memory operations, application settings, and open problems
- Stop condition: you can explain the three major branches without looking back at the survey map

### Step 2
- Paper: Generative Agents: Interactive Simulacra of Human Behavior
- Why now: gives an intuitive application-level picture of persistent memory in agents
- What to extract: what "memory" changes in agent behavior and what parts are task-state versus long-term memory
- Stop condition: you can distinguish persistent agent memory from one-shot prompting

### Step 3
- Paper: ReAct: Synergizing Reasoning and Acting in Language Models
- Why now: provides a non-memory baseline for reasoning-and-action loops
- What to extract: where memory enters the loop and where plain reasoning/acting is still enough
- Stop condition: you can describe when memory augmentation is necessary versus optional

## Research Path

### Step 1
- Paper: Graph-based Agent Memory: Taxonomy, Techniques, and Applications
- Why now: start from the taxonomy and open-problem framing
- What to extract: candidate claims about representation, update, forgetting, and evaluation
- Open tension: the survey source is not verified in full text in this run, so every specific claim needs later source confirmation

### Step 2
- Paper: GraphReader: Building Graph-based Agent to Enhance Long-Context Abilities of Large Language Models
- Why now: likely closest representation-heavy candidate in the current test set
- What to extract: how the graph is built, queried, and integrated into the agent loop
- Open tension: actual citation inclusion in the target survey is unverified

### Step 3
- Paper: HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models
- Why now: offers a structured memory formulation that may challenge or extend the survey taxonomy
- What to extract: memory representation, retrieval mechanism, and evaluation setup
- Open tension: whether graph memory produces benefits distinct from other structured retrieval schemes

### Step 4
- Paper: MemoryBank: Enhancing Large Language Models with Long-Term Memory
- Why now: useful for update and persistence comparisons
- What to extract: how memory is stored, updated, and reused across sessions
- Open tension: whether graph structure is essential or whether simpler memory stores are enough

## Engineering Path

### Step 1
- Paper: MemGPT: Towards LLMs as Operating Systems
- Why now: system-level framing is helpful before implementation work
- What to extract: memory hierarchy assumptions, orchestration boundaries, and failure modes
- Implementation note: translate memory ideas into components, not just citations

### Step 2
- Paper: LONGMEM: Augmenting Large Language Models with Long-Term Memory
- Why now: likely relevant for long-context augmentation design
- What to extract: storage format, retrieval trigger, and context insertion strategy
- Implementation note: compare memory benefit against token cost and control complexity

### Step 3
- Paper: RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- Why now: engineering comparison point for structured retrieval
- What to extract: indexing pipeline, retrieval latency trade-offs, and evaluation assumptions
- Implementation note: use as a contrast class if graph memory seems too operationally heavy

### Step 4
- Paper: Voyager: An Open-Ended Embodied Agent with Large Language Models
- Why now: useful for long-horizon agent behavior under realistic task progression
- What to extract: what persistent memory changes in execution quality and adaptation
- Implementation note: focus on task-loop integration rather than only memory storage design

## Cross-Path Notes
- Shared prerequisites: verify actual survey bibliography and collect real DOI/arXiv identifiers before any import work
- Papers to defer: any candidate reference whose relevance to graph-based memory stays weak after survey verification
- Items blocked by missing metadata or access: all identifier-based import steps and any stable claim promotion into `Knowledge/`
