# Tools index

This index tracks tool/methodology notes stored in `tools/`.

## How to use

- All tools use the canonical structure:
  - `tools/<tool-slug>/methodology/`
  - `tools/<tool-slug>/use-cases/<use-case>/`
- The tool root (`tools/<tool-slug>/`) must **not** directly contain notes.
- Any time a new note is added, **update this index** with:
  - Title (as a link)
  - Date (ISO `YYYY-MM-DD`)
  - Tool (which tool this note is related to)
  - Either:
    - Category: Methodology, or
    - Use case: <use-case-name>
  - 1–2 line summary
  - Optional tags

## Execution workflow (rule-first, note-driven)

When you ask me to do *anything*, I will:

1. **Check workspace rules first** in `.cursor/rules/` for any routing/storage/indexing or governance-output requirements that apply to your request.
2. **Check for relevant procedural notes** in the appropriate index (for tools work: this file, `tools/index.md`).
3. **Open the linked note(s)** that define the procedure (prompt templates, governance instructions, protocol steps, etc.).
4. **Follow the procedure from the note** rather than improvising.

This is specifically how “tools governance note” requests work: I consult `.cursor/rules/tools-governance-note-output.mdc` + `tools/index.md`, then generate the governance write-up from those sources.

## Entries (newest first)

- 2026-01-13 — [Stage 2 Response Example — Confirmation of Understanding (Bound Operation)](./epistemic-contract-engineering/use-cases/high-stakes-ai-collaboration/2026-01-13--stage-2-response-example-confirmation-of-understanding.md) — Tool: Epistemic Contract Engineering / Two-Stage Epistemic Binding Protocol — Use case: High-Stakes AI Collaboration — Example output to the Stage 2 binding prompt; explicitly binds behavior to the Stage 1 variables (MCR/FNR/OCM/DDR/AHA). (Tags: stage-2; response; example; confirmation)
- 2026-01-13 — [Stage 2 Binding Prompt — Context-Sensitive Operation Protocol](./epistemic-contract-engineering/use-cases/high-stakes-ai-collaboration/2026-01-13--stage-2-binding-prompt-context-sensitive-operation-protocol.md) — Tool: Epistemic Contract Engineering / Two-Stage Epistemic Binding Protocol — Use case: High-Stakes AI Collaboration — Copy/paste Stage 2 binding prompt that references the Stage 1 variables and prohibits hedging/flattening defaults unless net-harm reduction is shown. (Tags: stage-2; binding; prompt; protocol)
- 2026-01-13 — [Stage 1 Response Example — Output for “Shared Reality & Stakes Calibration”](./epistemic-contract-engineering/use-cases/high-stakes-ai-collaboration/2026-01-13--stage-1-response-example-for-shared-reality-and-stakes-calibration.md) — Tool: Epistemic Contract Engineering / Two-Stage Epistemic Binding Protocol — Use case: High-Stakes AI Collaboration — Example output to the paired Stage 1 prompt instance; defines explicit consequence variables for later Stage 2 binding. (Tags: stage-1; response; example; variables)
- 2026-01-13 — [Stage 1 Prompt Instance — Shared Reality & Stakes Calibration](./epistemic-contract-engineering/use-cases/high-stakes-ai-collaboration/2026-01-13--stage-1-prompt-instance-shared-reality-and-stakes-calibration.md) — Tool: Epistemic Contract Engineering / Two-Stage Epistemic Binding Protocol — Use case: High-Stakes AI Collaboration — Copy/paste Stage 1 prompt instance. Paired with the Stage 1 response example above. (Tags: prompting; stage-1; instance; stakes)
- 2026-01-13 — [Generalizing the Two-Stage Epistemic Binding Protocol Across Domains](./epistemic-contract-engineering/methodology/2026-01-13--generalizing-the-two-stage-epistemic-binding-protocol-across-domains.md) — Tool: Epistemic Contract Engineering / Two-Stage Epistemic Binding Protocol — Category: Methodology — Field-agnostic mapping of Stage 1 (constraints + causal chain + self-authored consequence variables) and Stage 2 (binding behavior to those variables) across mental health, AI research, startups, and creative work. (Tags: generalization; domain adaptation; leverage; drift control)
- 2026-01-13 — [Stage 1 Prompt Spec for Two-Stage Epistemic Binding Protocol](./epistemic-contract-engineering/methodology/2026-01-13--stage-1-prompt-spec-for-two-stage-epistemic-binding-protocol.md) — Tool: Epistemic Contract Engineering / Two-Stage Epistemic Binding Protocol — Category: Methodology — Checklist for the Stage 1 prompt: required context, causal chain, failure modes, and a strict output spec (shared understanding + named variables) to enable Stage 2 binding. (Tags: prompting; stage-1; variables; drift control)
- 2026-01-13 — [Two-Stage Epistemic Binding Protocol for High-Stakes AI Collaboration](./epistemic-contract-engineering/methodology/2026-01-13--two-stage-epistemic-binding-protocol-for-high-stakes-ai-collaboration.md) — Tool: Epistemic Contract Engineering / Two-Stage Epistemic Binding Protocol — Category: Methodology — Two-stage “epistemic contract” method: Stage 1 forces explicit stake variables; Stage 2 binds future behavior to those self-authored premises to reduce hedging/flattening drift. (Tags: methodology; AI collaboration; epistemics; drift control)

