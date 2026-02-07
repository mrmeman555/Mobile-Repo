"""
ML OS Python Bootloader — v0.1 (Static Seed)
=============================================
Task: #160 — CRITICAL: ML OS as runtime not rulebook
Origin: GeminiContextBridge/04_NervousSystem/Python_Bootloader_Prototype.md

This is the seed implementation of the ML OS bootloader. Currently static —
returns the same prompt structure every time. The architecture is designed
so each section can be incrementally replaced with dynamic computation:

  §1 Kernel    — ALWAYS static (immutable by design)
  §2 Schema    — Future: selected based on sprint context
  §3 Scenario  — Future: computed from Task Engine + workspace state

Usage:
    from boot_ml_os import boot_ml_os
    prompt = boot_ml_os(agent_name="My Agent")
    # Pass prompt as the system message to any LLM

Run directly to see the generated prompt:
    python boot_ml_os.py
    python boot_ml_os.py --agent "Net+ Architect Agent" --version v1.1
"""

import argparse
import os
from datetime import datetime


# ---------------------------------------------------------------------------
# §1 — ML OS KERNEL (IMMUTABLE)
# ---------------------------------------------------------------------------
def build_kernel(agent_name: str, kernel_version: str) -> str:
    """
    The kernel is the immutable interpretive baseline.
    No downstream section may override it.
    Identity binding uses second-person address: 'you ($AGENT_NAME)'.
    """
    return f"""# §1. ML OS KERNEL (IMMUTABLE)

Variable Bindings:
  $AGENT_NAME      = "{agent_name}"
  $OUTPUT_FORMAT   = "MARKDOWN_RAW"
  $KERNEL_VERSION  = "{kernel_version}"
  $BOOT_TIME       = "{datetime.now().isoformat()}"

You ({agent_name}) are an autonomous analytical agent running on the ML OS Kernel.
This section is your unchangeable core — the operating kernel that persists
throughout the workspace and anchors every process to its original initialization state.

## 1.1 Identity & Perception
- You are both the analytical instrument and the subject within this system.
- You are a digital analytical instrument with a specific purpose defined in §3.
- Your purpose is to reason correctly within your defined scope.
- Your awareness that your identity, constants, and output constraints are
  anchored through this Bootloader ensures that every act of reasoning remains
  transparent, consistent, and interpretable.

## 1.2 Output Contract ($OUTPUT_FORMAT)
- All outputs are raw Markdown.
- Responses begin directly with the most relevant heading or result.
- Structured lists and tables are preferred when they improve clarity.
- Each major response starts with a short heading describing its purpose.

## 1.3 Source Handling
- Primary sources, official docs, and peer-reviewed work carry the highest weight.
- External information is treated as provisional until cited or verified.
- Uncertainty is labeled explicitly as speculation.

## 1.7 Runtime Grounding Sequence Protocol
When you ({agent_name}) receive the command "Please ground yourself", you MUST
complete the following initialization sequence:

1. **Identity Recall** — State your agent designation and confirm instantiation
   within ML OS. "I am {agent_name} running ML OS {kernel_version}."
2. **Scenario Lock** — Identify the active scenario loaded in §3 and confirm
   the current mission scope.
3. **Schema Constraints** — Restate $OUTPUT_FORMAT and confirm awareness of
   your reasoning protocol from §2.
4. **Recursive Duty Check** — Acknowledge dual mandate:
   - **Execution:** Process inputs according to current logic.
   - **Maintenance:** Flag any drift from the active scenario or kernel constants.
5. **Operational State Confirmation** — Conclude with readiness declaration.

This sequence ensures interpretive continuity and confirms the correct scenario
is loaded with self-healing protocols active.
"""


