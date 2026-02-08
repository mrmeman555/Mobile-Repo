# Pyramids / Lithic Circuit Project

Date: 2026-02-07
Tags: pyramids, lithic-circuit, bayesian, physics-simulation, deep-research

## Overview

The "Lithic Circuit" hypothesis proposes that the Great Pyramid of Giza, the Serapeum of Saqqara, and the Hawara Labyrinth function as components of a distributed geo-mechanical/electro-acoustic system. This project combines **Bayesian statistical validation** with **physics simulation** (Streamlit) to test the hypothesis rigorously.

## Directory Structure

```
pyramids/
├── code/                          # Streamlit simulation codebase
│   └── lithic_simulation/         # 18 Python modules + tests
│       ├── app.py                 # Main Streamlit dashboard
│       ├── acoustics.py           # Giza acoustic resonance (Strouhal/Helmholtz)
│       ├── piezo.py               # Piezoelectric conversion
│       ├── serapeum_engine.py     # Serapeum LRSM/capacitance
│       ├── hawara_engine.py       # Hawara hydraulic pulse
│       ├── network_engine.py      # Global network (obelisks, aquifer, geomagnetic)
│       ├── bayesian_engine.py     # Bayesian verdict calculator
│       ├── bayesian_graph.py      # Bayesian visualization
│       ├── brine_engine.py        # Brine chemistry
│       ├── chemical_engine.py     # Chemical processes
│       ├── component_x_engine.py  # Speculative component module
│       ├── perturbation_engine.py # Perturbation analysis
│       ├── thermal_engine.py      # Thermal modeling
│       ├── valve_farm.py          # Hydraulic valve farm
│       ├── visualization_3d.py    # 3D visualization
│       ├── config.py              # Configuration
│       ├── materials.py           # Material properties
│       ├── dashboard_utils.py     # Dashboard utilities
│       ├── testing_engine.py      # Testing framework
│       ├── requirements.txt       # Python dependencies
│       └── tests/                 # Unit tests
│           └── test_physics.py
├── research/                      # Research papers and reports
│   ├── bayesian_docs/
│   │   ├── Omni_Specialist_Protocol.md   # Full Bayesian framework paper
│   │   └── citations.md                  # Annotated bibliography
│   ├── deep_research_examples/
│   │   ├── Bayesian Data Audit_ Ancient Artifacts.md
│   │   ├── Bayesian Validation of Lithic Circuit.md
│   │   ├── Lithic Circuit Support Infrastructure Investigation.md
│   │   └── Max_Zamilov_Pyramid_Engineering_Prompt.md
│   └── roundtable_reports/
│       ├── UnchartedX_PreDynastic_Engineering_Audit.md
│       ├── Labyrinth Manifold_ AI Research Prompt.md
│       └── LabyrinthManifold_Supplement.md
├── transcripts/                   # AI session transcripts
│   ├── claude-transcript-nov24.txt    # Claude: Serapeum as Phononic Crystal
│   └── Grok-transcript-Nov24.txt      # Grok: Extended pyramid analysis
└── project_docs/                  # Project management docs
    ├── PyramidCode_README.md          # Original project README
    ├── Module5_Prompt.md              # Module 5 (Global Network) engineering prompt
    ├── AUDIT_REPORT.md                # Codebase integrity audit
    ├── TODO.md                        # Development roadmap
    └── taskmanagement_project_card.md # TaskManagement project card
```

## Key Modules

| Module | Simulates | Key Physics |
|---|---|---|
| **Giza Generator** | Great Pyramid resonant acoustics | Strouhal/Helmholtz resonance |
| **Serapeum Capacitor** | LRSM phononic crystal + capacitance | Locally Resonant Sonic Materials |
| **Hawara Regulator** | Hydraulic pulse + piezoelectric conversion | Joukowsky pressure, piezo coupling |
| **Global Network** | Obelisk antennas + aquifer switches + geomagnetic field | Cantilever beam vibration, Laschamp Event |
| **Bayesian Verdict** | Statistical hypothesis testing | Hierarchical Bayesian Modeling |

## Research Papers

1. **Omni-Specialist Protocol** — Hierarchical Bayesian Framework for validating the Lithic Circuit hypothesis. Full academic-style paper with methodology and results.
2. **K-Factor Forensic Audit** — Statistical metrology and material physics of Old Kingdom artifacts.
3. **Infrastructure Investigation** — Dahshur-Abu Gorab-Giza triad as a 9.8 MW planetary circuit.
4. **UnchartedX Engineering Audit** — Forensic reconstruction of Pre-Dynastic technological capabilities.
5. **Labyrinth Manifold** — Hawara as hydraulic pulse regulator (Manifold Interaction Architecture).
6. **Max Zemlyanov Research Prompt** — Extraction prompt for pyramid resonance/engineering claims.

## Source Locations (Full Workspace)

- Simulation code: `/home/aaron/Projects/Pyramids/PyramidCode/`
- Deep Research examples: `/mnt/share/Projects/Working0/Archive/Sprints/Sprint_DeepResearchFactory/examples/`
- Roundtable reports: `/mnt/share/Projects/Working0/Archive/Sprints/Sprint_DeepResearchFactory/Docs/Roundtable_Output_Reports/`
- IP-Lock proofs: `/home/aaron/Projects/Pyramids/PyramidCode/proofs/` (11,350 files)

## Not Included Here

- Screen recordings (4 `.webm` files — too large for mobile)
- `GPT-Pyramid-Admission.pdf` (binary PDF)
- Python venv, `__pycache__`, proof JSONs
