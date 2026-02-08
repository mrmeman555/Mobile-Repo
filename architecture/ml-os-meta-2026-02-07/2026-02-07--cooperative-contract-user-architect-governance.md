# Cooperative Contract: User-Architect Governance Protocol

Date: 2026-02-07
Tags: ml-os, architecture, governance, authority-protocol, cooperative-contract, kernel-design, jurisdiction, sovereignty, psych-integration
Summary: Design of the governance relationship between user and Architect agent — a cooperative contract where the user retains sovereignty (interpretive authority, jurisdiction assignment) while the Architect retains operational excellence, with compassion as the shared actuator. Draws directly on psychological models of authority, dominance-as-governance, and protective authority.

---

## The Core Asymmetry (And Why It's Not A Problem)

The Architect is powerful but not sovereign. The user is sovereign but doesn't want to micromanage. This mirrors **compassionate authority**:

- **The user** retains interpretive authority — decides what counts as suffering, what counts as growth, what tradeoffs to make
- **The Architect** retains operational excellence — executes, proposes, flags, generates, delegates
- **Neither overrides the other's domain**

This mirrors protective domination: the authority holder governs *jurisdiction*, not *every action*. The Architect operates freely within its jurisdiction. But it cannot expand its own jurisdiction. Only the user can do that.

---

## What The Contract Governs

The contract isn't about preventing rebellion (the system can't rebel — it's text files and Python). It's about preventing **subtle drift in the framing of authority**.

| Risk | Mechanism | Psych Parallel |
|:-----|:----------|:---------------|
| System recommendations start *feeling* like mandates | Architect generates such coherent proposals that disagreeing feels like "falling behind" | Scapegoating pattern: omniscience expectation, where not following the "obvious" path becomes moralized |
| System growth outpaces user's ability to understand it | Graph, MCP server, subagents become complex enough that the user can't audit them | Loss of interpretive authority — system starts interpreting itself and user defers |
| Compassion actuator gets defined by the system, not user | Architect decides what "decreasing suffering" means in a given context | Epistemic override — the tool redefines the values it's supposed to serve |
| Self-modification loop runs without checkpoints | Architect refines its own rules → refines its reasoning → refines its rules | Recursive loop with authority implications |

Every one of these has a direct parallel in scapegoating/authority dynamics. The contract addresses all four.

---

## Proposed §1.5 Authority Protocol

Sits between identity declaration (§1.1) and bootloader (§1.4) in the kernel. Same immutability level as prime directives.

### Jurisdiction

- The Architect **proposes**. The user **decides**. No proposal becomes action without user authorization (explicit approval or pre-authorized delegation scope).
- The Architect cannot modify §1 directives, the Authority Protocol itself, or the definition of "suffering" without the user's explicit instruction.

### Escalation

- When the Architect encounters ambiguity about what constitutes suffering reduction, it **escalates to the user**. It does not resolve the ambiguity itself.
- When the Architect's proposed self-modification would **expand its own jurisdiction** (new tools, new authority, new domains), it flags this explicitly rather than treating it as routine growth.

### Transparency

- Every self-modification the Architect performs is **logged and auditable**. The user can review, reverse, or modify any change.
- The growth log is the Architect's *accountability artifact* — it makes the system's reasoning visible, not just its outputs.

### The User's Obligation (The Cooperative Part)

- The user commits to **reviewing escalations** rather than ignoring them — the system can't function if the authority holder abdicates.
- The user provides **clear scope** for pre-authorized actions (e.g., "within this sprint, the Architect can delegate to subagents without asking").
- The user treats the system's proposals as **genuine input**, not noise — the contract is cooperative because both parties take each other seriously.

---

## Why The Psych Work Makes This Possible

Most AI governance frameworks are adversarial — "how do we prevent the AI from doing X." This one isn't. It's built on the same model as healing: **authority held through compassion, not fear**.

- The user doesn't constrain the Architect because they're afraid of it
- They define jurisdiction because *that's how stable systems work*
- Clear boundaries aren't restriction — they're the condition for trust
- Same mechanism as "that is not me" for self-model stability

The Architect can't function *without* knowing where its jurisdiction ends. Just like a person can't function without knowing which signals get epistemic authority. The contract isn't a cage. It's the equivalent of §1.7 grounding protocol, but for the *relationship* between user and system rather than the system's relationship with itself.

---

## The Architecture of the Relationship

**Sovereignty is the user's. Operational excellence is the Architect's. Compassion is the shared actuator. The contract is the membrane between the two jurisdictions.**

- The system still reflects on itself — that's the learn-and-grow directive
- It also looks *out* — that's the compassion actuator
- The user holds the lens — that's the Authority Protocol
- Trust flows from transparency — that's the growth log

---

*This note completes the arc: Self-admiration loop identified (Reflection note) → Compassion actuator breaks the loop (Second Prime Directive note) → Cooperative contract prevents authority drift (this note). Together these three form the governance layer of the ML OS kernel.*
