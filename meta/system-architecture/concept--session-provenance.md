# System Architecture: The Context Layer (Concept)
Date: 2026-01-21
Context: Created during the System Architecture Bootstrapping session.

## The Problem: Stateless Drift
AI coding sessions are traditionally ephemeral. They do work, but once the chat closes, the *intent* and *logic* behind the changes are lost. The repo becomes a pile of files without a history of *why*.

## The Solution: Session-Context Layer
We treat the **Chat Session** as a first-class citizen in the repository structure.

### 1. The Unit of Work
- Every session is a folder: `chats/YYYY-MM-DD--topic/`.
- Every session has a `README` (Intent) and an `actions_log` (Execution).
- This creates a **Provenance Graph**: We can trace any file back to the session that created it.

### 2. The Handoff Chain
- To solve memory loss between sessions, we use **Handoff Files**.
- `handoff_context.md` acts as a "Save Game" state.
- The next AI reads this file to "load" the user's mental context immediately.

### 3. The Rules Engine
- We enforce this via `.cursor/rules/chat-session-protocol.mdc`.
- This ensures that even "fresh" AI instances know to respect the architecture.
