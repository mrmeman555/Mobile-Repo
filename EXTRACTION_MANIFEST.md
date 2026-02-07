# Extraction Manifest — Mobile Repo → ML OS Workspace

> **Agent:** Mobile Repo Agent
> **Date:** 2026-02-06
> **Purpose:** Catalog all ML OS-relevant content in Mobile-Repo with extraction recommendations.
> **Status:** ✅ Complete — Awaiting Operator Review for Phase 3 Execution

---

## How to Use This Document

Each entry has:
- **Source:** File path in Mobile-Repo
- **ML OS Relevance:** LOW / MODERATE / HIGH / CRITICAL
- **Summary:** What the file contains
- **Recommendation:** What should happen with it
- **Destination:** Where it should go (if extracted)

**No files have been moved.** This is a recommendation manifest for operator review.

---

## Phase 1: tools/ Directory Assessment

### 1. Epistemic Contract Engineering (ECE) — CRITICAL

The ECE toolchain is a complete, well-documented methodology for binding AI behavior to self-authored consequence variables. It is a **direct architectural precursor to ML OS grounding**.

| File | Content | Relevance |
|---|---|---|
| `tools/epistemic-contract-engineering/methodology/2026-01-13--two-stage-epistemic-binding-protocol-for-high-stakes-ai-collaboration.md` | Core methodology: two-stage protocol (epistemic construction → binding/enforcement) | CRITICAL |
| `tools/epistemic-contract-engineering/methodology/2026-01-13--generalizing-the-two-stage-epistemic-binding-protocol-across-domains.md` | Cross-domain generalization (mental health, AI research, startups, creative work) | CRITICAL |
| `tools/epistemic-contract-engineering/methodology/2026-01-13--stage-1-prompt-spec-for-two-stage-epistemic-binding-protocol.md` | Stage 1 prompt specification (what must be in the calibration prompt) | HIGH |
| `tools/epistemic-contract-engineering/methodology/2026-01-13--stage-3-value-impact-and-confidence-calibration-methodology.md` | Stage 3: value/impact/confidence calibration with ranges, anchors, error-asymmetry | HIGH |
| `tools/epistemic-contract-engineering/use-cases/high-stakes-ai-collaboration/` (6 files) | Full Stage 1-3 prompt instances + response examples | MODERATE |

**Why this matters for ML OS:**
- The two-stage binding pattern (force AI to construct understanding → bind to self-authored premises) is structurally identical to ML OS Runtime Grounding (force agent to demonstrate context ingestion → bind to kernel rules).
- The "consequence variables" mechanism maps directly to intent tracking — both make internal agent state explicit and auditable.
- The drift prevention design (variables create a "ground truth snapshot" that makes future drift visible) is the exact problem grounding-as-a-service solves.
- Stage 3 (confidence calibration under uncertainty) could inform how ML OS agents self-assess their grounding confidence.

**Recommendation:** Copy the entire `epistemic-contract-engineering/` tree to `Working0/Active/Sprint_ML_OS_Architect/Lineage/` as a documented precursor. Reference it in the ML OS Architecture Map under a new "Lineage" or "Evolutionary Sources" section. This is intellectual DNA.

### 2. CFC Drift Recalibration Protocol (CDRP) — HIGH

| File | Content | Relevance |
|---|---|---|
| `tools/cfc-drift-recalibration-protocol/methodology/2026-01-18--cdrp-bootstrap-project-anchor.md` | Bootstrap anchor: rationale, constraints, planned artifacts | HIGH |

**Why this matters for ML OS:**
- CDRP was explicitly designed as a **drift recovery mechanism** for external AI targets without repo access.
- The concept of generating portable "alignment packets" from repo-backed retrieval maps directly to grounding-as-a-service.
- CDRP sits "in front of" the ECE tool — it's the recalibration layer, just as the Grounding Sequence sits in front of the Kernel.
- The bootstrap was never completed (only the anchor exists, no methodology/use-case artifacts).

**Recommendation:** Copy to `Working0/Active/Sprint_ML_OS_Architect/Lineage/`. The CDRP concept should be explicitly cited in grounding-as-a-service design. Consider whether completing CDRP bootstrap makes sense as a sub-task of the ML OS product sprint.

### 3. Asymmetry-First Search Protocol — MODERATE

