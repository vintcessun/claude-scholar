# Notes: Survey Navigator Planning-Only Run

## Source Availability

### Repo search
- Query: `rg --files | rg "Graph-based Agent Memory|graph-based-agent-memory|agent-memory"`
- Result: only `skills/survey-navigator/examples/graph-based-agent-memory-example.md`
- Interpretation: there is no real survey PDF or parsed Markdown source inside the repo for this test target.

## Test Mode
- Mode: `planning-only`
- Evidence type: `structure-only`
- Reason: the example file explicitly says it demonstrates workflow shape and does not claim that the real survey has been fully parsed.

## Constraints Applied
- No `S2_API_KEY`
- No Google Scholar
- No Zotero MCP
- No Obsidian write-back
- `unknown` is preferred over invented metadata

## Candidate Reference Policy
- The reference list is a structure-based candidate list for workflow testing.
- It is not a verified bibliography extracted from the real survey.
- Titles may be real papers in the topic area, but citation inclusion in the target survey is not claimed unless verified.

## Enrichment Expectations
- The helper script is real and can be run in no-key mode.
- Because this environment may block network access, expected statuses include `api_error`, `not_found`, and `manual-review`.
- The markdown table should normalize ambiguous or skipped cases into `manual-review` when needed.

## Enrichment Run Result
- Command run: `python skills/survey-navigator/scripts/enrich_references_semantic_scholar.py --input skills/survey-navigator/examples/graph-based-agent-memory-planning-only-run/reference-list.json --output skills/survey-navigator/examples/graph-based-agent-memory-planning-only-run/enriched-references.json`
- Output file created: `skills/survey-navigator/examples/graph-based-agent-memory-planning-only-run/enriched-references.json`
- Status counts from the real run: `{"api_error": 11}`
- Observed behavior: literal `unknown` values in `doi` and `arxiv` were treated as queryable identifiers by the helper, which pushed all records down the API path instead of skipping missing identifiers.
