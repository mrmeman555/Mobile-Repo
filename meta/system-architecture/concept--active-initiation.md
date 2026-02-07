# System Architecture: The Active Initiation Workflow
Date: 2026-01-21
Context: Upgraded during the System Architecture Bootstrapping session.

## The Shift: Inverted Control
Instead of the user managing the AI's context ("Read this, do that"), the AI manages the session's lifecycle ("What are we doing? Okay, I've set up the workspace").

## The "Initiate Meta System" Trigger
When invoked, the AI executes a **Setup Script** defined in `.cursor/rules/chat-session-protocol.mdc`.

### Session Types
We classify sessions to constrain the AI's behavior and focus its context retrieval.

1.  **Architect Mode**
    - **Goal:** System design, rule changes, meta-structure.
    - **Behavior:** High-level, abstract, cautious about breaking changes.
    - **Key Directories:** `meta/`, `.cursor/rules/`, `chats/`.

2.  **Builder Mode**
    - **Goal:** Execution, content creation, coding.
    - **Behavior:** High-speed, focused on specific output artifacts.
    - **Key Directories:** `daily/`, `inbox/`, specific project folders.

3.  **Gardener Mode**
    - **Goal:** Maintenance, indexing, link repair.
    - **Behavior:** Systematic, thorough, low-risk.
    - **Key Directories:** `*/**` (Global scan).

## The Workflow
1.  **Trigger:** User says "Initiate".
2.  **Negotiation:** AI asks Goal & Type.
3.  **Setup:** AI creates `chats/<session>/` and loads Type-specific context.
4.  **Work:** Standard execution with logging.
5.  **Handoff:** AI generates the bridge for the next session.
