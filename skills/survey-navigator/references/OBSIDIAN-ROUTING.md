# Obsidian Routing For Survey Navigator

`survey-navigator` is an entry workflow into the existing project KB, not a replacement for it.

## Default destinations

### 1. Survey source note

Store the source survey itself under:

```text
Sources/Papers/{survey-slug}.md
```

This note should capture:
- the survey metadata that is actually known
- scope and access limits
- taxonomy summary
- links to triaged cited papers when they later become canonical notes

### 2. Survey-derived synthesis

Store durable synthesized outputs under `Knowledge/`, for example:
- `Knowledge/{topic} Survey Map.md`
- `Knowledge/{topic} Reading Roadmap.md`
- `Knowledge/{topic} Paper Triage.md`

Keep these linked back to the survey source note.

### 3. Graph destination

Default graph artifact:

```text
Maps/literature.canvas
```

Do not create a dedicated survey canvas unless the user explicitly asks for one.

## Promotion boundary

- `Sources/Papers/` may contain partial metadata and working extraction notes.
- `Knowledge/` should only contain stable synthesis that can point back to the survey note or stronger paper notes.
- If triaged references are still weak, incomplete, or abstract-only, keep them as planning artifacts instead of durable claims.

## Recommended note relationships

```text
Sources/Papers/{survey-slug}.md
    -> Knowledge/{topic} Survey Map.md
    -> Knowledge/{topic} Reading Roadmap.md
    -> Knowledge/{topic} Paper Triage.md
    -> Maps/literature.canvas
```

## Daily and registry hygiene

If the repo is bound to an Obsidian KB and the user asks for actual write-back:
- update today's `Daily/` note with the survey-navigation work
- update project memory conservatively
- update hub or index notes only if the top-level project state changes
