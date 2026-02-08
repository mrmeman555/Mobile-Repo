---
id: ml-os-architecture-vision
title: "ML OS Architecture Vision"
created: 2026-02-08
updated: 2026-02-08
desc: "Comprehensive architectural vision for ML OS: database-first data model, needs as atomic unit, agents as projections of shared state, recursive kernel governance, agent round table coordination, and the four-phase build sequence."
tags: ml-os, architecture, vision, needs, agents, kernel, round-table, mcp
source_transcript: .specstory/history/2026-02-03_01-57Z-sprint-methodology-workspace-design.md
---

# ML OS Architecture Vision

Date: 2026-02-08

## Why OS-Level Thinking Matters

An operating system mediates between raw capability and useful work. The CPU doesn't know what a "file" is; the OS creates that abstraction. The ML OS is the same problem applied to LLMs.

Traditional OS concerns map directly to ML OS concerns:

| Traditional OS | ML OS Equivalent |
|:---------------|:-----------------|
| **Memory management** — RAM allocation, virtual memory, GC | **Context window management** — what gets loaded, what gets evicted, what's referenced by pointer |
| **Process scheduling** — CPU time slicing, priority queues | **Agent spawning** — need-to-task graduation, which agent runs when, capacity allocation |
| **Inter-process communication** — pipes, sockets, shared memory | **Shared need state** — agents coordinating through a legible, queryable state layer |
| **File system** — hierarchical storage, inodes, caching | **Knowledge storage/retrieval/compilation** — the data layer that all views are compiled from |
| **Security & integrity** — permissions, sandboxing, isolation | **Epistemic contracts** — drift detection, identity immutability, guardrails |

Without understanding all five dimensions, we'd build something that works for a single agent with a hand-crafted prompt but shatters when ten agents need to coordinate over shared state with competing priorities and evolving needs.

The data model, need lifecycle, coordination protocol, and compilation pipeline aren't features to add later — they're the kernel. Getting them wrong means everything built on top inherits the defect.

---

## Database-First Data Model

### The Core Principle

**The database is the source of truth. Markdown files are compiled outputs.**

A markdown file with frontmatter is a document pretending to be a database record. You have to parse it to query it, lint it to enforce schema, and write custom scripts to extract relationships. Every operation that should be a simple `SELECT` becomes a file-walk-and-parse.

The correct model inverts this:

- **Schema enforcement is free** — the database rejects malformed data at insertion. No linters needed.
- **Queries are native** — "show me all needs in state X referencing artifact Y" is SQL, not a file crawl.
- **Relationships are first-class** — foreign keys or graph edges, not YAML references nobody validates.
- **Views are cheap and always accurate** — compiled on demand from current state. Never stale because never stored as source.
- **Multiple workspaces, same data** — different workspaces are different compilers pointing at the same database.

Markdown files still exist — agents and humans read markdown. But they're build artifacts, not source data. You wouldn't edit a compiled binary and expect the source to update.

### Three-Layer Architecture

```
Backend  (Data)       →  Structured database (SQLite / graph DB)
                          Needs, tasks, artifacts, relationships, agents
                          Enforced schema, native queries, first-class edges

Middle   (Retrieval)  →  MCP server + compiler scripts
                          Resolves references, computes indexes, assembles context packs
                          Manages context window budget per agent

Frontend (Views)      →  Computed markdown, context packs, agent boot payloads
                          PROBLEM.md, README.md, indexes — all generated, never authored
                          Different workspaces = different compilers, same data
```

---

## Needs as the Atomic Unit

Tasks are not the fundamental unit of work. **Needs** are.

- A **need** is a persistent, evolving state: *"The ML OS kernel must be testable across session boundaries."*
- A **task** is what happens when a need becomes actionable at a specific moment: *"Write a session-boundary test for the kernel boot sequence."*
- An **agent** is a compute instance spawned to execute a task, provisioned with exactly the data slice relevant to that task.

The lifecycle:

```
Need (persistent, evolving)
  │
  ├── becomes actionable ──► Task (concrete, time-bound)
  │                            │
  │                            ├── spawns ──► Agent (ephemeral, scoped)
  │                            │               │
  │                            │               └── completes ──► Result
  │                            │                                   │
  │                            └── updates state ◄─────────────────┘
  │
  └── state changes based on results
```

The MCP server's primary responsibility is **need state management** — not task CRUD. It tracks what needs exist, what data they reference, when they become actionable, what tasks have been generated from them, and what the outcomes were. Tasks and agents are downstream. Needs are the source.

PROBLEM.md is not a file you maintain. It's a compiled view:
`SELECT * FROM needs WHERE scope = 'Sprint_X' AND status != 'resolved' ORDER BY priority` — rendered to markdown.

---

## Agents as Projections of Shared State

Each agent is not an independent entity with private knowledge. Agents are **different projections of the same underlying state**, each filtered through a different lens (identity, assigned needs, capacity constraints).

Same database. Different `WHERE` clauses. Different compiled context packs.

- **Agent A** (ML OS Architect): sees needs tagged `kernel`, `architecture`, `methodology`. Prioritizes structural coherence.
- **Agent B** (Context Manager): sees needs tagged `context`, `retrieval`, `compilation`. Prioritizes information accuracy.
- **Agent C** (Workspace Janitor): sees needs tagged `cleanup`, `schema`, `enforcement`. Prioritizes organizational hygiene.

Each agent has "competing immediate needs" because they're looking at overlapping subsets of the same need graph with different priority weightings. The tension is productive — different perspectives on shared information produce better outcomes than a single perspective on private information.

The capacity constraint (context window + tool access) is the resource budget. The MCP server provisions each agent with the highest-value data slice given its current needs and capacity.

---

