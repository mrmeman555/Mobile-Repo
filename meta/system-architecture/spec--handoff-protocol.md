# System Spec: Handoff Protocol
Date: 2026-01-21

## The Handoff File (`handoff_context.md`)

This file is the **Bridge** between AI sessions. It must contain everything a fresh model needs to be useful *immediately*.

### Required Fields

1.  **Status:** (e.g., In Progress, Blocked, Complete)
2.  **Repo State:** (e.g., "Branch X merged", "Tests failing")
3.  **Active Context:** (What were we just talking about? What is the user's mood/intent?)
4.  **The Prompt:** A direct instruction for the next AI.

### Usage Pattern

**User:** "Read `chats/latest/handoff_context.md` and continue."

**Next AI:**
1.  Reads the file.
2.  Adopts the persona/goal defined in "The Prompt".
3.  Executes the "Next Steps".
