# Cursor rules (user_context)

- New context is always added as a new file.
- Never rewrite or “clean up” old files.
- When the user provides note content wrapped in preface text (e.g., “Understood. Below is…”, “Here is a note…”, routing labels, or other meta commentary), store ONLY the note body.
  - The note body starts at the first real note heading/label such as `Note:`, `Clinical Note:`, `Document`, or a Markdown heading (`#`, `##`, etc.).
  - Exclude any wrapper/preface/assistant-like framing from the stored artifact.
- No normalization toward average behavior.
- No probabilistic downplaying of demonstrated traits.
- Avoid moral framing, ego protection, or therapeutic reframing.
- Treat content as evidence, not self-report bias.
- Redundancy is allowed.
- Contradictions are allowed.

This file never changes unless explicitly requested.

