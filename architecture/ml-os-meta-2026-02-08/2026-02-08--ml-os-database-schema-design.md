---
id: ml-os-database-schema-design
title: "ML OS Database Schema Design Notes"
created: 2026-02-08
updated: 2026-02-08
desc: "Emerging schema design for the ML OS data layer: needs, tasks, artifacts, relationships, and agents as first-class tables. SQLite starting point with graph DB evolution path."
tags: ml-os, schema, database, design, sqlite, graph-db
source_transcript: .specstory/history/2026-02-03_01-57Z-sprint-methodology-workspace-design.md
---

# ML OS Database Schema Design Notes

Date: 2026-02-08

## Design Principles

1. **Database is source of truth** — all markdown files, context packs, and views are compiled from structured data. No file is ever hand-maintained as a primary record.
2. **Needs are atoms** — the schema centers on needs, not tasks. Tasks are derived from needs when they become actionable.
3. **Relationships are first-class** — edges between entities are stored explicitly, not inferred from text references.
4. **Schema enforcement at insertion** — malformed data is rejected by the database, not caught by linters after the fact.
5. **Every entity has provenance** — source transcript, creation context, and modification history are tracked.

---

## Core Tables

### `needs`

The fundamental atomic unit. A need is a persistent, evolving state that the system must satisfy.

| Column | Type | Description |
|:-------|:-----|:------------|
| id | INTEGER PK | Auto-increment |
| title | TEXT NOT NULL | Human-readable name |
| description | TEXT | Full description of the need |
| status | TEXT NOT NULL | `identified`, `active`, `actionable`, `in_progress`, `resolved`, `deferred` |
| priority | INTEGER | 1 (critical) to 5 (background) |
| scope | TEXT | Which domain/sprint/project this need belongs to |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |
| source_transcript | TEXT | Path to transcript where need was first identified |
| parent_need_id | INTEGER FK | Self-referential — needs can be nested |

Needs have a lifecycle: `identified → active → actionable → in_progress → resolved`. A need becoming `actionable` is the trigger for task generation.

### `tasks`

Concrete actions derived from needs. A task exists because a need reached the `actionable` state.

| Column | Type | Description |
|:-------|:-----|:------------|
| id | INTEGER PK | Auto-increment |
| need_id | INTEGER FK | Which need this task was derived from |
| description | TEXT NOT NULL | What specifically to do |
| status | TEXT NOT NULL | `open`, `assigned`, `in_progress`, `completed`, `failed`, `cancelled` |
| priority | INTEGER | Inherited from need but can be overridden |
| assigned_agent_id | INTEGER FK | Which agent instance is working on this |
| result | TEXT | Outcome description upon completion |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |
| assigned_date | TEXT | Date the task was assigned |
| source_transcript | TEXT | Path to transcript where task was created |

### `artifacts`

Every document, file, note, code object, or data asset in the system.

| Column | Type | Description |
|:-------|:-----|:------------|
| id | INTEGER PK | Auto-increment |
| title | TEXT NOT NULL | Human-readable name |
| description | TEXT | What this artifact contains / is for |
| file_path | TEXT | Physical location on disk (if applicable) |
| artifact_type | TEXT | `document`, `code`, `config`, `context_pack`, `transcript`, `image`, `schema` |
| content_hash | TEXT | SHA256 of current content (for change detection) |
| created_at | TEXT | ISO timestamp |
| updated_at | TEXT | ISO timestamp |
| source_transcript | TEXT | Path to transcript where artifact was created |

Artifacts are registered in the database when created. The file on disk is the content; the database record is the metadata and index entry.

### `relationships`

Explicit edges between any two entities in the system. This is where graph DB capabilities shine — but can start as a simple join table in SQLite.

| Column | Type | Description |
|:-------|:-----|:------------|
| id | INTEGER PK | Auto-increment |
| source_type | TEXT NOT NULL | `need`, `task`, `artifact`, `agent` |
| source_id | INTEGER NOT NULL | ID in the source table |
| target_type | TEXT NOT NULL | `need`, `task`, `artifact`, `agent` |
| target_id | INTEGER NOT NULL | ID in the target table |
| relationship_type | TEXT NOT NULL | `derived_from`, `references`, `blocks`, `enables`, `monitors`, `produced`, `consumed` |
| metadata | TEXT | JSON blob for additional edge properties |
| created_at | TEXT | ISO timestamp |

