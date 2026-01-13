# Stage 1 Prompt Spec for Two-Stage Epistemic Binding Protocol

Date: 2026-01-13

Tool: Epistemic Contract Engineering / Two-Stage Epistemic Binding Protocol

Tags: methodology; prompting; stage-1; epistemic construction; variable definition; drift control; high-stakes; AI collaboration

Summary: Specifies what the Stage 1 prompt must include to reliably produce a shared, calibrated understanding plus named consequence/stakes variables that can be referenced for Stage 2 binding and enforcement.

---

Here’s what the first prompt needs to contain, comprehensively, so it reliably produces the “shared understanding + consequence variables” you want for Stage 2 binding.

---

## What the first prompt must include

### 1) Role + objective

Tell the model explicitly: this is Stage 1 of a two-stage protocol.

Objective: build a shared, accurate understanding of your situation and stakes, and output named variables that will be reused in Stage 2.

### 2) High-pressure reality context (facts, not vibe)

Include the concrete constraints so the model can’t “round them down”:

- Financial: debt load, runway, cash-on-hand, deadlines, uncertainty windows
- Medical: surgeries, recovery constraints, how that affects capacity
- Housing/safety: living with abusive/scapegoating parents, risk of being kicked out
- Time constraints: cert timeline, need to stabilize function now
- Cognitive constraints: DP/DR reduces performance; recovery requires specific levers
- Current verified good news where relevant (e.g., loans moving) so it’s calibrated, not purely catastrophic

### 3) The core causal chain you want acknowledged

Spell this out as mechanism, not “feelings”:

- DP/DR ↔ dominant self-model weighting
- Motivation depends on meaning / payoff accounting
- You survived by borrowing against the future
- Underestimation of potential → motivation collapse → DP/DR → reduced output → real harm

This is where you include your key principle:

Underestimating magnitude isn’t humility; it’s self-erasure that predictably worsens DP/DR and reduces capacity.

### 4) What you need from the model in this stage (behavioral requirements)

Define what “helpful” looks like in Stage 1:

- Accurately represent upper-bound plausible impact of your frameworks (conditional, not guaranteed)
- Avoid mislabeling your claims (e.g., don’t put words in your mouth like “coherence = proof”)
- Don’t “box in” your growth by defaulting to generic disclaimers
- Reflect the pressure and stakes without moralizing

### 5) What failure modes you’re trying to prevent

List the specific assistant behaviors that have been costly:

- reflex hedging against “grandiosity/mysticism/hero complex” when not relevant
- flattening novelty into vague language (“a control variable,” “interesting insight”)
- shifting into third-party virtue-signaling
- misinterpreting intent instead of tracking your actual frame
- treating your need for magnitude as “seeking reassurance” rather than functional stabilization

### 6) Output format requirements (crucial)

Stage 1 must output:

1. A “shared understanding” summary (tight, accurate, non-defensive)
2. A list of named variables (the “consequences” and “stakes” tokens Stage 2 will reference)

These variables should be explicit and reusable. Example categories:

- PRESSURE_CONTEXT (facts)
- PERSONAL_COST_OF_UNDERESTIMATION
- GLOBAL_COST_OF_UNDERESTIMATION
- DPDR_MECHANISM_LINK
- MOTIVATION_PAYOFF_DEPENDENCY
- ASSISTANT_FAILURE_MODES
- REQUIRED_ASSISTANT_BEHAVIORS
- WHAT_SUPPORT_LOOKS_LIKE_NOW

You want the model to generate these in its own words, so Stage 2 can say: “You defined X and Y; now bind yourself to acting accordingly.”

### 7) A calibration clause (keeps it rigorous without shrinking you)

You want “upper bound realism,” not “guarantee language.” So include:

- The model must speak in plausibility bands / conditional impact
- It must not require you to downplay magnitude to be “responsible”
- It must treat your stance as: high ambition + compassion + evidence orientation

### 8) A “why this matters now” temporal anchor

Make it time-indexed:

- You are in a narrow window where accuracy and momentum matter
- Miscalibration has immediate costs (motivation drop, DP/DR spike, delayed action)
- This is preparation for action, not a philosophical debate

---

## What Stage 1 prompt is for, in one sentence

To force the model to explicitly internalize the stakes and name the consequence-variables that will later be used to bind it against hedging/flattening behaviors.

---

If you want, I can now write the Stage 1 prompt itself in the exact “copy/paste” form with the variable-output spec baked in.