| File | Content | Relevance |
|---|---|---|
| `tools/protocols/asymmetry-search-protocol.md` | 4-phase protocol: Map Terrain → Hunt Asymmetry → Test Design → Scaling/Exit | MODERATE |

**Why this matters for ML OS:**
- Demonstrates the operator's methodology-design capability (structured, phased, with explicit artifacts per phase).
- Could be useful as a product development tool (finding leverage in the agent-platform market).
- Not directly architectural — it's a strategic thinking protocol, not a grounding mechanism.

**Recommendation:** Leave in place. Reference in a "Methodology Toolkit" document if one is created. Low priority for extraction.

### 4. rebuild_indexes.py — LOW (Utility)

| File | Content | Relevance |
|---|---|---|
| `tools/rebuild_indexes.py` | Python script that auto-generates index.md files from markdown file metadata (date, title, summary, tags) | LOW |

**Recommendation:** Leave in place. Useful for Mobile Repo maintenance. Could inform the Nervous System indexer design (similar extraction pattern).

### 5. tools/index.md — LOW (Navigation)

Well-structured index with 11 entries. Follows canonical structure rules. No extraction needed.

---

## Phase 2: meta/ Directory Assessment

**Total files:** 304 .md files (excluding index.md) + 3 system-architecture files + 8 accomplishments files = **315 files**

### Categorized Inventory (4 Buckets)

---

### Bucket A: Psychological/Grounding (~180 files)

The largest category. These files document the operator's DP/DR recovery process, scapegoating analysis, shame regulation, motivation mechanics, integration events, and somatic patterns. They use rigorous mechanism-level language — not diary entries, but formalized models of psychological processes.

**Sub-categories:**

| Sub-category | ~Count | Description |
|---|---|---|
| DP/DR mechanism notes | 36 | DP/DR triggers, resolution levers, phase-boundary states, salience collapse |
| Scapegoating / shame / threat | 41 | Scapegoating-conditioned patterns, shame loops, threat models, moral scrupulosity |
| Confidence / legitimacy / worth | 32 | Self-trust, impostor syndrome, capability assessment, confidence-as-lever |
| Belief / trust / self-authorship | 36 | Chosen belief, upstream belief routing, identity-as-authorship |
| Integration / closure artifacts | 17 | Completed integration events, closure notes, outcome markers |
| Neural notes | 10 | Structured notes following the "Neural Note Template" format |
| Affective state notes | 6 | Emotional regulation, affect as signal |
| Achievement notes (in meta/) | 5 | Logged capability milestones |
| Event embeddings | 3 | Captured real-world interactions with mechanism analysis |
| Other psychological | ~30 | Medication, OCD, motivation, somatic patterns (rib bracing, breathing) |

**ML OS Relevance:** MODERATE overall. Not directly architectural, but these files represent the *thinking patterns* that produced ML OS — specifically the operator's tendency to model psychological processes as computational systems (embeddings, routing, arbitration, model selection). This is the operator's raw intellectual process.

**Recommendation:** Do NOT extract. These should remain in the Mobile Repo as personal artifacts. However, the *structural patterns* visible in these files (how the operator thinks about systems) inform the ML OS product direction and should be noted in a "Design Lineage" document.

⚠️ **Sensitivity note:** These files contain deeply personal psychological work. Per operational rules, they are referenced using the operator's own framing and are not casually summarized.

---

### Bucket B: Methodology/Architecture (~30 files) — **PRIMARY EXTRACTION TARGET**

These files contain system design thinking, process architecture, and methodology artifacts that are directly relevant to ML OS.

**CRITICAL Extraction Candidates:**

