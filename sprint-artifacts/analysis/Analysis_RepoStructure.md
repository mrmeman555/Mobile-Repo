# Mobile Repo Analysis

> **Date:** Feb 4, 2026
> **Scope:** `/home/aaron/Projects/Mobile-Repo/`

## 📊 High-Level Metrics
- **Total Files:** 914
- **Root Directory:** `/home/aaron/Projects/Mobile-Repo/`
- **Primary Content Node:** `Jan27_2026/` (Appears to be a major snapshot or migration point).

## 📂 Directory Structure & File Counts

The repository is organized into distinct domains under the `Jan27_2026` root.

| Directory | File Count | Purpose | Index Present? |
|---|---|---|---|
| `Jan27_2026/meta` | **305** | System prompts, architecture, core context | ✅ `index.md` |
| `Jan27_2026/Indexed` | **164** | (Sub: `user_context`) Processed context | ✅ `INDEX.md` |
| `Jan27_2026/Bible` | **100** | Theological/Philosophical references | ✅ `index.md` |
| `Jan27_2026/inbox` | **71** | Unprocessed notes and captures | ✅ `index.md` |
| `Jan27_2026/achievements`| **66** | Logged wins/milestones | ✅ `index.md` |
| `Jan27_2026/daily` | **~49** | Daily logs (Dated folders) | ✅ `index.md` |
| `Jan27_2026/user_context` | **32** | (Sub: `suffering`, `achievements`) User state | ✅ `INDEX.md` |
| `Jan27_2026/PoE` | **9** | Path of Exile related | ✅ `index.md` |
| `Jan27_2026/chats` | **6** | Transcripts | ✅ `index.md` |
| `Jan27_2026/tools` | **~15** | Methodologies & Protocols | ✅ `index.md` |

## 🧭 Navigation System (Indexes)

The repository uses a pervasive `index.md` pattern.

**Key Indexes:**
-   `Jan27_2026/meta/index.md`
-   `Jan27_2026/inbox/index.md`
-   `Jan27_2026/daily/index.md`
-   `Jan27_2026/tools/index.md`

**Inconsistencies:**
-   `user_context` uses `INDEX.md` (Uppercase) while most others use `index.md` (lowercase).
-   `Indexed/user_context` also uses `INDEX.md`.

**Automation:**
-   Found `Jan27_2026/daily/update_index.py`
-   Found `Jan27_2026/tools/rebuild_indexes.py`
-   *Observation:* These scripts suggest an attempt to automate the maintenance of these index files.

## ⚠️ Observations
1.  **Nesting:** The entire repo seems to live inside `Jan27_2026`. This might be a migration artifact.
2.  **Duplication?** There is a `user_context` (32 files) and an `Indexed/user_context` (164 files). This suggests a processing pipeline where raw context is refined or indexed.
3.  **Meta Dominance:** The `meta` folder is the largest (300+ files), indicating this repo is heavily used for system prompting and architecture definition.

## 📝 Recommendations
1.  **Flattening (Optional):** Consider if `Jan27_2026` should be the root, or if this date is significant enough to keep.
2.  **Index Standardization:** Decide on `index.md` vs `INDEX.md`.
3.  **Pipeline Verification:** Check if `update_index.py` is still functional or if `Sprint_Librarian` should take over indexing duties.
