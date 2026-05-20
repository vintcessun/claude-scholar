# Enriched Reference Table

## Run Context
- Mode: planning-only
- Source evidence: structure-only
- Resolver attempted: Semantic Scholar helper in no-key mode
- Real run output: `enriched-references.json`
- Status summary from the real run: `11 api_error`
- Important note: this run used `unknown` in missing DOI/arXiv fields as required by the test. The current helper treated those literal strings as identifiers and attempted API calls instead of skipping them.

| Original reference | Match status | Title | Authors | Year | Venue | Abstract | citationCount | influentialCitationCount | externalIds | URL | openAccessPdf | fieldsOfStudy | Resolver | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Graph-based Agent Memory: Taxonomy, Techniques, and Applications | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; structure-only survey object; manual review required |
| Generative Agents: Interactive Simulacra of Human Behavior | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; candidate reference not verified against the real survey bibliography |
| MemoryBank: Enhancing Large Language Models with Long-Term Memory | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; manual DOI/arXiv follow-up required |
| LONGMEM: Augmenting Large Language Models with Long-Term Memory | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; manual DOI/arXiv follow-up required |
| MemGPT: Towards LLMs as Operating Systems | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; manual DOI/arXiv follow-up required |
| HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; manual DOI/arXiv follow-up required |
| GraphReader: Building Graph-based Agent to Enhance Long-Context Abilities of Large Language Models | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; candidate reference not verified against the real survey bibliography |
| RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; manual DOI/arXiv follow-up required |
| Voyager: An Open-Ended Embodied Agent with Large Language Models | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; manual DOI/arXiv follow-up required |
| ReAct: Synergizing Reasoning and Acting in Language Models | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; manual DOI/arXiv follow-up required |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | api_error | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | semantic-scholar | Real helper run returned `api_error`; manual DOI/arXiv follow-up required |

## Status Policy For This Test
- `api_error` came from the real helper execution.
- `matched`, `manual-review`, and `not_found` did not appear in this run.
- If a later run returns `ambiguous` or `skipped`, they should be normalized to `manual-review` in this markdown layer.
