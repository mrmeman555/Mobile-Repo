# Concept: Kernel-Module Agent Architecture
Date: 2026-01-21
Context: Developed during the "System Architecture Bootstrapping" session.

## The Problem: Rule Saturation
A single AI agent cannot reliably adhere to a massive, monolithic rule set ("The Soup"). As constraints increase, adherence degrades ("Instruction Dilution").

## The Solution: Kernel + Modules
We split the governance layer into two distinct tiers, mimicking an Operating System.

### 1. The Kernel (`00-kernel.mdc`)
- **Role:** The Dispatcher / Traffic Cop.
- **State:** Always active / High priority.
- **Responsibility:**
  - Does NOT do work.
  - Monitors User Intent.
  - Determines the active **Mode**.
  - Loads/Invokes the correct **Module**.
- **Logic:** "User wants to redesign folders? -> Load Architect Mode."

### 2. The Modules (`10-mode-architect.mdc`, `20-mode-builder.mdc`, etc.)
- **Role:** The Worker / Expert.
- **State:** Loaded only when invoked by Kernel.
- **Responsibility:**
  - executing specific tasks with deep, specific constraints.
  - Ignorant of other modes (Separation of Concerns).

## Implementation Strategy
We will refactor `.cursor/rules/chat-session-protocol.mdc` into:
1.  `.cursor/rules/00-kernel.mdc` (The Trigger & Router)
2.  `.cursor/rules/10-mode-architect.mdc` (System Design Rules)
3.  `.cursor/rules/20-mode-builder.mdc` (Content/Code Rules)

This enables "Dynamic Mode Switching" where the agent explicitly acknowledges: "Switching context to Architect Mode."
