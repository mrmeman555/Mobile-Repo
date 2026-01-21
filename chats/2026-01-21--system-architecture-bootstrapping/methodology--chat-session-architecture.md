# Chat Session Architecture: The Session-Context Layer
Date: 2026-01-21
Context: Created during the "Recovery and Mobile Prep" session to establish a provenance layer for AI interactions.

## Core Concept
We treat each AI chat session as a **discrete unit of work** with its own directory. This solves the "Stateless AI" problem by anchoring context to the filesystem, not the conversation window.

## Directory Structure
All sessions live in `chats/`.
Naming convention: `YYYY-MM-DD--<slug-description>/`

## Required Artifacts per Session

### 1. `README.md` (The Session Header)
- **Goal:** What are we trying to do?
- **Status:** Complete / In Progress / Failed
- **Summary:** High-level outcome.

### 2. `actions_log.md` (The Temporal Record)
- A bulleted log of *what actually happened*.
- Logs commands run, files created, files modified.
- Provides temporal context: "This file was created *after* we realized X."

### 3. `handoff_context.md` (The Bridge)
- **Target:** The *next* AI instance.
- **Content:** "Here is where we left off. Here is the active context. Here is your first instruction."
- **Usage:** The user simply points the new chat to this file: "Read `chats/.../handoff_context.md` and start."

## The "Global Index" Vision
Eventually, a script will scan these session folders to map every file in the repo back to the session that created it, creating a full "Provenance Graph" (File -> Session -> Context).