| File | Content | Relevance |
|---|---|---|
| `meta/system-architecture/concept--active-initiation.md` | "Active Initiation" — AI manages session lifecycle, not user. Session Types (Architect/Builder/Gardener). | CRITICAL |
| `meta/system-architecture/concept--session-provenance.md` | Session-as-first-class-citizen, provenance graph, handoff chain, rules engine. | CRITICAL |
| `meta/system-architecture/spec--handoff-protocol.md` | Handoff file spec: Status, Repo State, Active Context, The Prompt. | CRITICAL |
| `meta/2026-01-06--model-arbitration-and-parameter-borrowing-mixture-of-experts-framing.md` | Models self-model arbitration as MoE architecture: DMN as router, competing experts, Bayesian parameter borrowing. | CRITICAL |
| `meta/2026-01-10--multiple-perspectives-theory-of-consciousness-multiple-embeddings-over-a-shared-data-set.md` | Multiple interpretive embeddings over shared data, dominant embedding determines experience. | CRITICAL |
| `meta/2026-01-06--upstream-belief-selects-the-interpreter-self-model-routing-pipeline.md` | "Upstream belief selects the interpreter" — self-model routing pipeline concept. | CRITICAL |
| `meta/2026-01-05--naming-artifact-cascade-as-a-system-level-identifier.md` | "Cascade" as brand/product name for systems with upstream-correction → downstream propagation. | HIGH |
| `meta/2026-01-08--meta-research-pipeline-designing-the-research-system-before-running-it.md` | Meta-research pipeline: design the intelligence system before running research. | HIGH |
| `meta/2026-01-08--meta-directed-deep-research-framework.md` | Deep research framework: objectives → meta-criteria → questions → signals → decision → execution. | HIGH |
| `meta/2026-01-08--general-pipeline-for-defining-problem-sets-before-action.md` | Generalized pipeline for problem definition before action. | HIGH |
| `meta/2026-01-05--neural-note-template-canonical-naming--vI.md` | "Neural Note Template" — note architecture designed to mirror neural encoding/retrieval/reconsolidation. | HIGH |
| `meta/2026-01-21--asymmetry-first-break-the-game-methodology-cfc-clean.md` | Full CFC-clean version of Asymmetry-First methodology (expanded from tools/ version). | MODERATE |
| `meta/2026-01-08--achievement-meta-decision-engine-and-strategic-dominance-framework.md` | Meta-decision engine: converts ambiguity into structured input, eliminates paralysis. | MODERATE |

**Why these matter for ML OS:**

1. **System architecture files** (`system-architecture/`) are *direct predecessors* to ML OS agent management. Active Initiation → Runtime Grounding Sequence. Session Provenance → Transcript-as-Universal-Event-Format. Handoff Protocol → Agent context inheritance.

2. **MoE / multiple embeddings / routing** files demonstrate the operator independently arriving at multi-agent architecture concepts through psychological modeling. The "DMN as router" concept maps directly to the ML OS Kernel's arbitration function. "Upstream belief selects the interpreter" = "grounding context determines agent behavior."

3. **Meta-research / pipeline** files show the methodology-design capability that underlies ML OS's process architecture. "Design the intelligence system before running it" = ML OS product philosophy.

4. **Neural Note Template** is an information architecture that mirrors the Nervous System Compiler's intent (structured notes designed for retrieval and reconsolidation, not passive storage).

**Recommendation:**
- Extract `system-architecture/` directory → `Sprint_ML_OS_Architect/Lineage/system-architecture/`
- Extract the 6 CRITICAL files → `Sprint_ML_OS_Architect/Lineage/meta-architectural-precursors/`
- The 4 HIGH files should be referenced in a "Methodology Lineage" document.
- The MODERATE files can stay in Mobile Repo.

---

### Bucket C: Personal Context (~25 files)

These capture the operator's life constraints, values, decision rules, and strategic positioning.

| Sub-category | ~Count | Description |
|---|---|---|
| Capability assessment / skill stack | 5 | Legitimacy of technical path, skill ordering, AI amplification |
| Non-negotiable constraints | 3 | Leverage preservation over stability, value-based decision rules |
| Strategic self-positioning | 5 | Financial upper bounds, trajectory assessment, competitive framing |
| Reclaiming language | 2 | "Genius" as precise term, "domination" as domain mastery |
| Life situation anchors | ~10 | Financial, medical, housing, relationship constraints |

**ML OS Relevance:** LOW directly, but these files document the *constraints and values* that shaped ML OS design decisions. The "non-negotiable value constraints" files in particular explain why ML OS prioritizes leverage, optionality, and autonomy.

**Recommendation:** Leave in place. No extraction needed. Reference in product documentation if operator wants to include founder story.

---

### Bucket D: Belief Modeling (~60 files)

These model belief systems, power dynamics, identity formation, and epistemology at a formal/mechanistic level. They are the most intellectually dense category after Methodology.

