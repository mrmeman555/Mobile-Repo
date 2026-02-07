# ML OS Nervous System — Design Brief

> **Status:** Concept (not yet designed or implemented)
> **Date:** 2026-02-06
> **Source:** Design conversation in `05_Transcript/Session_2026-02-06.md`

---

## 1. The Problem

Conversations in Cursor produce rich design thinking — decisions, alternatives considered, architectural insights, rationale — but this knowledge is trapped in raw `.specstory/history/` transcript files. These transcripts are:

- **Unstructured** — thousands of lines of interleaved user messages and agent responses
- **Unsearchable by topic** — you can grep for exact strings but not for "conversations about the nervous system"
- **Disconnected from tasks** — a task ID like #160 exists in the Task Engine (SQLite), but the design discussion that shaped it is buried in a transcript
- **Not observable in real-time** — no agent or tool monitors conversations as they happen

The current workaround is `task_context.py` (in `03_Infrastructure/`), which searches transcripts for task ID patterns and returns surrounding context. This works but is reactive (you must ask) and limited to task IDs (can't search by topic, decision, or concept).

---

## 2. The Concept: Three-Layer Architecture

The Nervous System separates three concerns:

### Layer 1: The Watcher (Sensory Layer — Perception)

A **CLI daemon** that monitors `.specstory/history/` for file changes. When a transcript is updated (new message added), the watcher:

1. Reads the delta (new content since last check)
2. Runs a lightweight extraction pass (LLM or rule-based) to identify:
   - **Topics discussed** (ML OS, Net+, IP-Lock, etc.)
   - **Task IDs referenced** (#155, #160, etc.)
   - **Files mentioned** (paths)
   - **Decisions made** ("DECISION: markdown first, Python later")
   - **Artifacts created** (new files, new tasks)
   - **Open questions** (things left unresolved)
3. Appends a structured entry to the chat index

The watcher runs silently in the background. The working agents never have to think about indexing. They just work.

### Layer 2: The Index (Memory Layer — Short-Term Memory)

A **structured, queryable store** (likely SQLite, consistent with the Task Engine) that holds extracted metadata:

```
Entry:
  - transcript_file: "2026-02-06_04-10Z-runtime-grounding-sequence.md"
  - message_range: "lines 8500-8650"
  - timestamp: "2026-02-06T08:30:00Z"
  - topics: ["nervous_system", "ml_os", "context_pack"]
  - task_ids: [157, 158, 160]
  - files_mentioned: ["task_context.py", "publish_to_bridge.py"]
  - decisions: ["Use routing table not playbooks", "Transcripts are source of truth"]
  - artifacts_created: ["NervousSystem_ContextPack/"]
  - open_questions: ["How does watcher detect deltas?", "LLM vs rule-based extraction?"]
```

This replaces raw transcript grep with structured queries:
- "What conversations discussed the nervous system?"
- "What decisions were made about ML OS this week?"
- "Which transcripts reference task #160?"
- "What open questions remain from today?"

### Layer 3: The Compiler (Cortex Layer — Synthesis)

A **doc compiler agent** that reads the index, pulls relevant transcript sections, and generates documentation artifacts on demand. Documents become "materialized views" of the conversation data:

- "Generate a design spec for the Nervous System" → compiler queries index for all nervous system entries → pulls transcript sections → synthesizes into a structured spec
- "What's the current state of ML OS?" → compiler queries index for all ML OS entries from last 7 days → generates a status report

The compiler doesn't create documents from scratch. It assembles them from indexed conversation fragments. The conversations ARE the database. The documents are computed outputs.

---

## 3. Design Principles

### Conversations Are the Database

The primary source of truth is always the transcript. The index is a derived view. The compiled documents are derived from the index. Nothing replaces the transcript. Everything points back to it.

### Lightweight Index, Heavy Source

Index entries are small — metadata, topic tags, line ranges. They don't duplicate the conversation content. They just tell you *where to look*. When you need the full context, you read the transcript.

### Three Separate Concerns, Completely Decoupled

- The **watcher** produces the conversations (perception)
- The **index** stores structured metadata (memory)
- The **compiler** synthesizes on demand (cortex)

No component knows about the internals of the others. The watcher writes to the index. The compiler reads from the index. The index is the boundary.

### Silent Background Operation

The watcher never interrupts the working agent. It runs as a background daemon. The working agent produces conversations. The watcher indexes them. This happens without the working agent's awareness or participation.

---

## 4. Integration Points

### With Task Engine

The Task Engine (`task_ingest.py`, `task_query.py`, `task_update.py`, `tasks.db`) already manages tasks in SQLite. The Nervous System index should either:
- Share the same database (add a `chat_index` table alongside `tasks`)
- Use a separate database but with cross-references (task IDs as foreign keys)

### With task_context.py

`task_context.py` is a precursor — it searches transcripts for task IDs. The Nervous System subsumes this: instead of grep-searching raw files, `task_context.py` could query the structured index for instant results.

### With Python Bootloader (Task #160)

The bootloader computes system prompts from live workspace state. The Nervous System index is a source of live state — "what topics were discussed today," "what decisions were made," "what's unresolved." The bootloader could query the index to inject current conversational context into the system prompt.

### With publish_to_bridge.py

Context packs shipped to the Gemini bridge could be auto-assembled by the compiler: "Generate a context pack containing all conversations about X" → compiler queries index → pulls transcript sections → packages them.

---

## 5. Open Design Questions

1. **Delta detection:** How does the watcher detect that a transcript has been updated? File modification time? inotify? Polling?
2. **Extraction method:** LLM-based (more accurate, more expensive) vs. rule-based (faster, simpler, may miss nuance)?
3. **Extraction schema:** What fields exactly? The list above is a starting point — what's missing?
4. **Index storage:** SQLite (consistent with Task Engine) vs. something else?
5. **Compiler interface:** CLI tool? Cursor rule that triggers on command? MCP server?
6. **Watcher lifecycle:** Runs always? Starts with Cursor? Manual start/stop?
7. **Retroactive indexing:** Can the watcher process existing transcripts (backfill), or only new ones?
8. **Multi-session:** How does the index handle multiple simultaneous Cursor sessions?

---

## 6. Relationship to ML OS Port

The Nervous System is one component of the broader ML OS → Cursor port. It specifically enables:

- **Self-awareness:** ML OS agents can query what was discussed in previous sessions
- **Continuity:** New agents can be grounded not just in static files but in the indexed conversation history
- **Self-development:** The system can observe its own evolution over time through indexed metadata
- **Reduced context loss:** Decisions and rationale are preserved structurally, not just as raw text

Without the Nervous System, ML OS in Cursor is still a "brain in a jar" — it thinks, but it can't perceive what happened before it was instantiated. With it, ML OS gains temporal awareness.
