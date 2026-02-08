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
│   ├── roundtable_reports/
│   │   ├── UnchartedX_PreDynastic_Engineering_Audit.md
│   │   ├── Labyrinth Manifold_ AI Research Prompt.md
│   │   └── LabyrinthManifold_Supplement.md
│   └── agent_reports/             # Converted from .docx (NotebookLM/AI agent outputs)
│       ├── Analyzing Schumann Resonance Coupling in Stone.md
│       ├── Bayesian Analysis of Egyptian _Lithic Circuit_.md
│       ├── Bayesian Data Audit_ Ancient Artifacts.md
│       ├── Bayesian Validation of Lithic Circuit.md
│       ├── Critiquing Ancient Acoustic Claims.md
│       ├── Forensic Analysis_ Lost Sarcophagus Insert.md
│       ├── Forensic Analysis of King_s Chamber Coffer.md
│       ├── Forensic Coffer Insert Reconstruction Protocol.md
│       ├── Geomagnetic Anomalies and Megalithic Sites.md
│       ├── Giza Subterranean Infrastructure Investigation.md
│       ├── Hawara Hydro-Processor Technical Assessment.md
│       ├── King_s Chamber Coffer Dimple Research Pack.md
│       ├── Labyrinth Manifold_ AI Research Prompt.md
│       ├── Lithic Circuit_ Ancient Egyptian Engineering.md
│       ├── Lithic Circuit Support Infrastructure Investigation.md
│       ├── Metamaterial Seismic Damping Analysis.md
│       ├── Piezoelectric Stone Degradation Analysis.md
│       └── Serapeum Box Insert Forensics.md
├── transcripts/                   # AI session transcripts
│   ├── claude-transcript-nov24.txt        # Claude: Serapeum as Phononic Crystal (Nov 24)
│   ├── Claude-PyramidTranscript-Nov26-25.md # Claude: Full pyramid analysis (Nov 26, 365K)
│   ├── GPT-Pyramid-Nov26-25.md            # GPT: Pyramid analysis transcript (Nov 26, 227K)
│   ├── Gemini-PythonSim-Nov26-25.md       # Gemini: Simulation discussion (Nov 26, 47K)
│   └── Grok-transcript-Nov24.txt          # Grok: Extended pyramid analysis (Nov 24)
├── images/                        # Diagrams and screenshots
│   ├── Lithic_Circuit_Master_Archive.png  # Master circuit diagram
│   └── Screenshot_20251130_*.jpg (×15)    # ChatGPT session screenshots
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

### Core Papers (bayesian_docs/ + deep_research_examples/)
1. **Omni-Specialist Protocol** — Hierarchical Bayesian Framework for validating the Lithic Circuit hypothesis.
2. **K-Factor Forensic Audit** — Statistical metrology and material physics of Old Kingdom artifacts.
3. **Infrastructure Investigation** — Dahshur-Abu Gorab-Giza triad as a 9.8 MW planetary circuit.
4. **UnchartedX Engineering Audit** — Forensic reconstruction of Pre-Dynastic technological capabilities.
5. **Labyrinth Manifold** — Hawara as hydraulic pulse regulator (Manifold Interaction Architecture).
6. **Max Zemlyanov Research Prompt** — Extraction prompt for pyramid resonance/engineering claims.

### Agent Reports (agent_reports/ — converted from .docx)
7. **Schumann Resonance Coupling in Stone** — Analysis of Schumann resonance interaction with stone structures.
8. **Critiquing Ancient Acoustic Claims** — Critical assessment of acoustic anomaly interpretations.
9. **Forensic Analysis: Lost Sarcophagus Insert** — Reconstruction of missing sarcophagus component.
10. **Forensic Analysis of King's Chamber Coffer** — Engineering analysis of the coffer's physical properties.
11. **Forensic Coffer Insert Reconstruction Protocol** — Protocol for reconstructing the coffer insert.
12. **King's Chamber Coffer Dimple Research Pack** — Investigation of surface anomalies on the coffer.
13. **Geomagnetic Anomalies and Megalithic Sites** — Correlation between geomagnetic fields and site placement.
14. **Giza Subterranean Infrastructure Investigation** — Analysis of underground structures at Giza.
15. **Hawara Hydro-Processor Technical Assessment** — Engineering assessment of Hawara as hydraulic processor.
16. **Metamaterial Seismic Damping Analysis** — Analysis of metamaterial properties in stone structures.
17. **Piezoelectric Stone Degradation Analysis** — Study of piezoelectric property degradation over time.
18. **Serapeum Box Insert Forensics** — Forensic analysis of Serapeum sarcophagi insert mechanisms.
19. **Lithic Circuit: Ancient Egyptian Engineering** — Overview of the Lithic Circuit engineering hypothesis.

## Source Locations (Full Workspace)

- Simulation code: `/home/aaron/Projects/Pyramids/PyramidCode/`
- Deep Research examples: `/mnt/share/Projects/Working0/Archive/Sprints/Sprint_DeepResearchFactory/examples/`
- Roundtable reports: `/mnt/share/Projects/Working0/Archive/Sprints/Sprint_DeepResearchFactory/Docs/Roundtable_Output_Reports/`
- IP-Lock proofs: `/home/aaron/Projects/Pyramids/PyramidCode/proofs/` (11,350 files)

## Transcripts (5 total)

| File | Platform | Date | Size | Content |
|---|---|---|---|---|
| `Transcript_Pyramid_Transcript.md` | Claude | Nov 23+ | 277K / 9511 lines | Full Claude pyramid session — Serapeum phononic crystal, Lithic Circuit analysis |
| `claude-transcript-nov24.txt` | Claude | Nov 24 | ~762 lines | Serapeum as Phononic Crystal |
| `Claude-PyramidTranscript-Nov26-25.md` | Claude | Nov 26 | 365K | Full pyramid analysis (extended) |
| `GPT-Pyramid-Nov26-25.md` | GPT | Nov 26 | 227K | Pyramid engineering analysis |
| `Gemini-PythonSim-Nov26-25.md` | Gemini | Nov 26 | 47K | Simulation discussion |
| `Grok-transcript-Nov24.txt` | Grok | Nov 24 | ~7920 lines | Extended pyramid analysis |

## Not Included Here

- Screen recordings (4 `.webm` files — too large for mobile)
- `GPT-Pyramid-Admission.pdf` / `Lithic_Circuit_Archive.pdf` (binary PDFs)
- Python venv, `__pycache__`, proof JSONs (11,350 files)
- GrokBackup JSON (pyramid mentions embedded in full export)