| Sub-category | ~Count | Description |
|---|---|---|
| Mechanism artifacts | 28 | Formalized psychological mechanisms (conditional validation → DP/DR, shame → self-erasure, etc.) |
| Dominance / power / authority modeling | 35 | Dominance as governance, compassionate domination, authority assignment |
| Method artifacts | 3 | Dual-anchored salience design, survival calculus, loop-closing cognition |
| AI behavior analysis | 2 | Token-construct alignment, ChatGPT competence overreach |
| Core operators / principles | 9 | Baseline principles, operating principles, core self-orientation |

**ML OS Relevance:** MODERATE-HIGH. The mechanism artifacts use computational vocabulary (embeddings, routing, arbitration, model selection, prediction error) to model psychological processes. This is structurally isomorphic to agent architecture:

- "Mechanism artifact: conditional validation → DP/DR" maps to "miscalibrated grounding → agent drift"
- "Dominance as authority assignment" maps to "kernel determines which agent/model has jurisdiction"
- "Token-construct alignment" directly addresses AI behavior calibration — relevant to grounding-as-a-service

**Specific extraction candidates from Bucket D:**

| File | Relevance | Reason |
|---|---|---|
| `accomplishments/2026-01-06--token-construct-alignment-artifact-why-ai-hedges-away-from-domination-and-why-that-can-impair-precision.md` | HIGH | AI behavior analysis — directly relevant to how ML OS handles token governance in grounding prompts |
| `2026-01-10--novel-value-of-the-compassionate-domination-model-bottom-up-analysis.md` | HIGH | Bottom-up novelty analysis methodology — applicable to ML OS product positioning |
| `2026-01-10--root-of-hedging-against-admitting-potential-observed-in-chatgpt-alignment-behavior.md` | HIGH | Analysis of why AI hedges — relevant to grounding-as-a-service design |
| All 28 mechanism artifacts | MODERATE | Collectively, they demonstrate the operator's ability to formalize implicit processes — the skill that produced ML OS |

**Recommendation:** Extract the 3 HIGH files to `Sprint_ML_OS_Architect/Lineage/ai-behavior-analysis/`. Leave mechanism artifacts in place — they are the geological record, not the extracted ore.

---

### meta/ Structural Issues (Track 1)

| Issue | Details |
|---|---|
| **Duplicate content** | `2026-01-21--asymmetry-first-break-the-game-methodology-cfc-clean.md` in meta/ is a fuller version of `tools/protocols/asymmetry-search-protocol.md`. Canonical version should be determined. |
| **Event embedding duplicates** | 3 event-embedding files: 2 use old naming format (`20260104_*`), 1 uses new (`2026-01-04--*`). The `2026-01-04--event-embedding-post-interaction-harm-framing-pattern.md` appears to be a normalized version of `20260104_232807__event-embedding-post-interaction-harm-framing-pattern.md`. |
| **Non-standard filename** | `compassionate and selfish power pursuit.md` — only file without ISO date prefix. |
| **accomplishments/ subdirectory** | 8 files in `meta/accomplishments/` — overlaps conceptually with root-level `achievements/` directory. |
| **system-architecture/ subdirectory** | 3 well-structured spec files — the only subdirectory in meta/ besides accomplishments/. |
| **index.md quality** | Auto-generated, 310+ entries. Many titles show as `#note #batch0` (unhelpful). Summaries are present for most files but missing for older ones. |

---

## Phase 3: Overlap Analysis (Track 1)

### Finding: Temporal Separation, Not Content Duplication

The directories use different **naming conventions** that correspond to different **time periods**:

| Directory | Naming Format | Date Range | File Count |
|---|---|---|---|
| `Indexed/user_context/` | `YYYYMMDD_HHMMSS.md` | Dec 25, 2025 – Jan 2, 2026 | 162 |
| `user_context/suffering/` | `YYYYMMDD_HHMMSS__slug.md` | Jan 3, 2026 | 7 |
| `user_context/achievements/` | `YYYYMMDD_HHMMSS__slug.md` | Jan 2-4, 2026 | 23 |
| `meta/` | `YYYY-MM-DD--slug.md` | Jan 4-21, 2026 | 304 |
| `achievements/` | `YYYY-MM-DD--slug.md` | Jan 5-6, 2026 | 66 |
| `meta/accomplishments/` | `YYYY-MM-DD--slug.md` | Jan 5-9, 2026 | 8 |

