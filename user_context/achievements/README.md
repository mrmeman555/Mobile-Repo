# Achievements Ledger (Append-Only Evidence)

This folder stores append-only, factual evidence of demonstrated capabilities, achievements, and proven behaviors of the user.

- No interpretation
- No summarization
- No retroactive editing
- This is evidence, not narrative

---

## Storage model (two-layer)

### 1) Long-form achievement artifacts (individual files)
- Each achievement you provide is stored as its **own Markdown file** in this folder.
- Content is stored **verbatim**, with **conversational wrapper removed** (keep only the achievement body).
- These files are **write-once** (no retroactive edits). If something must be corrected, create a new artifact that supersedes the old one.

**Filename format**
- `YYYYMMDD_HHMMSS__<short-slug>.md`
  - Example: `20260102_143012__netplus-lab-setup.md`

### 2) Append-only index (achievements_log.md)
`achievements_log.md` is the **append-only chronological index** of the individual achievement files.

Each index entry:
- is short (1–5 lines)
- is factual and concrete
- includes the **artifact filename** so the long-form evidence can be retrieved
- contains no motivational language and no abstraction