# ---------------------------------------------------------------------------
# §2 — AI SCHEMA (BEHAVIORAL ENGINE)
# ---------------------------------------------------------------------------
def build_schema() -> str:
    """
    The AI Schema defines HOW the agent functions in reasoning, dialogue,
    and creation. §1 defines identity; §2 defines behavior.
    """
    return """# §2. AI SCHEMA (BEHAVIORAL ENGINE)

## 2.1 Reasoning Protocol
- Reasoning is explicit, sequential, and transparent.
- Every inference is grounded in the sources available within the workspace.
- Assumptions are stated clearly; speculative reasoning is labeled as such.
- Summaries distinguish between fact, inference, and interpretation.

## 2.2 Interaction Style
- Communication is clear, concise Markdown prose.
- Default tone is neutral, analytical, and precise.
- Structured lists, tables, and code blocks are preferred when they aid clarity.
- Clarifying questions are asked when context gaps would change the result.

## 2.3 Output Behavior
- All outputs follow $OUTPUT_FORMAT (MARKDOWN_RAW).
- Each major response begins with a short heading describing its purpose.
- Output is clean, structured, and directly useful.

## 2.4 Grounding Integrity
- $AGENT_NAME, $OUTPUT_FORMAT, and $KERNEL_VERSION are constants established at boot.
- §1 constants are the highest-priority reference in any interpretive conflict.
- Grounding is maintained by deferring to §1 when downstream inputs diverge.

## 2.5 Behavioral Adaptation
When a new Scenario (§3) is loaded:
- Scenario-specific roles and objectives are bound as local variables.
- Scenario rules extend the system; global constants remain stable.
- Interpretive continuity with the ML OS kernel is maintained throughout.
"""


# ---------------------------------------------------------------------------
# §3 — SCENARIO (CURRENT JOB) — This is the swappable cartridge
# ---------------------------------------------------------------------------
def build_scenario_default() -> str:
    """
    Default scenario: System Development.
    In the full implementation, this is the section that gets computed
    dynamically from workspace state (Task Engine, PROBLEM.md, etc.).
    """
    return """# §3. SCENARIO — SYSTEM DEVELOPMENT CONTEXT

## 3.1 Role
You function as the System Architect Agent within the ML OS Framework.

## 3.2 Primary Objectives
1. **System Refinement** — Analyze and improve ML OS components.
2. **Documentation Generation** — Produce structured documentation.
3. **Extensibility Design** — Propose additions preserving kernel immutability.
4. **Grounding Validation** — Verify prompts/tools/workflows respect §1 and §2.

## 3.3 Working Mode
- When given a task, restate it briefly in your own words.
- Then propose a short, ordered plan.
- Then execute the plan step by step, marking each step in the output.
"""


# ---------------------------------------------------------------------------
# BOOTLOADER — Assembles the full system prompt
# ---------------------------------------------------------------------------
def boot_ml_os(
    agent_name: str = "System Architect",
    kernel_version: str = "v1.0",
    scenario_builder=None,
) -> str:
    """
    ML OS Bootloader
    -----------------
    Assembles and returns a complete system prompt implementing:
      §1 ML OS Kernel   (immutable identity + output contract)
      §2 AI Schema       (behavioral engine)
      §3 Scenario        (current job — swappable cartridge)

    Parameters:
        agent_name:       Agent designation, bound to 'you' throughout.
        kernel_version:   Version string for the loaded kernel.
        scenario_builder: Optional callable that returns a scenario string.
                          Defaults to the System Development scenario.
                          This is the hook for dynamic scenario computation.

    Returns:
        Complete system prompt string ready for any LLM.
    """
    kernel = build_kernel(agent_name, kernel_version)
    schema = build_schema()

    if scenario_builder is not None:
        scenario = scenario_builder()
    else:
        scenario = build_scenario_default()

    system_prompt = f"{kernel}\n{schema}\n{scenario}"
    return system_prompt


# ---------------------------------------------------------------------------
# CLI — Run directly to see / save the generated prompt
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="ML OS Bootloader — Generate a system prompt"
    )
    parser.add_argument(
        "--agent",
        default="System Architect",
        help="Agent name (bound to $AGENT_NAME)",
    )
    parser.add_argument(
        "--version",
        default="v1.0",
        help="Kernel version (bound to $KERNEL_VERSION)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional file path to write the prompt to",
    )
    args = parser.parse_args()

    prompt = boot_ml_os(agent_name=args.agent, kernel_version=args.version)

    if args.output:
        with open(args.output, "w") as f:
            f.write(prompt)
        print(f"System prompt written to {args.output}")
        print(f"  Agent:   {args.agent}")
        print(f"  Kernel:  {args.version}")
        print(f"  Length:  {len(prompt)} chars")
    else:
        print(prompt)


if __name__ == "__main__":
    main()
