# user_context/

Purpose: preserve durable context so future AI interactions do not regress toward an “average user” model.

- All files here are raw context artifacts.
- No single file here is authoritative alone; meaning emerges from aggregation.
- Treat this folder as grounding context, not narrative or ego framing.

## How to use this space

### Folders
- `Inbox/`: dump raw notes here first (fast, no organizing).
- `Indexed/`: only put durable artifacts here (things you want to persist and reuse).
- `Indexed/user_context/`: append-only durable context for future AI sessions.

### Add new durable context (append-only)

```bash
/workspace/Indexed/user_context/append_context.sh "your text here"
```

Or via stdin:

```bash
printf "%s\n" "line 1" "line 2" | /workspace/Indexed/user_context/append_context.sh
```

This creates a new timestamped `.md` file and appends an entry to `INDEX.md`.

### Combine into a single file for reuse/sharing with an AI

```bash
/workspace/Indexed/user_context/combine_context.sh
```

Output: `Indexed/user_context/combined_user_context.md`

### Operating rules
- New context is always added as a new file (use `append_context.sh`).
- Never rewrite or “clean up” old files.
- When you need to provide context to an AI, use `combined_user_context.md`.

