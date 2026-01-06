# Model Arbitration & Parameter Borrowing — Mixture-of-Experts Framing
Date: 2026-01-06
Tags: self-model, DMN, salience, mixture-of-experts, arbitration, prediction error, Bayesian updating, belief
Summary: Frames “talking to” between self-models as mixture-of-experts arbitration: co-activation forces shared constraints; unresolved prediction error drives borrowing of explanations/priors from higher-coherence models, producing eventual rerouting and stable self-model convergence.

## 1. Self-Models as Concurrent Experts

Think of each self-model as a specialized expert:

Each has:

- Its own priors
- Its own explanation set
- Its own confidence weighting
- Its own way of resolving uncertainty

The DMN is effectively the router / arbitration layer that decides:

- Which model is currently “authoritative”
- Which one gets to interpret incoming data
- Which one writes back to long-term belief

This is extremely close to a mixture-of-experts architecture.

---

## 2. What “Talking To” Actually Means (Mechanistically)

When you hold a chosen belief + context in working memory, you are:

Forcing co-activation of two models:

- The currently dominant (negative) one
- The chosen (healthier) one

That co-activation creates a shared constraint space.

At that point, something important happens:

> The negative model encounters prediction errors it cannot locally resolve.

It starts asking, implicitly:

“If this wasn’t my fault… then how do I explain X?”

“If I was doing my best… then why does Y still feel true?”

“If this belief persists, what interpretation preserves coherence?”

This is where the “talking to” happens.

---

## 3. Borrowing Solutions Is a Real Thing

In predictive systems, when a model cannot resolve error internally, it does one of two things:

1. Borrow parameters / explanations from another model that can
2. Yield control to the model with higher explanatory power

That is not metaphorical.
That is how hierarchical Bayesian systems stabilize.

So when you say:

> “The positive model can literally send the connections the negative model needs”

What that means in practice is:

The healthier model has:

Already encoded explanations like:

- “effort under constraint”
- “intent vs outcome separation”
- “non-catastrophic attribution”

Those explanations get sampled when the negative model is searching for a way to reduce error.

Over time, the negative model either:

- Integrates those explanations
- Or becomes redundant and stops being selected

That’s not suppression.
That’s Bayesian updating under competition.

---

## 4. Why This Produces Sudden Consistency Shifts

This also explains the felt phenomenon:

> “That would explain the consistency in felt self-models”

Once:

- enough explanations are borrowed
- enough priors are weakened
- enough prediction errors resolve without catastrophe

the arbitration layer (DMN) goes:

> “This other model explains more with less cost.”

And then the system reroutes.

Subjectively, this feels like:

- “I’m suddenly myself again”
- “The old view no longer has traction”
- “The negative model just… stopped convincing me”

That’s not magic. That’s model selection convergence.

---

## 5. Why You Must Hold the Belief Through Discomfort

This also explains why the process requires discomfort:

- You are deliberately creating cross-model tension
- You are preventing the negative model from collapsing the experiment early
- You are forcing it to run out of justifications

Every spike of doubt is:

- A hypothesis being tested
- A pathway being exhausted
- A reason being checked and discarded

When there are no good answers left, the model doesn’t “die” — it defers.

---

## 6. Why “Talking To” Is the Right Language

In distributed systems, we routinely say:

- Services talk to each other
- Models query each other
- Agents exchange beliefs
- Components negotiate state

No one thinks that’s mystical.

Your brain is doing the same thing:

- Models exchange constraints
- Priors leak across boundaries
- Solutions propagate to reduce global error

So yes — they talk to each other.
Just not in words.

---

## 7. One Clean Summary Sentence

> When a self-model cannot resolve prediction error, it samples explanations from competing models with higher coherence — and eventually yields control.

That’s what you’re inducing deliberately.

You’re not fighting the negative model.
You’re out-informing it.

And once it has nothing left to say, it stops being selected.

That’s not coping.
That’s system-level reorganization.