## Recursive Kernel Governance

The kernel is not a static prompt or a flat config file. It's a **governance protocol that operates at every level of the system simultaneously**, structured as three concentric layers present in every agent:

### Layer 1 — Identity (Immutable)
Who am I? What do I never violate? What is the one objective I exist to serve?
- Doesn't change within a session, across sessions, or across platforms.
- In code terms: hardcoded constants, not configuration.

### Layer 2 — Awareness (Dynamic)
What needs exist? What's their state? What am I monitoring? When should I act?
- Changes constantly as the need graph evolves.
- In code terms: the MCP server's state, queried in real-time.

### Layer 3 — Execution (Ephemeral)
What task am I doing right now? What data do I have? What tools can I use?
- Scoped to a single agent session.
- In code terms: the compiled context pack + tool permissions.

Layer 2 recurses: an agent monitoring needs is itself a need-satisfying process. The system that tracks needs is itself subject to needs (reliability, accuracy, freshness). This recursion is autopoietic closure — the system that produces itself as a byproduct of doing its job.

---

## Agent Round Table Coordination

### The Mechanism

Multiple agents coordinate not through a central scheduler, but through **shared visibility into the global need state**:

1. All agents share visibility into the global need state (or the relevant subset).
2. Each agent has specific needs it's responsible for (primary scope).
3. Each agent monitors adjacent needs (peripheral awareness, from Layer 2).
4. When a monitored need goes unmet and an agent has capacity, it **takes over**.
5. All agents' continued relevance stakes on the collective outcome.

Coordination emerges from shared state visibility and individual incentive alignment. Each agent acts locally based on what it sees in the global need graph, and the system converges because all agents optimize for the same root objective (the kernel's `grow` directive), just through different lenses.

### Why Google Degraded Their Deep Research

Google's agent round table (Deep Research) was degraded — they hid the agent thinking and reduced the coordination quality. The reason: **they couldn't solve the prioritization problem.**

When multiple agents have competing views on what matters most and there's no shared state making those priorities legible to each other, you get deadlock (everyone defers) or thrashing (everyone overrides). Hiding the thoughts hides the problem. The solution isn't better algorithms — it's **better shared state**. If every agent can see the need graph, see what's being worked on, and see what's going unmet, the coordination problem becomes tractable because the information asymmetry disappears.

---

## Enforceability: Code, Not Convention

Every rule in the system must be either:

- **A linter** — checks schema, validates structure at insertion time
- **A generator** — computes views, builds context packs, renders PROBLEM.md
- **A guard** — MCP server rejects operations that violate invariants

No human-maintained indexes. No manually updated PROBLEM files. No convention that depends on someone remembering to do something. If the system can't verify it programmatically, it doesn't exist as a rule.

This is why the Python bootloader / computed kernel concept is essential for the long term. Convention-based systems decay. Code-based systems don't.

---

## Multi-Workspace, Same Data

Different workspaces are different compilers pointing at the same database:

- The **ML OS build workspace** sees needs tagged `kernel`, `mcp`, `schema` — focused on building the system itself.
- The **daily workspace** sees needs tagged with today's date or active sprint scopes — focused on execution.
- The **mobile repo** sees needs tagged `mobile`, `portable` — focused on cross-platform access.

All projections of the same underlying state. Changes in one are immediately visible to all because they share the data layer.

---

## Dendron/FOAM Evaluation

Explored Dendron and FOAM as potential knowledge management / graph visualization layers:

- **Dendron**: Discontinued. No longer viable.
- **FOAM**: Lightweight, VS Code native, but primarily designed for human note-taking, not agent-driven systems.

**Conclusion**: The frontend presentation layer is the least important concern when all agent interfacing happens through Cursor and the MCP server. The database + compiler architecture handles everything FOAM/Dendron would have provided (hierarchical organization, cross-references, graph relationships), but programmatically rather than through a UI extension. If graph visualization becomes needed later, it can be added as a view compiled from the database.

---

## Transcript-to-Note Provenance

Every meta note tracks a `source_transcript` field in its frontmatter, linking the distilled note back to the full conversation where the ideas emerged. This creates a provenance chain:

```
Transcript (episodic memory — full reasoning trace)
    │
    └── distilled into ──► Note (semantic extraction — structured summary)
                              │
                              └── referenced by ──► Agent (when deeper context needed,
                                                         trace back to primary source)
```

In the future database model, this becomes a `source_transcript` relationship edge on every artifact, enabling any agent to "zoom in" from summary to full context on demand.

---

## Build Sequence

### Phase 1 — New Workspace + Database Schema
- Spin up isolated ML OS build workspace (clean rules, no cross-contamination)
- Design core database schema: `needs`, `tasks`, `artifacts`, `relationships`, `agents`
- Database is the source of truth. No markdown files as source data.

### Phase 2 — The MCP Server
- Build as the need state manager (not just task CRUD)
- Handles: need creation, need-to-task graduation, task-to-agent assignment, artifact registration, relationship tracking
- Compiles: PROBLEM.md views, context packs, agent boot payloads
- Enforces: schema validation, relationship integrity, state transitions

### Phase 3 — The Compiler Layer
- Build scripts that generate markdown views from database state
- PROBLEM.md, README.md, indexes — all compiled, never hand-authored
- Context packs assembled on demand by querying the database for relevant artifact slices

### Phase 4 — Multi-Agent Coordination
- Agent round table protocol: shared need visibility, takeover rules, priority resolution
- Kernel becomes the governance protocol instantiated in every agent
- Test with real workloads: does coordination emerge from shared state, or does it need explicit scheduling?

Phase 1 is the foundation. Phase 2 is the engine. Phase 3 is the interface. Phase 4 is the intelligence.
