import json
import os
import streamlit as st
from datetime import datetime

class NexusUtils:
    # Master Key Map for Global Sync
    KEYS = [
        "tds_state", "temp_state", "ground_resistance", # Brine
        "giza_input_db", "giza_quartz_eff", "giza_load_tons", # Giza
        "lab_chambers", "lab_baffles", "lab_valves", # Labyrinth
        "hawara_velocity", "cascade_field", "cascade_hurst", # Hawara/Perturbation
        "giza_resonance", "hawara_stability", 
        "sera_spacing", "sera_mass", "sera_dielectric", # Serapeum
        "void_len", "void_temp_c", "gallery_res_count", "gallery_tuning", # Giza Extended
        "capstone_width", "capstone_material", "wind_speed_local", "shaft_width_cm",
        "chem_type", "chem_valve_pct", "hawara_fluid", "hawara_trapdoor",
        "obelisk_height", "obelisk_width", "obelisk_count", "flood_level", "depth_cutoff"
    ]

    @staticmethod
    def generate_system_snapshot(name: str, description: str) -> str:
        """Captures the entire simulation state into a JSON packet."""
        state_data = {k: st.session_state.get(k) for k in NexusUtils.KEYS}
        
        snapshot = {
            "meta": {
                "config_name": name,
                "description": description,
                "timestamp": datetime.now().isoformat(),
                "version": "Nexus Command v1.0"
            },
            "state": state_data
        }
        return json.dumps(snapshot, indent=4)

    @staticmethod
    def load_system_snapshot(source):
        """Restores state from JSON (file or string), overwriting current settings."""
        try:
            if isinstance(source, str):
                data = json.loads(source)
            else:
                data = json.load(source)
                
            state = data.get("state", {})
            meta = data.get("meta", {})
            
            # Restore values to Session State
            for key, value in state.items():
                if value is not None:
                    st.session_state[key] = value
                    
            return True, f"Loaded Config: '{meta.get('config_name', 'Untitled')}'"
        except Exception as e:
            return False, f"Load Error: {str(e)}"

    @staticmethod
    def render_signal_path() -> str:
        """Generates the Live System Diagram based on current Session State."""
        res = st.session_state.get('ground_resistance', 150.0)
        
        # Logic Thresholds
        brine_ok = res < 10.0
        giza_ok = st.session_state.get('giza_resonance', 0.8) > 0.7
        hawara_ok = st.session_state.get('hawara_stability', 0.7) > 0.6
        
        c_brine = "green" if brine_ok else "red"
        c_giza = "green" if giza_ok else "orange"
        c_hawara = "green" if hawara_ok else "orange"
        
        return f"""
        digraph G {{
            rankdir=LR;
            bgcolor="transparent";
            node [shape=box, style="filled,rounded", fontname="Helvetica", fontcolor="white", color="white"];
            edge [color="white", fontcolor="white"];
            
            Brine [label="Aquifer Nexus\\n{res:.3f} Ω", fillcolor="{c_brine}", fontcolor="black"];
            Giza [label="Giza Generator\\n(Source)", fillcolor="{c_giza}", fontcolor="black"];
            Hawara [label="Labyrinth\\n(Regulator)", fillcolor="{c_hawara}", fontcolor="black"];
            Grid [label="Global Grid\\n(Output)", shape=ellipse, fillcolor="lightblue", fontcolor="black"];
            
            Brine -> Giza [label="Ground"];
            Brine -> Hawara [label="Protection"];
            Giza -> Hawara [label="Pulse"];
            Hawara -> Grid [label="Power"];
        }}
        """

    # --- Library Management ---
    CONFIG_DIR = "lithic_simulation/saved_configs"

    @staticmethod
    def ensure_config_dir():
        if not os.path.exists(NexusUtils.CONFIG_DIR):
            os.makedirs(NexusUtils.CONFIG_DIR)

    @staticmethod
    def save_to_library(name: str, json_data: str) -> str:
        NexusUtils.ensure_config_dir()
        # Sanitize filename
        safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '_', '-')]).strip()
        filename = f"{safe_name.replace(' ', '_')}.json"
        filepath = os.path.join(NexusUtils.CONFIG_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(json_data)
        return filename

    @staticmethod
    def list_library() -> list:
        NexusUtils.ensure_config_dir()
        files = [f for f in os.listdir(NexusUtils.CONFIG_DIR) if f.endswith('.json')]
        return sorted(files)

    @staticmethod
    def load_from_library(filename: str):
        NexusUtils.ensure_config_dir()
        filepath = os.path.join(NexusUtils.CONFIG_DIR, filename)
        with open(filepath, 'r') as f:
            return NexusUtils.load_system_snapshot(f)

    @staticmethod
    def delete_from_library(filename: str):
        NexusUtils.ensure_config_dir()
        filepath = os.path.join(NexusUtils.CONFIG_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
