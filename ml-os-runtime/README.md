# ML OS Runtime — Python Bootloader

> **Status:** v0.1 — Static seed, ready for dynamic extension
> **Task:** #160 — ML OS as runtime not rulebook
> **Date:** 2026-02-07

---

## What This Is

The Python implementation of the ML OS bootloader. Instead of static markdown
rules that agents read and try to follow, this computes the system prompt
programmatically — turning ML OS from a rulebook into a runtime.

## Architecture

```
boot_ml_os(agent_name, kernel_version, scenario_builder)
    │
    ├── build_kernel()      → §1 ML OS Kernel (IMMUTABLE — always hardcoded)
    ├── build_schema()      → §2 AI Schema (behavioral engine)
    └── build_scenario()    → §3 Scenario (swappable cartridge)
                                  ↑
                          This is the hook for dynamic computation.
                          Pass a custom scenario_builder function to
                          compute §3 from live workspace state.
```

## Usage

```bash
# Print the default system prompt
python boot_ml_os.py

# Custom agent name and version
python boot_ml_os.py --agent "Net+ Architect Agent" --version v1.1

# Save to file
python boot_ml_os.py --agent "Nervous System Architect" --output prompt.md
```

```python
# Use as a library
from boot_ml_os import boot_ml_os

prompt = boot_ml_os(agent_name="My Agent", kernel_version="v1.0")
# Pass prompt as system message to any LLM
```

## Extension Points

The bootloader is designed for incremental extension. Each section can be
replaced with dynamic computation independently:

| Section | Current | Target |
|---|---|---|
| §1 Kernel | Static (immutable by design) | Same — kernel never changes |
| §2 Schema | Static behavioral rules | Select variant based on sprint context |
| §3 Scenario | Static default objectives | Compute from Task Engine + workspace state |
| Context | None | Read workspace files, recent changes, transcript history |
| Tools | None | Discover available tools and inject descriptions |

## Custom Scenarios

```python
def my_scenario():
    return """# §3. SCENARIO — MY CUSTOM MISSION
    ## 3.1 Role
    You are a specialized agent for [task].
    ## 3.2 Objectives
    1. [Objective 1]
    2. [Objective 2]
    """

prompt = boot_ml_os(
    agent_name="Custom Agent",
    scenario_builder=my_scenario,
)
```

## File Structure

```
ml-os-runtime/
├── README.md           ← This file
└── boot_ml_os.py       ← The bootloader (v0.1 — static seed)
```

## Lineage

- **Theory:** Mobile-Repo architecture docs (embedding theory, kernel/cartridge separation)
- **Prototype:** GeminiContextBridge/04_NervousSystem/Python_Bootloader_Prototype.md
- **Proof:** Case Study 001 (Net+ Autonomous Grounding) — documented in GeminiContextBridge