Relationship types define the semantics of how entities connect:
- `derived_from` — task derived from need, artifact produced by task
- `references` — artifact references another artifact
- `blocks` — need/task blocks another need/task
- `enables` — resolution of one need enables another
- `monitors` — agent monitors a need (for round table coordination)
- `produced` — agent produced this artifact
- `consumed` — agent was provisioned with this artifact

### `agents`

Records of agent instances — not the agent definition, but each specific invocation.

| Column | Type | Description |
|:-------|:-----|:------------|
| id | INTEGER PK | Auto-increment |
| agent_type | TEXT NOT NULL | `architect`, `context_manager`, `janitor`, `researcher`, etc. |
| status | TEXT NOT NULL | `provisioning`, `active`, `completed`, `failed` |
| kernel_version | TEXT | Which kernel version was loaded |
| provisioned_artifacts | TEXT | JSON array of artifact IDs provided to this agent |
| assigned_tasks | TEXT | JSON array of task IDs assigned |
| monitored_needs | TEXT | JSON array of need IDs this agent is watching |
| session_transcript | TEXT | Path to transcript for this agent's session |
| started_at | TEXT | ISO timestamp |
| completed_at | TEXT | ISO timestamp |
| result_summary | TEXT | What the agent accomplished |

---

## Compiled Views (Not Stored — Generated on Demand)

### PROBLEM.md

```sql
SELECT n.title, n.description, n.status, n.priority
FROM needs n
WHERE n.scope = :scope AND n.status NOT IN ('resolved', 'deferred')
ORDER BY n.priority ASC, n.updated_at DESC;
```

Rendered to markdown with headers, status indicators, and links to related artifacts.

### Context Pack (Agent Boot Payload)

```sql
SELECT a.file_path, a.title, a.description, a.artifact_type
FROM artifacts a
JOIN relationships r ON r.target_type = 'artifact' AND r.target_id = a.id
JOIN needs n ON r.source_type = 'need' AND r.source_id = n.id
WHERE n.id IN (:assigned_need_ids)
ORDER BY a.artifact_type, a.title;
```

Assembled as a directory or concatenated document with routing metadata.

### Index / README

```sql
SELECT a.title, a.description, a.file_path, a.artifact_type, a.updated_at
FROM artifacts a
WHERE a.file_path LIKE :scope_path || '%'
ORDER BY a.updated_at DESC;
```

---

## Storage Engine Considerations

### SQLite (Starting Point)

- Simple, file-based, zero-config
- Handles all core tables and basic relationships
- The `relationships` table acts as a manual edge table (no native graph traversal)
- Good enough for hundreds to low thousands of entities
- The current TaskEngine already uses SQLite — this extends that foundation

### Graph DB (Evolution Path)

- Native graph traversal makes relationship queries fast and expressive
- "Find all artifacts 2 hops from this need" becomes a single query instead of recursive CTEs
- Better for the round table: "which agents are monitoring needs adjacent to this one?"
- Candidates: Neo4j (heavy), DuckDB (analytical), or a lightweight embedded graph like kuzu
- Migration path: export SQLite tables + relationships → import as nodes + edges

### Decision

Start with SQLite. The `relationships` table gives us the data model of a graph even without graph query semantics. When traversal queries become a bottleneck (Phase 4 — multi-agent coordination), migrate to a graph DB. The schema is designed to make that migration straightforward.

---

## Frontmatter Schema (For Compiled Markdown Outputs)

When the compiler generates markdown files from database state, each file gets frontmatter derived from the database record:

```yaml
---
id: [from DB record]
title: [from DB record]
created: [from DB record]
updated: [from DB record]
desc: [from DB record]
tags: [derived from relationships/scope]
source_transcript: [from DB record]
compiled_at: [timestamp of compilation]
---
```

The `compiled_at` field distinguishes generated files from source files. Any file with `compiled_at` in its frontmatter is a build artifact and should never be edited directly.

---

## Relationship to Existing TaskEngine

The current TaskEngine (`/mnt/share/Meta/Tools/TaskEngine/`) manages a single `tasks` table. This schema supersedes and extends it:

- The existing `tasks` table maps to the new `tasks` table with additional fields (need_id, assigned_agent_id, result)
- The existing `sprint_context` maps roughly to `needs.scope`
- The existing `source_line` / `source_transcript` concepts carry forward
- Migration path: extend the current SQLite DB with new tables, then migrate existing tasks to link to needs

No existing data is lost. The schema grows around what exists.