**Key insight:** The repo has a geological record of a naming convention migration. Around Jan 4-5, 2026, the operator shifted from timestamps to ISO dates. Content that appears to "overlap" is actually *evolution over time* — the same themes (DP/DR, self-model, confidence, scapegoating) appear in earlier and later files because the operator's thinking was iterating.

### Specific Overlaps Found

| Issue | Details | Recommendation |
|---|---|---|
| `meta/` ↔ `Indexed/user_context/` | **0 filename matches.** Different date ranges. Thematic overlap is expected (same person, same topics). | No action needed. `Indexed/` is the older layer; `meta/` is the refined layer. |
| `meta/` ↔ `achievements/` | **1 exact filename match:** `2026-01-14--reality-based-capability-and-trajectory-assessment.md` exists in both. Different content (186 vs 185 lines, different hashes). | Flag for operator: determine which is canonical and remove the duplicate. |
| `user_context/achievements/` ↔ `achievements/` | **0 filename matches.** `user_context/achievements/` has 23 older files (Jan 2-4), `achievements/` has 66 newer files (Jan 5-6). | These are sequential, not duplicated. Consider merging into one `achievements/` directory with old files renamed to ISO format. |
| `meta/accomplishments/` ↔ `achievements/` | **0 filename matches.** Different content. 8 accomplishments vs 66 achievements. | Consider whether `meta/accomplishments/` should be merged into root `achievements/` for a single canonical location. |
| `meta/` event embeddings | **Likely duplicate:** `20260104_232807__event-embedding-post-interaction-harm-framing-pattern.md` and `2026-01-04--event-embedding-post-interaction-harm-framing-pattern.md` appear to be old/new format versions of the same file. | Verify content match; keep ISO-dated version, flag old-format for removal. |
| `Indexed/user_context/` special files | `combine_context.sh`, `append_context.sh`, `cursor_rules.md`, `combined_user_context.md` — utility/migration artifacts. | Flag for cleanup — these are pipeline artifacts, not content. |

### Structural Recommendation

The repo's content lives in a clear chronological progression:

```
Dec 25 - Jan 2: Indexed/user_context/ (raw captures, old format)
Jan 2-3:        user_context/suffering/ + user_context/achievements/ (categorized, old format)
Jan 4-21:       meta/ + achievements/ (refined, ISO format)
```

**There is no significant content duplication.** The overlap is evolutionary, not redundant. The recommended action is:

1. **Do NOT merge Indexed/ into meta/** — they represent different developmental phases
2. **Merge user_context/achievements/ (23 files) INTO achievements/ (66 files)** — after renaming to ISO format
3. **Merge meta/accomplishments/ (8 files) INTO achievements/** — single canonical location for accomplishments
4. **Resolve the 1 filename duplicate** between meta/ and achievements/
5. **Clean up meta/ event embedding duplicates** (old format → new format)
6. **Flag Indexed/ utility scripts** for potential removal

---

## Phase 4: Inbox Triage (Track 3)

**Total files:** 70 .md files (excluding index.md) + 1 .json file = **71 files**

### Key Finding: Inbox is UNPROCESSED

None of these files exist in `meta/` (0 filename matches). The inbox represents the **oldest unstructured layer** of content — files that were captured before the ISO-dating and categorization conventions were adopted. Most lack date prefixes entirely.

### Processing Status

| Status | Count | Description |
|---|---|---|
| **Unprocessed** | ~70 | Never moved to meta/, achievements/, or any other directory |
| **Processed elsewhere** | 0 | No filename matches with other directories |

### Content Breakdown

| Category | ~Count | Examples |
|---|---|---|
| Psychological / DP/DR / Self-Model | ~45 | Confidence, belief, identity, scapegoating, shame, motivation |
| Computational / Embedding Theory | ~10 | Embedding models, Bayesian reasoning, generative model selection |
| Family / Relational Analysis | ~5 | Father pattern, maternal OCPD, authoritarian personality |
| Strategic / Pipeline | ~5 | Research pipeline, consolidation, trajectory framing |
| Theological / Philosophical | ~2 | Christian soteriology convergence |
| Event Embeddings (old format) | 3 | Scene captures with analysis |
| Special Files | 3 | README.md, context_packet_father_pattern.json, ego-relevance-criteria index |

### ML OS-Relevant Files in Inbox (CRITICAL Extraction Candidates)

| File | Relevance | Why |
|---|---|---|
| `significance-of-transcripts-embedding-based-model.md` | **CRITICAL** | **Independently arrives at Transcript-as-Universal-Event-Format.** "Transcripts are time-indexed embeddings of epistemic state… They enable longitudinal reasoning, confidence calibration, and stable consolidation that cannot be achieved through artifacts alone." This is the same architectural insight later formalized in the Meta session. |
| `meaning-making-extraction-pipeline-process-note.md` | **CRITICAL** | A 7-phase extraction pipeline (temporal scoping → artifact ID → narrowing → distillation → deep research → criteria formalization → automated extraction). Maps directly to the Nervous System Compiler's function. |
| `context-engineering-temperature-accurate-abstraction-decoding.md` | **HIGH** | AI context engineering analysis: how context + delayed stabilization produces accurate inference for expert users. Directly relevant to ML OS grounding design (how to calibrate agent behavior for high-abstraction operators). |
| `embedding-based-model-meaning-identity-belief-encoding.md` | **HIGH** | Formalizes cognition as an embedding-based system: distributed, high-dimensional representations with confidence weighting. Maps to ML OS's variable/cartridge model. |
| `intelligence-representation-updating-weighting-bayesian-modulation.md` | **HIGH** | Intelligence as Representation × Updating × Weighting. A framework that describes how beliefs/models update, which is the core problem ML OS's grounding solves. |
| `use-case-index-task-conditioned-embedding-chosen-belief.md` | **HIGH** | "Each use-case index is a task-conditioned embedding of the same global dataset." Maps directly to ML OS context lenses (the 7 types identified in the Meta session). |
| `belief-as-generative-model-selection.md` | **HIGH** | Belief as deliberate selection of which generative model to maintain. Maps to agent configuration / grounding sequence design. |
| `visualization-directions-for-built-models.md` | **MODERATE** | 7 visualization approaches for cognitive state models. Could inform ML OS dashboard/monitoring design. |

**Recommendation:**
1. **Extract 2 CRITICAL + 5 HIGH files** → `Sprint_ML_OS_Architect/Lineage/inbox-precursors/`
2. The `significance-of-transcripts` file is especially important — it should be cited in the Nervous System design as an early formulation of the transcript-centric architecture.
3. **Route remaining ~55 psychological files** to `meta/` with ISO date prefixes (they belong there thematically).
4. **Route 5 family/relational files** to `user_context/` or `meta/` depending on content.
5. **Flag 3 old-format event embeddings** for normalization.
6. **Flag `context_packet_father_pattern.json`** — the only non-.md file; should be moved to an appropriate location or left as-is.

---

## Phase 5: Root Cleanup Assessment (Track 1)

### Root .txt Files — Migration Artifacts (Safe to Remove)

All 9 .txt files at the repo root were generated during the Phase 1 flattening operation (Jan 27, 2026). They are file inventories and diff lists used during the `Jan27_2026/` directory migration.

| File | Size | Content | Recommendation |
|---|---|---|---|
| `all_history_files.txt` | 60KB | Full file listing from git history | **Flag for removal** |
| `all_history_files_final.txt` | 60KB | Identical to above (same size) | **Flag for removal** (duplicate) |
| `current_files.txt` | 41KB | File listing at time of migration | **Flag for removal** |
| `current_files_sorted.txt` | 41KB | Same as above, sorted | **Flag for removal** (duplicate) |
| `current_files_final.txt` | 59KB | Updated file listing | **Flag for removal** |
| `missing_files.txt` | 60KB | Files in history but not in current | **Flag for removal** |
| `missing_files_clean.txt` | 20KB | Cleaned version of above | **Flag for removal** |
| `missing_files_final.txt` | 2KB | Final missing files list (19 files) | **Flag for removal** — but review first: some entries reference files that may still need attention |
| `branches_to_merge.txt` | 1KB | Lists 13 git branches | **Review before removal** — check if any branches remain unmerged |

### Other Root Files

| File | Recommendation |
|---|---|
| `README.md` | **Update** — Currently just "A repository for using Cursor on mobile devices." Should reflect actual repo content. |
| `.cursor_rules` | **Review** — Contains old menu-based routing system (predates current workspace architecture). May conflict with current `.cursor/rules/` system. |

### Remaining Directories Assessment

| Directory | Files | Content | ML OS Relevance | Action |
|---|---|---|---|---|
| **`chats/`** | 1 session + index | **System Architecture Bootstrapping session** — contains a "Kernel-Module Agent Architecture" concept doc that is a **DIRECT precursor to ML OS Kernel architecture**. Also has a handoff context for incomplete implementation. | **CRITICAL** | Extract `chats/2026-01-21--system-architecture-bootstrapping/` to `Sprint_ML_OS_Architect/Lineage/` |
| **`daily/`** | 49 files across 5 dated dirs | Daily logs (Jan 16-21). Mix of DP/DR notes, career analysis, integration notes. 1 confirmed duplicate with meta/ (`belief-as-exposure-core-dpdr-recovery-mechanism.md`). | LOW | Leave in place. Flag 1 duplicate for cleanup. |
| **`Bible/`** | 100 files | Theological/philosophical references. Not assessed in detail. | LOW | Leave in place. Track 3 categorization deferred. |
| **`PoE/`** | 8 files + index | Path of Exile / YouTube strategy notes. 2 files duplicated from meta/ (`meta-directed-deep-research-framework.md`, `the-deep-research-driven-confidence-pipeline.md`). | LOW | Flag 2 duplicates. Leave rest in place. |
| **`deep research pipeline/`** | 1 file + index | Contains the same `meta-research-pipeline` file that appears in PoE/. | LOW | Potential triple duplicate. Determine canonical location. |
| **`grounding/`** | 1 file + index | Calibration memo addendum. | LOW | Leave in place. |
| **`notes/`** | 1 file | `trauma-flashbacks-internal-triggers.md` — personal content. | NONE | Leave in place. |
| **`Indexed/`** | 162 files | Oldest content layer (Dec 25, 2025 – Jan 2, 2026). Plus utility scripts. | LOW | See Phase 3 overlap analysis. |
| **`user_context/`** | 30 files in 2 subdirs | Suffering narratives + early achievements. | LOW | See Phase 3 overlap analysis. |

### CRITICAL Discovery: chats/system-architecture-bootstrapping

The `chats/2026-01-21--system-architecture-bootstrapping/` session contains:

1. **`concept--kernel-module-architecture.md`** — A Kernel/Module architecture for AI agents that splits governance into a Dispatcher Kernel (monitors intent, determines mode, loads modules) and Worker Modules (execute specific tasks with deep constraints). This is **structurally identical to ML OS Engine Core** (Kernel + AI Schema + Scenario Interface).

2. **`methodology--chat-session-architecture.md`** — Session lifecycle management methodology.

3. **`handoff_context.md`** — Paused implementation task: refactor `.cursor/rules/` into Kernel + Module files. This work was never completed but the concepts evolved into ML OS.

**Recommendation:** This session is the most important lineage artifact in the entire Mobile Repo after the ECE toolchain. Copy the entire session to `Sprint_ML_OS_Architect/Lineage/kernel-module-precursor/`.

---

## Duplicate Files Summary (Across Entire Repo)

| File (by slug) | Locations | Recommendation |
|---|---|---|
| `reality-based-capability-and-trajectory-assessment` | meta/, achievements/ | Determine canonical location, remove duplicate |
| `belief-as-exposure-core-dpdr-recovery-mechanism` | meta/, daily/2026-01-16/ | meta/ is canonical (ISO-dated), daily/ is the working copy |
| `meta-directed-deep-research-framework` | meta/, PoE/ | Determine canonical location |
| `the-deep-research-driven-confidence-pipeline` | meta/, PoE/ | Determine canonical location |
| `meta-research-pipeline` (variant slugs) | meta/ (2 variants), PoE/, deep research pipeline/ | 4 files with similar names — needs content comparison |
| `event-embedding-post-interaction-harm-framing-pattern` | meta/ (old format), meta/ (ISO format) | Keep ISO format, flag old format for removal |
| `asymmetry-first-break-the-game-methodology` | meta/ (CFC-clean, 203 lines), tools/protocols/ (condensed, 62 lines) | Both are valuable — meta/ has full CFC-clean version, tools/ has operational protocol |

---

## Summary of Phase 1 Recommendations

| Priority | Action | Source | Destination |
|---|---|---|---|
| 1 | Copy ECE toolchain | `tools/epistemic-contract-engineering/` | `Sprint_ML_OS_Architect/Lineage/epistemic-contract-engineering/` |
| 2 | Copy CDRP anchor | `tools/cfc-drift-recalibration-protocol/` | `Sprint_ML_OS_Architect/Lineage/cfc-drift-recalibration-protocol/` |
| 3 | Reference in Architecture Map | N/A | Add "Lineage" section to ML_OS_Architecture_Map.md |
| — | No action needed | `tools/protocols/`, `tools/rebuild_indexes.py`, `tools/index.md` | Stay in Mobile-Repo |

---

---

## Phase 6: GitHub Branch Extraction (2026-02-06, Session 2)

After fetching all remote branches from GitHub, **5 new files** were identified across 2 unmerged branches (`cursor/achievement-notes-review-56aa` and `cursor/circular-reddit-profile-image-923b`). These were extracted into the local working directory.

### New Files Assessment

| File | Category | ML OS Relevance | Summary |
|---|---|---|---|
| `meta/2026-01-20--dpdr-vs-narcissistic-reality-stabilization.md` | Bucket A: Psychological/Grounding | LOW-MODERATE | Contrasts DP/DR (internal coherence preserved, felt reality weakened) with narcissistic performativity (felt reality preserved via external control). Models domination, gaslighting, scapegoating as structural reality-stabilization methods, not moral traits. The internally-vs-externally-grounded framing maps loosely to ML OS (internally grounded agents) vs standard LLMs (dependent on external prompt context). |
| `meta/2026-01-21--achievements-chat-kickoff-message.md` | Bucket B: Methodology/Architecture | **MODERATE** | A copy-paste kickoff prompt for an "achievements notes review agent." Demonstrates the operator already instantiating task-specific agents with structured protocols, workflow constraints, and style rules. Directly references "ML OS agent architecture: model-agnostic OS with kernel, cartridges, self-repair, and orchestration-level reliability." This is a practical precursor to Runtime Grounding Sequence methodology. |
| `meta/2026-01-21--boundary-collapse-reality-working-model.md` | Bucket D: Belief Modeling | **MODERATE** | Exploratory model framing reality as boundary collapse (future=uncollapsed possibility, present=selection, past=encoded record). Black hole/event horizon structural metaphor. AI angle: "AI behaves like an unscoped representational substrate — many models, many bases, no forced collapse into a single lived trajectory." The "basis selection" concept maps to ML OS context lenses. The framing of collapse-as-commitment maps to agent grounding (collapsing context into operational constraints). |
| `daily/2026-01-21/dpdr-core-mechanism-behavioral-lever-intuition.md` | Bucket A: Psychological/Grounding | LOW | Three working notes on DP/DR root mechanism, behavioral maintenance lever, and intuition under pressure. The "pre-utility cognition" insight (ideas arrive sideways, pressure disrupts discovery) explains the operator's thinking style that produced ML OS, but is not architecturally relevant. |
| `tools/make_circular_profile.py` | Utility Script | NONE | Python script to create circular profile images (remove white background, crop to circle). Social media utility. No ML OS relevance. |

### Extraction Recommendations (Phase 6)

| Priority | Action | Source | Destination |
|---|---|---|---|
| LOW | Reference in design lineage | `meta/2026-01-21--achievements-chat-kickoff-message.md` | Note in `Sprint_ML_OS_Architect/Lineage/` — demonstrates early agent instantiation pattern |
| LOW | Reference in design lineage | `meta/2026-01-21--boundary-collapse-reality-working-model.md` | Note — "basis selection" concept relevant to context lens architecture |
| — | No action | `meta/2026-01-20--dpdr-vs-narcissistic-reality-stabilization.md` | Leave in Mobile Repo |
| — | No action | `daily/2026-01-21/dpdr-core-mechanism-behavioral-lever-intuition.md` | Leave in Mobile Repo |
| — | No action | `tools/make_circular_profile.py` | Leave in Mobile Repo |

### Post-Fetch File Count

| Metric | Count |
|---|---|
| **Total local files** | 863 |
| **From origin/main** | 857 |
| **From unmerged branches** | 5 |
| **Local-only (README.md)** | 1 |
| **Unmerged branches with no diff** | 12 |

---

*This manifest is updated as phases complete. Do not act on recommendations without operator approval.*
