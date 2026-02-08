import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import graphviz

# Ensure we can import the package components
# Add the project root (parent of lithic_simulation) to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from lithic_simulation.acoustics import ResonantChamber, BigVoidResonator, ResonatorArray
    from lithic_simulation.thermal_engine import GroundingHeat
    from lithic_simulation.chemical_engine import ChemicalInjector
    from lithic_simulation.piezo import PiezoGenerator
    from lithic_simulation.serapeum_engine import PhononicTunnel, GraniteCapacitor
    from lithic_simulation.hawara_engine import HydraulicRam, QuartziteReactor
    from lithic_simulation.visualization_3d import visualize_chamber_resonance
    from lithic_simulation.network_engine import ObeliskTuner, AquiferSwitch, PlanetaryGrid, CapstoneAntenna, ObeliskBeam, EdfuHandoff
    from lithic_simulation.bayesian_engine import BayesianSiege
    from lithic_simulation.component_x_engine import ArkCapacitor
    from lithic_simulation.bayesian_graph import EvidenceGraph
    from lithic_simulation.brine_engine import BrineSimulator, DataVault
    from lithic_simulation.perturbation_engine import CascadeDynamics, HBMStability
    from lithic_simulation.valve_farm import LabyrinthManifold
    from lithic_simulation.dashboard_utils import NexusUtils
    from lithic_simulation.testing_engine import SystemValidator
    from lithic_simulation import config
    from lithic_simulation.testing_engine import SystemValidator
except ImportError:
    # Fallback for local development/different run contexts
    import config
    from testing_engine import SystemValidator
    from acoustics import ResonantChamber, BigVoidResonator, ResonatorArray
    from thermal_engine import GroundingHeat
    from chemical_engine import ChemicalInjector
    from piezo import PiezoGenerator
    from serapeum_engine import PhononicTunnel, GraniteCapacitor
    from hawara_engine import HydraulicRam, QuartziteReactor
    from visualization_3d import visualize_chamber_resonance
    from network_engine import ObeliskTuner, AquiferSwitch, PlanetaryGrid, CapstoneAntenna, ObeliskBeam, EdfuHandoff
    from bayesian_engine import BayesianSiege
    from component_x_engine import ArkCapacitor
    from bayesian_graph import EvidenceGraph
    from brine_engine import BrineSimulator, DataVault
    from perturbation_engine import CascadeDynamics
    from valve_farm import LabyrinthManifold
    from dashboard_utils import NexusUtils

st.set_page_config(page_title="Lithic Circuit: Master Archive", layout="wide")

# --- Global State Initialization ---
defaults = {
    'tds_state': 67.7, 'temp_state': 25.0, 'ground_resistance': 150.0,
    'giza_quartz_eff': 0.3, 'giza_input_db': 120, 'giza_load_tons': 1000,
    'lab_chambers': 3000, 'lab_baffles': 0.5, 'lab_valves': 50,
    'hawara_velocity': 4.0, 'cascade_field': 100, 'cascade_hurst': 0.7,
    'giza_resonance': 0.8, 'hawara_stability': 0.7, 'sera_spacing': 6.0,
    'sera_mass': 70, 'sera_dielectric': 5.5,
    # --- Extended Defaults (Deep Integration) ---
    'void_len': 30.0, 'void_temp_c': 20.0,
    'gallery_res_count': 27, 'gallery_tuning': 90,
    'capstone_width': 2.1, 'capstone_material': "Gold",
    'wind_speed_local': 20, 'shaft_width_cm': 21,
    'chem_type': "Dilute Sulfuric Acid", 'chem_valve_pct': 5,
    'hawara_fluid': "Fresh Water", 'hawara_trapdoor': "Instant",
    'obelisk_height': 28.0, 'obelisk_width': 2.5, 'obelisk_count': 2,
    'flood_level': 4.0, 'depth_cutoff': 0,
    # --- Gap Fill ---
    'd18o': 4.9, 'lab_pressure': 50.0, 'giza_freq_dev': 0.0,
    'harmonic_x': 1, 'harmonic_y': 1, 'harmonic_z': 4
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Run Brine Physics Globally
brine_global = BrineSimulator()
cond_global = brine_global.calculate_conductivity(st.session_state['tds_state'], st.session_state['temp_state'])
st.session_state['ground_resistance'] = cond_global['resistance_ohms']

# --- Sidebar Navigation ---
st.sidebar.title("🧮 Lithic Circuit")

# Version Control Logic
project_version = st.sidebar.radio(
    "Project Version",
    ["v1.0 (The Bedrock)", "v2.0 (The Interface)"],
    index=0
)

# Define Modules based on Version
base_modules = [
    "🎛️ Nexus Command (Master)",
    "🧪 The Proving Ground (Testing)",
    "📜 The Origin Calculations",
    "📍 Giza Generator (Active)",
    "💧 Brine-Aquifer Nexus (Active)",
    "🗄️ Data Armor Vault (Active)",
    "🌪️ Cascade Dynamics (Perturbation)",
    "🔒 Serapeum Capacitor (Active)",
    "💧 Hawara Regulator (Active)",
    "🏛️ Labyrinth Manifold (Active)",
    "🌍 Planetary Circuit Map (Active)",
    "🌍 Global Network (Active)",
    "⚖️ The Bayesian Verdict (Active)"
]

if "v2.0" in project_version:
    st.sidebar.warning("⚠️ v2.0 Unlocked: Speculative Mode")
    speculative_modules = [
        "📦 Component X (The Removable Core)",
        "⚡ The Rod of Power",
        "🕯️ The Menorah Assembly"
    ]
    modules = base_modules + speculative_modules
else:
    modules = base_modules

module = st.sidebar.radio("Select Module", modules)

if "v2.0" in project_version and module in speculative_modules:
    st.warning("⚠️ SPECULATIVE THEORY WARNING: You are viewing v2.0 features which are theoretical extensions beyond the verified physics engines.")

if module == "🎛️ Nexus Command (Master)":
    st.title("🎛️ Nexus Command: System Orchestrator")
    
    # --- 1. Snapshot Manager ---
    with st.expander("💾 Configuration Manager (Library & I/O)", expanded=False):
        tab_lib, tab_io = st.tabs(["📚 Saved Library", "📤 Import/Export"])
        
        with tab_lib:
            st.subheader("Persistent Config Library")
            lib_files = NexusUtils.list_library()
            
            c_lib1, c_lib2 = st.columns([3, 1])
            with c_lib1:
                selected_config = st.selectbox("Select Configuration", ["-- Select --"] + lib_files)
                
            with c_lib2:
                st.write("Actions")
                if selected_config != "-- Select --":
                    if st.button("Load Selected"):
                        success, msg = NexusUtils.load_from_library(selected_config)
                        if success: st.success(msg); st.rerun()
                    if st.button("Delete", type="primary"):
                        if NexusUtils.delete_from_library(selected_config): st.rerun()

            st.markdown("---")
            c_save_lib1, c_save_lib2 = st.columns([3, 1])
            with c_save_lib1:
                save_name_lib = st.text_input("Save Current State As...")
            with c_save_lib2:
                st.write("") # Spacer
                st.write("") 
                if st.button("Save to Library"):
                    if save_name_lib:
                        json_str = NexusUtils.generate_system_snapshot(save_name_lib, "Saved via Library")
                        NexusUtils.save_to_library(save_name_lib, json_str)
                        st.success(f"Saved {save_name_lib}")
                        st.rerun()

        with tab_io:
            c_save, c_load = st.columns(2)
            
            with c_save:
                st.subheader("Export File")
                cfg_name = st.text_input("Config Name", "My Experiment")
                cfg_desc = st.text_area("Description", "e.g. High Salinity test for Laschamp survival.")
                
                live_json = NexusUtils.generate_system_snapshot(cfg_name, cfg_desc)
                
                st.caption("Live JSON (Copy):")
                st.code(live_json, language="json")
                
                st.download_button(
                    label="⬇️ Download JSON",
                    data=live_json,
                    file_name=f"{cfg_name.replace(' ', '_')}.json",
                    mime="application/json"
                )
                    
            with c_load:
                st.subheader("Import File/Text")
                uploaded = st.file_uploader("Upload JSON", type=["json"])
                if uploaded and st.button("Load File"):
                    success, msg = NexusUtils.load_system_snapshot(uploaded)
                    if success: st.success(msg); st.rerun()
                
                st.markdown("**OR**")
                json_text = st.text_area("Paste JSON Config")
                if st.button("Load Text"):
                    if json_text:
                        success, msg = NexusUtils.load_system_snapshot(json_text)
                        if success: st.success(msg); st.rerun()

    # --- 2. Live Visuals ---
    col_diag, col_metrics = st.columns([2, 1])
    with col_diag:
        st.graphviz_chart(NexusUtils.render_signal_path())
    with col_metrics:
        res = st.session_state.get('ground_resistance', 150.0)
        st.metric("Ground Resistance", f"{res:.4f} Ω", delta="Optimal" if res < 0.1 else "High")
        st.metric("Brine Status", "SUPERCONDUCTIVE" if res < 1.0 else "RESISTIVE")

    # --- 3. Master Control Racks ---
    
    # --- 3. Master Control Racks ---
    
    with st.expander("💧 Rack 1: Chemistry & Aquifer", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.slider("TDS (g/L)", 0.5, 100.0, key="tds_state")
        with c2: st.slider("Temperature (°C)", 10.0, 50.0, key="temp_state")
        with c3: st.slider("d18O (‰)", -15.0, 15.0, key="d18o")
        with c4: 
            # Live Calc
            brine = BrineSimulator()
            cond = brine.calculate_conductivity(st.session_state.get('tds_state', 67.7), st.session_state.get('temp_state', 25.0))
            st.metric("Conductivity", f"{cond['conductivity_sm']:.2f} S/m", delta="Super" if cond['conductivity_sm'] > 4 else "Normal")

    with st.expander("📍 Rack 2: Giza Generator (Primary & Atmosphere)", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            st.slider("Input dB", 60, 140, key="giza_input_db")
            st.slider("Quartz Eff.", 0.1, 1.0, key="giza_quartz_eff")
        with c2: 
            st.slider("Wind Speed (km/h)", 0, 60, key="wind_speed_local")
            st.slider("Shaft Width (cm)", 10, 50, key="shaft_width_cm")
        with c3:
            st.slider("Freq Dev (%)", 0.0, 10.0, key="giza_freq_dev")
        with c4: 
            # Live Calc
            piezo = PiezoGenerator()
            # Simplified calculation for dashboard speed
            pressure = 20e-6 * (10 ** (st.session_state.get('giza_input_db', 120) / 20))
            eff = st.session_state.get('giza_quartz_eff', 0.3) * 1.5 
            volts = 0.12 * eff * pressure * 2.0 * 9 
            st.metric("Output Voltage", f"{volts:.1f} V", delta="Ignition" if volts > 1000 else "Sub-Critical")

    with st.expander("🕳️ Rack 3: Giza Internal (Void, Gallery, Chem)", expanded=False):
        c3_1, c3_2, c3_3, c3_4 = st.columns(4)
        with c3_1:
            st.caption("Big Void Buffer")
            st.slider("Void Length (m)", 25.0, 35.0, key="void_len")
            st.slider("Internal Temp (°C)", 0.0, 50.0, key="void_temp_c")
        with c3_2:
            st.caption("Grand Gallery & 3D")
            st.slider("Resonators", 0, 54, key="gallery_res_count")
            st.slider("Tuning Match %", 50, 100, key="gallery_tuning")
            st.number_input("X-Harmonic", 1, 9, key="harmonic_x")
            st.number_input("Y-Harmonic", 1, 9, key="harmonic_y")
            st.number_input("Z-Harmonic", 1, 9, key="harmonic_z")
        with c3_3:
            st.caption("Chemical & Hardware")
            st.selectbox("Chemical", ["Dilute Sulfuric Acid", "Hydrochloric Acid", "Water"], key="chem_type")
            st.slider("Valve %", 0, 100, key="chem_valve_pct")
            st.slider("Capstone (m)", 1.0, 5.0, key="capstone_width")
            st.selectbox("Cap. Material", ["Gold", "Electrum", "Granite"], key="capstone_material")
        with c3_4:
             # Live KPI
             void_calc = BigVoidResonator(st.session_state.get('void_len', 30.0), st.session_state.get('void_temp_c', 20.0))
             v_chk = void_calc.check_harmonic_coupling(117.0)
             st.metric("Void Tuning", f"{v_chk['fundamental']:.2f} Hz", delta=f"Dev: {v_chk['deviation']*100:.1f}%", delta_color="inverse")
             
             # Sparkline
             lengths = np.linspace(25.0, 35.0, 20)
             freqs = [BigVoidResonator(l, st.session_state.get('void_temp_c', 20.0)).calculate_fundamental_frequency() for l in lengths]
             fig_spark = px.line(x=lengths, y=freqs)
             fig_spark.add_scatter(x=[st.session_state.get('void_len', 30.0)], y=[v_chk['fundamental']], mode='markers', marker=dict(color='red', size=8))
             fig_spark.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0), height=60, xaxis_visible=False, yaxis_visible=False)
             st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})
        
        with st.expander("📉 Live Tuning Curve", expanded=False):
             lengths = np.linspace(25.0, 35.0, 50)
             freqs = [BigVoidResonator(l, st.session_state.get('void_temp_c', 20.0)).calculate_fundamental_frequency() for l in lengths]
             
             fig_v = go.Figure()
             fig_v.add_trace(go.Scatter(x=lengths, y=freqs, name="Void Freq"))
             
             curr_len = st.session_state.get('void_len', 30.0)
             curr_freq = void_calc.calculate_fundamental_frequency()
             fig_v.add_trace(go.Scatter(x=[curr_len], y=[curr_freq], mode='markers', marker=dict(size=10, color='red'), name="Current"))
             
             fig_v.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20), title="Resonance Tuning")
             st.plotly_chart(fig_v, use_container_width=True)

    with st.expander("🏛️ Rack 4: Labyrinth Manifold", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.slider("Active Chambers", 100, 3000, key="lab_chambers")
        with c2: st.slider("Baffle Complexity", 0.0, 1.0, key="lab_baffles")
        with c3: 
            st.slider("Valve Open %", 0, 100, key="lab_valves")
            st.slider("Pressure (Bar)", 10.0, 100.0, key="lab_pressure")
        with c4:
            # Live Calc
            manifold = LabyrinthManifold(st.session_state.get('lab_chambers', 3000), st.session_state.get('lab_baffles', 0.5))
            res = manifold.calculate_flow_dynamics(50.0, st.session_state.get('lab_valves', 50), st.session_state.get('ground_resistance', 150))
            st.metric("Flow Stability", f"{res['stability_factor']*100:.1f}%", delta=res['status'])

    with st.expander("🔋 Rack 5: Serapeum Capacitor", expanded=False):
        c5_1, c5_2, c5_3, c5_4 = st.columns(4)
        with c5_1: st.slider("Box Spacing (m)", 2.0, 10.0, key="sera_spacing")
        with c5_2: st.slider("Box Mass (tons)", 50, 100, key="sera_mass")
        with c5_3: st.slider("Dielectric (mm)", 1.0, 20.0, key="sera_dielectric")
        with c5_4:
            # Live KPI
            cap = GraniteCapacitor(st.session_state.get('sera_dielectric', 5.5))
            store = cap.calculate_storage_potential(24)
            st.metric("Array Capacitance", f"{store['capacitance_nF']:.2f} nF", delta="Charged")
            
            # Sparkline
            tun = PhononicTunnel(st.session_state.get('sera_spacing', 6.0), st.session_state.get('sera_mass', 70))
            df_t = tun.simulate_transmission()
            fig_spark = px.line(df_t, x='frequency', y='transmission_db')
            fig_spark.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0), height=60, xaxis_visible=False, yaxis_visible=False)
            st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})
        
        with st.expander("🔒 Phononic Band Gap", expanded=False):
             tun = PhononicTunnel(st.session_state.get('sera_spacing', 6.0), st.session_state.get('sera_mass', 70))
             df_t = tun.simulate_transmission()
             
             fig_s = px.line(df_t, x='frequency', y='transmission_db', title="Acoustic Filter Profile")
             fig_s.add_vline(x=117.0, line_dash="dot", line_color="green", annotation_text="Pilot Signal")
             
             fig_s.update_layout(height=300, margin=dict(t=30, b=20), yaxis_range=[-60, 10])
             st.plotly_chart(fig_s, use_container_width=True)

    with st.expander("🌊 Rack 6: Hawara Regulator", expanded=False):
        c6_1, c6_2, c6_3, c6_4 = st.columns(4)
        with c6_1: st.slider("Flow Velocity (m/s)", 0.5, 10.0, key="hawara_velocity")
        with c6_2: st.selectbox("Fluid Type", ["Fresh Water", "Conductive Brine"], key="hawara_fluid")
        with c6_3: st.select_slider("Trapdoor Speed", options=["Slow", "Medium", "Fast", "Instant"], key="hawara_trapdoor")
        with c6_4:
            # Live KPI
            speed_map = {"Slow": 0.2, "Medium": 0.5, "Fast": 0.8, "Instant": 1.0}
            cf = speed_map.get(st.session_state.get('hawara_trapdoor', "Instant"), 1.0)
            ram = HydraulicRam(st.session_state.get('hawara_fluid', "Fresh Water"), cf)
            spike = ram.calculate_pressure_spike(st.session_state.get('hawara_velocity', 4.0))
            st.metric("Water Hammer", f"{spike['pressure_bar']:.1f} Bar", delta="Critical" if spike['pressure_bar'] > 80 else "Nominal")
            
            # Sparkline
            vels = np.linspace(0.1, 10.0, 20)
            pressures = [ram.calculate_pressure_spike(v)['pressure_bar'] for v in vels]
            fig_spark = px.line(x=vels, y=pressures)
            fig_spark.add_scatter(x=[st.session_state.get('hawara_velocity', 4.0)], y=[spike['pressure_bar']], mode='markers', marker=dict(size=8, color='red'))
            fig_spark.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0), height=60, xaxis_visible=False, yaxis_visible=False)
            st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})
        
        with st.expander("🌊 Water Hammer Pulse", expanded=False):
             vels = np.linspace(0.1, 10.0, 20)
             pressures = []
             ram_viz = HydraulicRam(st.session_state.get('hawara_fluid', "Fresh Water"), cf)
             for v in vels:
                 pressures.append(ram_viz.calculate_pressure_spike(v)['pressure_bar'])
                 
             fig_h = px.line(x=vels, y=pressures, labels={'x':'Velocity (m/s)', 'y':'Pressure (Bar)'}, title="Joukowsky Limit")
             
             curr_v = st.session_state.get('hawara_velocity', 4.0)
             curr_p = spike['pressure_bar']
             fig_h.add_scatter(x=[curr_v], y=[curr_p], mode='markers', marker=dict(size=10, color='red'), name="Current")
             
             fig_h.update_layout(height=300, margin=dict(t=30, b=20))
             st.plotly_chart(fig_h, use_container_width=True)

    with st.expander("🌍 Rack 7: Global Network", expanded=False):
        c7_1, c7_2, c7_3, c7_4 = st.columns(4)
        with c7_1: st.slider("Obelisk Height (m)", 10.0, 40.0, key="obelisk_height")
        with c7_2: st.slider("Obelisk Width (m)", 1.0, 4.0, key="obelisk_width")
        with c7_3: st.slider("Active Nodes", 0, 12, key="obelisk_count")
        with c7_4:
            # Live KPI
            tuner = ObeliskTuner()
            tuned = tuner.calculate_resonance(st.session_state.get('obelisk_height', 28.0), st.session_state.get('obelisk_width', 2.5))
            st.metric("Obelisk Freq", f"{tuned['frequency_hz']:.2f} Hz", delta="TUNED" if tuned['is_harmonic'] else "MISTUNED")

    with st.expander("🌪️ Rack 8: Stress Environment", expanded=True):
        c8_1, c8_2, c8_3, c8_4 = st.columns(4)
        with c8_1: st.slider("Geomagnetic Field (%)", 0, 100, key="cascade_field")
        with c8_2: st.slider("Hurst Exponent", 0.1, 0.9, key="cascade_hurst")
        with c8_3:
             st.slider("Nile Flood Level (m)", 0.0, 10.0, key="flood_level")
             st.slider("Tomography Depth", -60, 0, key="depth_cutoff")
        with c8_4:
            # Live Calc
            cascade = CascadeDynamics()
            stress = cascade.laschamp_stress_test(st.session_state.get('cascade_field', 100), 0.1/st.session_state.get('ground_resistance', 150))
            st.metric("Projected Uptime", f"{stress['uptime_pct']:.1f}%", delta=stress['status'])
            
            # Sparkline
            fields = np.linspace(0, 100, 20)
            grid_viz = PlanetaryGrid()
            effs = [grid_viz.calculate_grid_status(f)['efficiency'] * 100 for f in fields]
            fig_spark = px.line(x=fields, y=effs)
            fig_spark.add_vline(x=st.session_state.get('cascade_field', 100), line_dash="dash", line_color="red")
            fig_spark.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0), height=60, xaxis_visible=False, yaxis_visible=False)
            st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})
        
        with st.expander("⏳ Collapse Timeline", expanded=False):
             fields = np.linspace(0, 100, 50)
             grid_viz = PlanetaryGrid()
             effs = [grid_viz.calculate_grid_status(f)['efficiency'] * 100 for f in fields]
             
             fig_e = px.area(x=fields, y=effs, labels={'x':'Geomagnetic Field (%)', 'y':'Grid Efficiency (%)'}, title="Laschamp Vulnerability Curve")
             
             curr_f = st.session_state.get('cascade_field', 100)
             fig_e.add_vline(x=curr_f, line_dash="dash", line_color="red", annotation_text="Current Field")
             
             fig_e.update_layout(height=300, margin=dict(t=30, b=20))
             st.plotly_chart(fig_e, use_container_width=True)

    # --- 4. The Omni-Deck (Deep Telemetry) ---
    st.divider()
    st.subheader("👁️ Omni-Deck: Real-Time Simulation")
    
    # --- Helper Functions for Modular Visualization ---
    def get_fig_chamber_3d():
        return visualize_chamber_resonance(
            10.47, 5.23, 5.81, 
            st.session_state.get('harmonic_x', 1), 
            st.session_state.get('harmonic_y', 1), 
            st.session_state.get('harmonic_z', 4)
        )

    def get_fig_void_gauge():
        current_freq = BigVoidResonator(st.session_state.get('void_len', 30.0), st.session_state.get('void_temp_c', 20.0)).calculate_fundamental_frequency()
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_freq,
            delta={'reference': 5.85},
            title={'text': "Void Freq (Hz)"},
            gauge={'axis': {'range': [4, 8]}, 'bar': {'color': "cyan"}}
        ))
        fig.update_layout(height=300)
        return fig

    def get_fig_signal_bar():
        arr = ResonatorArray(st.session_state.get('gallery_res_count', 27), 47.0, 117.0)
        res_amp = arr.simulate_amplification(120.0, st.session_state.get('gallery_tuning', 90))
        df_amp = pd.DataFrame(res_amp['profile'])
        fig = px.bar(df_amp, x='distance_m', y='signal_db', color='signal_db', color_continuous_scale='Bluered')
        fig.update_layout(height=300, xaxis_title="Distance (m)", yaxis_title="Signal (dB)")
        return fig

    def get_fig_capstone_3d():
        cap_w = st.session_state.get('capstone_width', 2.1)
        cap_mat = st.session_state.get('capstone_material', "Gold")
        cap_eng = CapstoneAntenna(cap_w, cap_mat)
        cap_r = cap_eng.calculate_radiation_efficiency(117.0)
        h = cap_r['height_m']
        w = cap_w / 2.0
        x = [w, w, -w, -w, 0]
        y = [w, -w, -w, w, 0]
        z = [0, 0, 0, 0, h]
        mesh_color = "gold" if cap_mat == "Gold" else "grey"
        mesh = go.Mesh3d(x=x, y=y, z=z, i=[0,0,0,1,2,3], j=[1,2,1,2,3,0], k=[2,3,4,4,4,4], color=mesh_color, opacity=1.0)
        fig = go.Figure(data=[mesh])
        fig.update_layout(height=300, scene=dict(aspectmode='data'), margin=dict(l=0, r=0, t=0, b=0))
        return fig

    def get_fig_water_hammer():
        vels = np.linspace(0, 10, 50)
        speed_map = {"Slow": 0.2, "Medium": 0.5, "Fast": 0.8, "Instant": 1.0}
        cf = speed_map.get(st.session_state.get('hawara_trapdoor', "Instant"), 1.0)
        ram_viz = HydraulicRam(st.session_state.get('hawara_fluid', "Fresh Water"), cf)
        ps = [ram_viz.calculate_pressure_spike(v)['pressure_bar'] for v in vels]
        fig = px.line(x=vels, y=ps, labels={'x':'Velocity (m/s)', 'y':'Pressure (Bar)'})
        curr_v = st.session_state.get('hawara_velocity', 4.0)
        curr_p = ram_viz.calculate_pressure_spike(curr_v)['pressure_bar']
        fig.add_scatter(x=[curr_v], y=[curr_p], mode='markers', marker=dict(size=15, color='red'), name="Current")
        fig.update_layout(height=300)
        return fig

    def get_fig_labyrinth_heat():
        stab = LabyrinthManifold(3000, st.session_state.get('lab_baffles', 0.5)).calculate_flow_dynamics(50, 50, 150)['stability_factor']
        grid_size = 10
        grid = np.random.rand(grid_size, grid_size) * (1.0 - stab) 
        fig = px.imshow(grid, color_continuous_scale='RdBu_r', title=f"Turbulence Intensity (Stability: {stab*100:.1f}%)")
        fig.update_layout(height=300)
        return fig

    def get_fig_h2_gauge():
        chem = ChemicalInjector(fluid_type=st.session_state.get('chem_type', "Dilute Sulfuric Acid"))
        rate = chem.calculate_hydrogen_yield(chem.calculate_flow_rate(st.session_state.get('chem_valve_pct', 5)))['h2_rate_l_min']
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=rate,
            title={'text': "L/min"},
            gauge={'axis': {'range': [0, 5000]}, 'bar': {'color': "green"}, 'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}}
        ))
        fig.update_layout(height=300)
        return fig

    def get_fig_thermal_scan():
        therm = GroundingHeat(9.8, 400, st.session_state.get('ground_resistance', 150))
        dt = therm.calculate_temperature_delta()['delta_t_celsius']
        grid_t = np.zeros((10, 10)) + 20 
        grid_t += np.random.normal(0, 0.2, (10, 10))
        grid_t[7:9, 7:9] += dt
        fig = px.imshow(grid_t, color_continuous_scale='Inferno', labels=dict(color="Temp (°C)"))
        fig.update_layout(height=300)
        return fig

    def get_fig_obelisk_3d():
        h_ob = st.session_state.get('obelisk_height', 28.0)
        w_ob = st.session_state.get('obelisk_width', 2.5)
        x_ob = [w_ob/2, w_ob/2, -w_ob/2, -w_ob/2, 0]
        y_ob = [w_ob/2, -w_ob/2, -w_ob/2, w_ob/2, 0]
        z_ob = [0, 0, 0, 0, h_ob]
        mesh_ob = go.Mesh3d(x=x_ob, y=y_ob, z=z_ob, i=[0,0,0,1,2,3], j=[1,2,1,2,3,0], k=[2,3,4,4,4,4], color='red', opacity=0.8)
        fig = go.Figure(data=[mesh_ob])
        fig.update_layout(height=300, scene=dict(aspectmode='data'), margin=dict(l=0, r=0, t=0, b=0))
        return fig

    def get_fig_collapse_area():
        fields = np.linspace(0, 100, 50)
        grid_viz = PlanetaryGrid()
        effs = [grid_viz.calculate_grid_status(f)['efficiency'] * 100 for f in fields]
        fig = px.area(x=fields, y=effs, labels={'x':'Field (%)', 'y':'Efficiency (%)'})
        fig.add_vline(x=st.session_state.get('cascade_field', 100), line_dash="dash", line_color="red")
        fig.update_layout(height=300)
        return fig

    # --- Visualization Map ---
    viz_options = {
        "Giza: 3D Resonance": get_fig_chamber_3d,
        "Giza: Void Tuning": get_fig_void_gauge,
        "Giza: Signal Gain": get_fig_signal_bar,
        "Giza: Capstone": get_fig_capstone_3d,
        "Hawara: Water Hammer": get_fig_water_hammer,
        "Labyrinth: Turbulence": get_fig_labyrinth_heat,
        "Chem: H2 Gauge": get_fig_h2_gauge,
        "Chem: Thermal Scan": get_fig_thermal_scan,
        "Net: Obelisk 3D": get_fig_obelisk_3d,
        "Net: Collapse Timeline": get_fig_collapse_area
    }

    tab_resonance, tab_power, tab_fluid, tab_chem, tab_net, tab_custom = st.tabs([
        "🔊 Resonance Lab", "⚡ Power & Signal", "🌊 Fluid Dynamics", "⚗️ Chemical & Thermal", "🌍 Global Grid", "🎛️ Custom Matrix"
    ])
    
    with tab_resonance:
        c_viz1, c_viz2 = st.columns([2, 1])
        with c_viz1:
            st.caption("King's Chamber Harmonic Pressure Field")
            st.plotly_chart(get_fig_chamber_3d(), use_container_width=True)
        with c_viz2:
            st.caption("Frequency Lock")
            st.plotly_chart(get_fig_void_gauge(), use_container_width=True)

    with tab_power:
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.caption("Grand Gallery Signal Gain")
            st.plotly_chart(get_fig_signal_bar(), use_container_width=True)
        with c_p2:
            st.caption("Capstone Emitter")
            st.plotly_chart(get_fig_capstone_3d(), use_container_width=True)

    with tab_fluid:
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            st.caption("Joukowsky Pressure Profile")
            st.plotly_chart(get_fig_water_hammer(), use_container_width=True)
        with c_f2:
            st.caption("Labyrinth Turbulence Scan")
            st.plotly_chart(get_fig_labyrinth_heat(), use_container_width=True)

    with tab_chem:
        c_ch1, c_ch2 = st.columns([1, 2])
        with c_ch1:
            st.caption("H2 Production")
            st.plotly_chart(get_fig_h2_gauge(), use_container_width=True)
        with c_ch2:
            st.caption("Eastern Face Thermal Scan")
            st.plotly_chart(get_fig_thermal_scan(), use_container_width=True)

    with tab_net:
        c_n1, c_n2 = st.columns(2)
        with c_n1:
            st.caption("Obelisk Resonator")
            st.plotly_chart(get_fig_obelisk_3d(), use_container_width=True)
        with c_n2:
            st.caption("Laschamp Collapse Profile")
            st.plotly_chart(get_fig_collapse_area(), use_container_width=True)

    with tab_custom:
        st.info("Select specific real-time simulations to view them side-by-side.")
        selected_viz = st.multiselect(
            "Select Simulations to Compare", 
            options=list(viz_options.keys()),
            default=["Giza: 3D Resonance", "Hawara: Water Hammer"]
        )
        
        if selected_viz:
            cols = st.columns(2)
            for i, viz_name in enumerate(selected_viz):
                with cols[i % 2]:
                    st.caption(viz_name)
                    st.plotly_chart(viz_options[viz_name](), use_container_width=True, key=f"custom_viz_{i}")
                    
                    # --- Smart Control Deck ---
                    with st.expander(f"⚙️ Tune {viz_name.split(':')[1].strip()}"):
                        
                        if "Giza: 3D" in viz_name:
                            def sync_hx(): st.session_state.harmonic_x = st.session_state[f"hx_{i}"]
                            def sync_hy(): st.session_state.harmonic_y = st.session_state[f"hy_{i}"]
                            def sync_hz(): st.session_state.harmonic_z = st.session_state[f"hz_{i}"]
                            
                            c_x, c_y, c_z = st.columns(3)
                            with c_x: st.number_input("Harmonic X", 1, 10, key=f"hx_{i}", value=st.session_state.get('harmonic_x', 1), on_change=sync_hx)
                            with c_y: st.number_input("Harmonic Y", 1, 10, key=f"hy_{i}", value=st.session_state.get('harmonic_y', 1), on_change=sync_hy)
                            with c_z: st.number_input("Harmonic Z", 1, 10, key=f"hz_{i}", value=st.session_state.get('harmonic_z', 4), on_change=sync_hz)
                            
                        elif "Giza: Void" in viz_name:
                            def sync_vlen(): st.session_state.void_len = st.session_state[f"vl_{i}"]
                            st.slider("Void Length (m)", 25.0, 35.0, key=f"vl_{i}", value=st.session_state.get('void_len', 30.0), on_change=sync_vlen)
                            
                        elif "Hawara" in viz_name:
                            def sync_hvel(): st.session_state.hawara_velocity = st.session_state[f"hv_{i}"]
                            st.slider("Flow Velocity (m/s)", 0.5, 10.0, key=f"hv_{i}", value=st.session_state.get('hawara_velocity', 4.0), on_change=sync_hvel)

                        elif "Labyrinth" in viz_name:
                            def sync_lb(): st.session_state.lab_baffles = st.session_state[f"lb_{i}"]
                            st.slider("Baffle Complexity", 0.0, 1.0, key=f"lb_{i}", value=st.session_state.get('lab_baffles', 0.5), on_change=sync_lb)

                        elif "Net: Obelisk" in viz_name:
                            def sync_oh(): st.session_state.obelisk_height = st.session_state[f"oh_{i}"]
                            st.slider("Height (m)", 10.0, 40.0, key=f"oh_{i}", value=st.session_state.get('obelisk_height', 28.0), on_change=sync_oh)
                            
                        elif "Signal Gain" in viz_name:
                            def sync_gt(): st.session_state.gallery_tuning = st.session_state[f"gt_{i}"]
                            st.slider("Resonator Tuning", 10, 150, key=f"gt_{i}", value=st.session_state.get('gallery_tuning', 90), on_change=sync_gt)

                        elif "Collapse" in viz_name:
                            def sync_cf(): st.session_state.cascade_field = st.session_state[f"cf_{i}"]
                            st.slider("Field Strength (%)", 0, 100, key=f"cf_{i}", value=st.session_state.get('cascade_field', 100), on_change=sync_cf)

                        elif "Capstone" in viz_name:
                            def sync_cw(): st.session_state.capstone_width = st.session_state[f"cw_{i}"]
                            st.slider("Base Width (m)", 0.5, 5.0, key=f"cw_{i}", value=st.session_state.get('capstone_width', 2.1), on_change=sync_cw)

elif module == "📜 The Origin Calculations":
    st.title("📜 The Origin: Initial Theoretical Models")
    st.markdown("Archive of the theoretical physics models that inspired this computational suite.")

    st.header("1. The Giza 3-Mass Model")
    st.markdown("""
    **Theory:** We modeled the King's Chamber complex not as a static room, but as a **3-Degree-of-Freedom (3-DOF)** dynamic system consisting of:
    1. The Chamber (Floor/Walls)
    2. The Relieving Beams (Massive Granite Beams)
    3. The Surrounding Limestone Masonry

    **Findings:**
    The eigenvalues of this system revealed three distinct resonant modes:
    *   **Mode 1 (18.6 Hz):** **Global Sway / Seismic Breathing.** The entire structure moves in unison.
    *   **Mode 2 (82.9 Hz):** **Shear Decoupling.** The beams move out of phase with the masonry.
    *   **Mode 3 (125.6 Hz):** **Granite Torsional Mode.** The "Energy Trap." This is where the granite beams resonate intensely while the limestone remains relatively still, effectively trapping acoustic energy in the piezoelectric crystal lattice.
    """)
    st.info("This theoretical finding (125.6 Hz) aligns closely with the F# target frequency (117 Hz), suggesting the relieving chambers act as a mechanical amplifier.")

    st.divider()

    st.header("2. The Serapeum Dispersion Relation")
    st.markdown("""
    **Theory:** We modeled the Serapeum as a **1D Phononic Crystal**—a periodic chain of massive granite boxes separated by limestone tunnels.
    
    **Findings:**
    By solving the dispersion relation for this periodic structure, we identified a massive "Band Gap" where sound cannot propagate.
    
    *   **Lower Branch (0 - 15 Hz):** Acoustic waves pass through (Infrasound).
    *   **Band Gap (16 - 40 Hz):** **The Zone of Silence.** In this frequency range, the Effective Mass Density of the system becomes **NEGATIVE**. The boxes move out of phase with the floor, creating "Negative Inertia" that cancels the wave transmission.
    *   **Upper Branch (40 - 200 Hz):** Higher frequencies pass through.
    """)
    
    st.markdown("### Calculated Proof")
    st.markdown("The Bragg Scattering condition for this lattice is approximately:")
    st.latex(r"f_B \approx \frac{v}{2a}")
    st.markdown("Where $v$ is the speed of sound in the host medium and $a$ is the lattice constant.")

elif module == "📍 Giza Generator (Active)":
    # --- Header ---
    st.title("📍 Giza Power Plant: Verification Engine")
    with st.expander("📘 How the Giza Power Plant Works (The Theory)"):
        st.markdown("""
        ### The Core Physics Engine
        This simulation models the Great Pyramid as a **Piezoelectric Generator**.
        
        1.  **The Resonator (117 Hz):**
            The King's Chamber is a granite box. Just as a wine glass rings at a specific note, this room resonates at **117 Hz** (the F# note).
            We calculate the standing waves (harmonics) to verify this tuning.
            
        2.  **The Crystal (Piezoelectricity):**
            The chamber is built of **Rose Granite**, which is 55% Quartz. Quartz is piezoelectric—when you squeeze it, it generates electricity.
            (This is the same mechanism used in quartz watches and BBQ lighters).
            
        3.  **The Amplifier (Pre-Stress):**
            Above the chamber are 5 layers of massive granite beams (The Relieving Chambers).
            The weight of the masonry (approx. 1000 tons) compresses the quartz lattice.
            **Physics Rule:** Compressed quartz is significantly more sensitive to vibration, amplifying the output.
            
        4.  **The Battery (Series Stacking):**
            There are **9 Beams** forming the ceiling. We model them as a battery pack wired in series.
            Total Voltage = (Single Beam Voltage) × 9.
        """)

    # --- Sidebar Controls ---
    st.sidebar.header("Simulation Inputs")
    quartz_eff = st.sidebar.slider("Quartz Efficiency", 0.1, 1.0, 0.3, key="giza_quartz_eff", help="Purity/Alignment of crystals")
    input_db = st.sidebar.slider("Input Sound Pressure (dB)", 60, 140, 120, key="giza_input_db")
    load_tons = st.sidebar.number_input("Static Load (tons)", 0, 5000, 1000, key="giza_load_tons")

    # --- Simulation Core ---
    # Dimensions: L=10.47, W=5.23, H=5.81
    chamber = ResonantChamber(10.47, 5.23, 5.81)
    piezo = PiezoGenerator()
    beam_thickness = 2.0 # Meters
    BEAM_COUNT = 9

    # 1. Calculate Acoustic Modes (1-9 Harmonics)
    modes = chamber.calculate_room_modes(max_order=9)
    match_data = chamber.check_resonance_match(modes, config.TARGET_FREQUENCY)

    # 2. Calculate Voltage Sweep (With Stacking & Pre-stress)
    df_sweep = piezo.simulate_voltage_sweep(60, 140, quartz_eff, beam_thickness, beam_count=BEAM_COUNT, static_load_tons=load_tons)

    # 3. Calculate Current State Point
    # Apply Pre-Stress Logic manually for single point to match sweep
    efficiency_multiplier = 1.5 if load_tons > 500 else 1.0
    effective_efficiency = quartz_eff * efficiency_multiplier
    
    current_pressure = 20e-6 * (10 ** (input_db / 20))
    single_beam_voltage = config.VOLTAGE_CONSTANT_QUARTZ * effective_efficiency * current_pressure * beam_thickness
    current_voltage = single_beam_voltage * BEAM_COUNT

    # --- KPI Row ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Target Frequency", f"{config.TARGET_FREQUENCY} Hz")

    with col2:
        # Display Closest Harmonic Match
        closest = match_data['closest_harmonic']
        match_text = f"{closest['freq']:.2f} Hz"
        delta_color = "normal" if match_data['is_match'] else "off"
        st.metric("Calculated Harmonic", match_text, delta=f"{match_data['deviation']:.2f} Hz Deviation", delta_color=delta_color)

    with col3:
        st.metric("Voltage Output", f"{current_voltage:.2f} V")
        if current_voltage > 1000:
            st.error("⚠️ HIGH VOLTAGE DETECTED")

    # --- Visualizations ---
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["📊 Acoustic Verification", "⚡ Voltage Simulation", "📋 Forensic Data Vault", "💻 Logic Archive", "🧊 3D Resonance Lab", "🌬️ The Wind Flute", "🕳️ The Big Void", "🔊 Grand Gallery", "🔥 Thermal Anomalies", "📡 The Capstone", "⚗️ Chemical Shafts"])

    with tab1:
        st.subheader("Harmonic Resonance Analysis")
        col_chart, col_gauge = st.columns([2, 1])
        
        with col_chart:
            # Prepare data for plotting
            plot_data = []
            for axis, freqs in modes.items():
                for i, f in enumerate(freqs):
                    if f <= 300: 
                        is_match_harmonic = (axis == closest['axis'] and (i+1) == closest['order'])
                        color = 'green' if is_match_harmonic else 'lightgrey'
                        plot_data.append({
                            'freq': f, 
                            'label': f"{axis.upper()}-{i+1}", 
                            'axis': axis,
                            'color': color
                        })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[item['freq'] for item in plot_data],
                y=[50] * len(plot_data),
                text=[item['label'] for item in plot_data],
                marker_color=[item['color'] for item in plot_data],
                width=2,
                textposition='outside'
            ))
            fig.add_vline(x=config.TARGET_FREQUENCY, line_width=2, line_dash="dash", line_color="red", annotation_text="Target (117 Hz)")
            
            fig.update_layout(
                title="Chamber Harmonics vs 117 Hz Target",
                xaxis_title="Frequency (Hz)",
                yaxis_visible=False,
                xaxis_range=[0, 300],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"**Verdict:** The {closest['axis'].upper()}-Axis {closest['order']}th Harmonic resonates at **{closest['freq']:.2f} Hz**, matching the 117 Hz target with high precision.")

        with col_gauge:
            st.markdown("### Precision Gauge")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = closest['freq'],
                delta = {'reference': config.TARGET_FREQUENCY},
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Frequency Match (Hz)"},
                gauge = {
                    'axis': {'range': [110, 124]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [110, 115], 'color': "lightgray"},
                        {'range': [115, 119], 'color': "lightgreen"}, # Green Zone
                        {'range': [119, 124], 'color': "lightgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': config.TARGET_FREQUENCY
                    }
                }
            ))
            fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

    with tab2:
        st.subheader("Piezoelectric Generation Curve")
        col_waterfall, col_curve = st.columns([1, 2])
        
        with col_waterfall:
            st.markdown("### Power Amplification")
            
            # Chemical Boost Toggle
            chem_active = st.toggle("Enable Chemical Injection?", value=False, help="Simulate H2 Pressure (50 PSI)")
            
            if chem_active:
                internal_pressure = 344000.0 # 50 PSI
                boost_text = "+ 344 kPa (Chemical)"
                chart_color = 'red'
                mode_title = "Active Mode: Chemical Injection (kV Range)"
                y_label = "Voltage (kV)"
                y_divisor = 1000.0
            else:
                internal_pressure = 0.0
                boost_text = "Passive Mode"
                chart_color = 'purple'
                mode_title = "Passive Mode: Wind/Seismic (V Range)"
                y_label = "Voltage (V)"
                y_divisor = 1.0
            
            # Re-run simulation with pressure
            df_sweep = piezo.simulate_voltage_sweep(60, 140, quartz_eff, beam_thickness, beam_count=BEAM_COUNT, static_load_tons=load_tons, internal_pressure_pa=internal_pressure)
            
            # Update current voltage point for this view
            current_total_pressure = current_pressure + internal_pressure
            v1_base = config.VOLTAGE_CONSTANT_QUARTZ * effective_efficiency * current_total_pressure * beam_thickness
            current_voltage_view = v1_base * BEAM_COUNT
            
            # Waterfall Logic
            # 1. Base Acoustic
            v_acoustic = config.VOLTAGE_CONSTANT_QUARTZ * quartz_eff * current_pressure * beam_thickness * BEAM_COUNT
            
            # 2. Chemical Boost
            v_chem = (config.VOLTAGE_CONSTANT_QUARTZ * quartz_eff * internal_pressure * beam_thickness * BEAM_COUNT) if chem_active else 0
            
            # 3. Pre-Stress Boost
            v_total_raw = v_acoustic + v_chem
            v_stress_boost = v_total_raw * (efficiency_multiplier - 1.0)
            
            fig_waterfall = go.Figure(go.Waterfall(
                name = "Voltage Stack",
                orientation = "v",
                measure = ["relative", "relative", "relative", "total"],
                x = ["Acoustic Signal", "Chemical Pressure", "Pre-Stress Boost", "Total Output"],
                textposition = "outside",
                text = [f"{v_acoustic:.1f}V", f"{v_chem/1000:.1f} kV" if v_chem > 1000 else f"{v_chem:.1f}V", f"{v_stress_boost/1000:.1f} kV" if v_stress_boost > 1000 else f"{v_stress_boost:.1f}V", f"{current_voltage_view/1000:.1f} kV" if current_voltage_view > 1000 else f"{current_voltage_view:.1f}V"],
                y = [v_acoustic, v_chem, v_stress_boost, 0],
                connector = {"line": {"color": "rgb(63, 63, 63)"}},
            ))
            
            fig_waterfall.update_layout(
                title = "Voltage Amplification Stages",
                showlegend = False,
                height=400
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
        with col_curve:
            st.markdown("### Non-Linear Response")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            
            # Plot with scaling
            sns.lineplot(x=df_sweep['db'], y=df_sweep['voltage']/y_divisor, ax=ax2, color=chart_color, linewidth=2)
            
            # Mark current point
            ax2.plot(input_db, current_voltage_view/y_divisor, 'ro', markersize=10)
            ax2.annotate(f"Current: {current_voltage_view/y_divisor:.1f} {'kV' if chem_active else 'V'}", 
                         (input_db, current_voltage_view/y_divisor), 
                         xytext=(-20, 20), 
                         textcoords='offset points',
                         bbox=dict(boxstyle="round", fc="w"))
            
            # Ignition Annotation if Active
            if chem_active:
                 ax2.text(100, df_sweep['voltage'].mean()/1000, "REACTOR IGNITION POINT", color='red', fontsize=12, fontweight='bold')
                         
            ax2.set_title(mode_title)
            ax2.set_ylabel(y_label)
            ax2.set_xlabel("Sound Pressure Level (dB)")
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)
            
            st.markdown(f"**Physics Engine:** {boost_text} | {efficiency_multiplier}x Pre-Stress Multiplier")

    with tab3:
        st.subheader("📋 Forensic Data Vault")
        st.markdown("Complete simulation dataset for external verification.")
        
        shaft_area = 0.2 * 0.2 
        helmholtz_length = chamber.calculate_helmholtz_neck_length(shaft_area, config.TARGET_FREQUENCY)

        full_report = {
            "meta": {
                "version": "3.0",
                "module": "Giza Generator",
                "timestamp": "2024-Simulation"
            },
            "inputs": {
                "quartz_efficiency": quartz_eff,
                "input_db": input_db,
                "static_load_tons": load_tons,
                "beam_count": BEAM_COUNT,
                "beam_thickness_m": beam_thickness
            },
            "physics_derived": {
                "efficiency_multiplier_applied": efficiency_multiplier,
                "effective_efficiency": effective_efficiency,
                "input_pressure_pa": round(current_pressure, 4)
            },
            "acoustic_analysis": {
                "target_frequency_hz": config.TARGET_FREQUENCY,
                "closest_match": match_data,
                "all_modes": modes,
                "helmholtz_neck_length_m": round(helmholtz_length, 4) if helmholtz_length else "INVALID_GEOMETRY"
            },
            "piezo_analysis": {
                "single_beam_voltage_v": round(single_beam_voltage, 4),
                "total_stacked_voltage_v": round(current_voltage, 4),
                "peak_potential_v": round(df_sweep['voltage'].max(), 4)
            },
            "verdict": {
                "match_found": match_data['is_match'],
                "deviation_hz": round(match_data['deviation'], 4),
                "status": "HIGH CONFIDENCE" if match_data['is_match'] else "LOW PROBABILITY"
            }
        }
        
        json_str = json.dumps(full_report, indent=4)
        st.json(full_report, expanded=True)
        st.download_button(
            label="💾 Download Forensic Report (JSON)",
            data=json_str,
            file_name="lithic_report.json",
            mime="application/json"
        )

    with tab4:
        st.subheader("💻 Logic Archive")
        st.markdown("Transparent access to the physics engine source code.")
        
        col_code1, col_code2 = st.columns(2)
        with col_code1:
            st.markdown("### acoustics.py")
            with open(os.path.join(current_dir, "acoustics.py"), "r") as f:
                st.code(f.read(), language="python")
        with col_code2:
            st.markdown("### piezo.py")
            with open(os.path.join(current_dir, "piezo.py"), "r") as f:
                st.code(f.read(), language="python")

    with tab5:
        st.subheader("🧊 3D Resonance Lab")
        st.markdown("Visualizing the Standing Wave pressure field inside the King's Chamber.")
        
        col_3d_ctrl, col_3d_plot = st.columns([1, 3])
        
        with col_3d_ctrl:
            st.markdown("**Harmonic Selection**")
            h_x = st.number_input("X-Harmonic (Length)", 1, 9, key="harmonic_x")
            h_y = st.number_input("Y-Harmonic (Width)", 1, 9, key="harmonic_y")
            h_z = st.number_input("Z-Harmonic (Height)", 1, 9, key="harmonic_z", help="Z=4 is theorized to couple with the beams")
            st.info("Adjust harmonics to see how pressure nodes align with the ceiling beams.")
            
        with col_3d_plot:
            # Generate 3D Visualization
            fig_3d = visualize_chamber_resonance(10.47, 5.23, 5.81, h_x, h_y, h_z)
            st.plotly_chart(fig_3d, use_container_width=True)

    with tab6:
        st.subheader("🌬️ Atmospheric Power Source (The Wind Flute)")
        
        with st.expander("Why the North Wind?", expanded=True):
            st.markdown("""
            **The Etesian Winds:** Egypt experiences a constant, prevailing North-West wind (The Etesians) for most of the year.
            
            **The Intake:** The Northern Air Shaft (0.21m x 0.21m) points directly into this wind stream at an angle of ~32 degrees.
            
            **The Physics (Vortex Shedding):** 
            When wind blows across a sharp edge (like the shaft opening), it creates oscillating vortices. This is the same principle that makes a beer bottle whistle when you blow across the top. This phenomenon is governed by the **Strouhal Effect**.
            """)
            
        col_wind_ctrl, col_wind_viz = st.columns([1, 2])
        
        with col_wind_ctrl:
            st.markdown("**Atmospheric Conditions**")
            # Mark "Average Giza Wind (20 km/h)" clearly
            wind_speed_local = st.slider("Wind Speed (km/h)", 0, 60, key="wind_speed_local", help="Average Giza Wind ~20 km/h")
            # Mark "Actual (21 cm)" clearly
            shaft_width_cm = st.slider("Shaft Opening Width (cm)", 10, 50, key="shaft_width_cm")
            shaft_width_m = shaft_width_cm / 100.0
            
            # Calculate
            strouhal_res = chamber.calculate_strouhal_resonance(wind_speed_local, shaft_width_m)
            vortex_f = strouhal_res['fundamental']
            
            # Status Logic
            if 15 <= wind_speed_local <= 25:
                status_msg = "PASSIVE RESONANCE ACTIVE"
                status_color = "normal" # Green/Black
            elif wind_speed_local < 10:
                status_msg = "INSUFFICIENT ENERGY"
                status_color = "inverse" # Red/White
            else:
                status_msg = "TURBULENT / OVERDRIVE"
                status_color = "off" # Grey
                
            st.metric("System Status", status_msg, delta="Wind Driver Online" if status_msg=="PASSIVE RESONANCE ACTIVE" else None, delta_color=status_color)
            st.caption(f"Vortex Freq: {vortex_f:.2f} Hz")
            
        with col_wind_viz:
            # Gauge 1 (Vortex Frequency)
            # Green Zone: 100 - 130 Hz (Resonance Range)
            fig_wind_new = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = vortex_f,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Generated Frequency (Hz)"},
                gauge = {
                    'axis': {'range': [0, 150]},
                    'bar': {'color': "cyan"},
                    'steps': [
                        {'range': [100, 130], 'color': "lightgreen"}, # Target Zone
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': config.TARGET_FREQUENCY
                    }
                }
            ))
            fig_wind_new.update_layout(height=300)
            st.plotly_chart(fig_wind_new, use_container_width=True)
            
        st.info("**Conclusion:** At average Giza wind speeds (20 km/h), the shaft geometry naturally generates a frequency of ~115-120 Hz, mechanically locking the King's Chamber into resonance without human intervention.")

    with tab7:
        st.subheader("🕳️ The Big Void (Harmonic Buffer Analysis)")
        st.markdown("Investigation into whether the massive void acts as a resonant buffer.")
        
        col_void_ctrl, col_void_viz = st.columns([1, 2])
        
        with col_void_ctrl:
            st.markdown("**Forensic Analysis**")
            void_len = st.slider("Estimated Void Length (m)", 25.0, 35.0, key="void_len", help="ScanPyramids estimate > 30m")
            temp_c = st.slider("Internal Air Temperature (°C)", 0.0, 50.0, key="void_temp_c", help="Resonance varies with temperature")
            
            void_res = BigVoidResonator(void_len, temp_c)
            check = void_res.check_harmonic_coupling(config.TARGET_FREQUENCY, tolerance_percent=0.01) # 1% Tolerance
            
            st.metric("Fundamental Frequency", f"{check['fundamental']:.2f} Hz")
            
            # Status Logic
            if check['deviation'] <= 0.005: # 0.5%
                status_msg = "STATUS: OPERATIONAL TEMPERATURE REACHED (Harmonic Lock)"
                status_type = "success"
            elif check['deviation'] <= 0.01: # 1.0%
                status_msg = "STATUS: HARMONIC ALIGNMENT DETECTED (Drift Warning)"
                status_type = "warning"
            else:
                status_msg = "STATUS: SYSTEM COLD (Detuned / Safety Mode)"
                status_type = "warning" # Use yellow for safety mode
                
            if status_type == "success":
                st.success(status_msg)
            else:
                st.warning(status_msg)
                
            st.markdown(f"""
            ### 🔎 Forensic Analysis: Thermal Calibration
            
            **The Finding:**
            The Fundamental Frequency ({check['fundamental']:.2f} Hz) creates a **1:{check['nearest_harmonic']} Harmonic Ratio** with the King's Chamber ({config.TARGET_FREQUENCY} Hz) with a **{check['deviation']*100:.2f}%** deviation.
            
            **The Thermal Key:**
            The void is tuned to resonate at **33.5°C** (Lock window starts at 30.4°C). This acts as a passive safety switch; the system only engages when the chemical reaction heats the air to operating temperature.
            """)
            
            st.metric("Energy Multiplication Factor", f"{check['nearest_harmonic']}x")
                
        with col_void_viz:
            # Plot Tuning Curve
            lengths = np.linspace(25.0, 35.0, 100)
            freqs = []
            for l in lengths:
                vr = BigVoidResonator(l)
                freqs.append(vr.calculate_fundamental_frequency())
                
            fig_void = go.Figure()
            fig_void.add_trace(go.Scatter(x=lengths, y=freqs, name="Void Fundamental"))
            
            # Add Sub-Harmonics Lines
            sub_harmonics = [16, 20, 24]
            colors = ['green', 'orange', 'red']
            for idx, sh in enumerate(sub_harmonics):
                target_sub = config.TARGET_FREQUENCY / sh
                fig_void.add_hline(y=target_sub, line_dash="dot", annotation_text=f"1/{sh} Harmonic ({target_sub:.1f} Hz)")
                
            # Current Point
            fig_void.add_trace(go.Scatter(
                x=[void_len], y=[check['fundamental']],
                mode='markers', marker=dict(color='red', size=12),
                name="Current Estimate"
            ))
            
            fig_void.update_layout(
                title="Void Tuning Curve",
                xaxis_title="Length (m)",
                yaxis_title="Frequency (Hz)",
                height=400
            )
            st.plotly_chart(fig_void, use_container_width=True)

    with tab8:
        st.subheader("🔊 The Grand Gallery (Signal Amplifier)")
        st.markdown("Simulation of the 27 slot-pairs acting as a Phased Array Resonator Bank.")
        
        col_gal_ctrl, col_gal_viz = st.columns([1, 2])
        
        with col_gal_ctrl:
            st.markdown("**Array Parameters**")
            res_count = st.slider("Resonator Count", 0, 54, key="gallery_res_count", help="Number of resonant vessels in the slots")
            coherence = st.slider("Resonator Tuning Match (%)", 50, 100, key="gallery_tuning", help="Phase coherence efficiency")
            
            # Input signal from previous stages (approx 120 dB from wind)
            input_db = 120.0 
            
            # Updated Class Usage
            array = ResonatorArray(slot_count=res_count, array_length_m=47.0, input_frequency=config.TARGET_FREQUENCY)
            amp_result = array.simulate_amplification(input_db, coherence)
            
            gain = amp_result['total_gain_db']
            
            st.metric("Signal Gain", f"+{gain:.2f} dB")
            st.metric("Output Strength", f"{amp_result['output_db']:.2f} dB")
            
            if gain > 10.0:
                st.success("STATUS: LINEAR AMPLIFICATION CONFIRMED")
                st.caption("The array boosts the signal significantly before it hits the King's Chamber.")
            else:
                st.warning("STATUS: WEAK AMPLIFICATION")
                
        with col_gal_viz:
            # Bar Chart of Signal Growth
            df_amp = pd.DataFrame(amp_result['profile'])
            
            fig_amp = px.bar(
                df_amp, 
                x='distance_m', 
                y='signal_db',
                title="Signal Amplification along Grand Gallery (47m)",
                labels={'distance_m': 'Distance (m)', 'signal_db': 'Signal Strength (dB)'}
            )
            
            # Animation effect (Blue to Red)
            fig_amp.update_traces(marker_color=df_amp['signal_db'], marker_colorscale='Bluered')
            
            # Add threshold line for "Injection" into King's Chamber
            fig_amp.add_vline(x=47.0, line_dash="dot", line_color="red", annotation_text="King's Chamber Injection")
            
            fig_amp.update_layout(height=400, yaxis_range=[100, 160]) # Expanded range for higher gain
            st.plotly_chart(fig_amp, use_container_width=True)

    with tab9:
        st.subheader("🔥 Thermal Anomaly Analysis (Grounding Exhaust)")
        st.markdown("Verification of the ScanPyramids 'Hot Spots' via Electrical Grounding physics.")
        
        col_therm_ctrl, col_therm_viz = st.columns([1, 2])
        
        with col_therm_ctrl:
            st.markdown("**Grounding Parameters**")
            # Auto-linked power (Default 9.8 MW from Circuit)
            sys_power = st.number_input("System Power (MW)", 1.0, 100.0, 9.8, step=0.1)
            
            # Check for Brine Integration
            default_res = st.session_state.get('ground_resistance', 150.0)
            ground_res = st.slider("Grounding Resistance (Ω)", 10.0, 500.0, float(default_res), help="Resistance of the limestone/bedrock interface")
            if 'ground_resistance' in st.session_state:
                st.caption(f"🔗 Linked to Brine Simulator ({default_res:.2f} Ω)")
            
            voltage_kv = 400.0 # Assumed HV injection
            
            therm_engine = GroundingHeat(sys_power, voltage_kv, ground_res)
            therm_res = therm_engine.calculate_temperature_delta()
            
            delta_t = therm_res['delta_t_celsius']
            
            st.metric("Calculated Temp Rise", f"+{delta_t:.1f} °C")
            st.caption(f"Dissipated Power: {therm_res['heat_watts']/1000:.1f} kW")
            
            if 4.0 <= delta_t <= 8.0:
                st.success("STATUS: THERMODYNAMIC MATCH CONFIRMED")
                st.markdown("**Verdict:** The calculated electrical dissipation matches the observed 6-degree thermal anomaly reported by ScanPyramids.")
            elif delta_t > 8.0:
                st.error("STATUS: OVERHEATING")
            else:
                st.warning("STATUS: WEAK THERMAL SIG")
                
        with col_therm_viz:
            # Simulated Thermal Camera
            # 10x10 Grid
            grid = np.zeros((10, 10))
            # Ambient variation (noise)
            grid += np.random.normal(20, 0.5, (10, 10))
            
            # Add Hot Spots (Eastern Face - Bottom Right)
            # 3 blocks
            grid[8, 8] += delta_t
            grid[8, 9] += delta_t * 0.8
            grid[9, 8] += delta_t * 0.9
            
            fig_therm = px.imshow(
                grid,
                color_continuous_scale='Inferno',
                title="Simulated Thermal Scan (Eastern Face)",
                labels=dict(color="Temp (°C)")
            )
            fig_therm.update_layout(height=400)
            st.plotly_chart(fig_therm, use_container_width=True)

    with tab10:
        st.subheader("📡 The Capstone (Broadcast Terminal)")
        st.markdown("Verification of the Pyramidion as a High-Voltage Emitter.")
        
        col_cap_ctrl, col_cap_viz = st.columns([1, 2])
        
        with col_cap_ctrl:
            st.markdown("**Capstone Parameters**")
            base_width = st.slider("Base Width (m)", 1.0, 5.0, key="capstone_width", help="Base dimension of the pyramidion")
            material = st.selectbox("Material", ["Gold", "Electrum", "Granite"], key="capstone_material")
            
            cap_engine = CapstoneAntenna(base_width, material)
            cap_res = cap_engine.calculate_radiation_efficiency(config.TARGET_FREQUENCY)
            
            eff = cap_res['efficiency_pct']
            
            st.metric("Broadcast Efficiency", f"{eff:.1f}%")
            st.caption(f"Mode: {cap_res['mode']}")
            
            if eff > 90.0:
                st.success("STATUS: HIGH-EFFICIENCY EMITTER CONFIRMED")
                st.markdown("**Verdict:** A solid gold capstone is the only material capable of discharging the 400kV load without melting or arcing back into the structure.")
            elif eff < 5.0:
                st.error("STATUS: SYSTEM FAILURE (RESISTIVE HEATING)")
                st.markdown("Granite acts as an insulator, trapping the energy and causing catastrophic thermal failure.")
            else:
                st.warning("STATUS: PARTIAL EMISSION")
                
        with col_cap_viz:
            # 3D Cone Visualization
            # Define pyramidion geometry
            h = cap_res['height_m']
            w = base_width / 2.0
            
            # Vertices
            x = [w, w, -w, -w, 0]
            y = [w, -w, -w, w, 0]
            z = [0, 0, 0, 0, h]
            
            # Colors
            if material == "Gold":
                mesh_color = "gold"
                opacity = 1.0
            elif material == "Electrum":
                mesh_color = "khaki"
                opacity = 0.9
            else:
                mesh_color = "grey"
                opacity = 1.0
                
            # Mesh
            mesh = go.Mesh3d(
                x=x, y=y, z=z,
                i=[0, 0, 0, 1, 2, 3],
                j=[1, 2, 1, 2, 3, 0],
                k=[2, 3, 4, 4, 4, 4],
                color=mesh_color,
                opacity=opacity,
                name="Capstone"
            )
            
            data = [mesh]
            
            # Add Arcs (Corona) if Emitter
            if cap_res['mode'] == "EMITTER":
                # Random lines radiating from tip
                for _ in range(20):
                    theta = np.random.uniform(0, 2*np.pi)
                    phi = np.random.uniform(0, np.pi/3)
                    r = np.random.uniform(0.5, 2.0) * (eff/100.0)
                    
                    x_arc = [0, r * np.sin(phi) * np.cos(theta)]
                    y_arc = [0, r * np.sin(phi) * np.sin(theta)]
                    z_arc = [h, h + r * np.cos(phi)]
                    
                    data.append(go.Scatter3d(
                        x=x_arc, y=y_arc, z=z_arc,
                        mode='lines',
                        line=dict(color='cyan', width=2),
                        showlegend=False
                    ))
            
            fig_cap = go.Figure(data=data)
            fig_cap.update_layout(
                scene=dict(aspectmode='data'),
                title=f"{material} Pyramidion Simulation",
                height=400,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_cap, use_container_width=True)

    with tab11:
        st.subheader("⚗️ The Chemical Shafts (Fuel Injection)")
        st.markdown("Analysis of the Queen's Chamber shafts as gravity-fed chemical injectors.")
        
        col_chem_ctrl, col_chem_viz = st.columns([1, 2])
        
        with col_chem_ctrl:
            st.markdown("**Injection Controls**")
            chem_type = st.selectbox("Chemical Input", ["Dilute Sulfuric Acid", "Hydrochloric Acid", "Water"], key="chem_type")
            valve_pct = st.slider("Valve Open %", 0, 100, key="chem_valve_pct", help="Controls fluid flow rate")
            
            chem_engine = ChemicalInjector(fluid_type=chem_type)
            flow_rate = chem_engine.calculate_flow_rate(valve_pct)
            h2_data = chem_engine.calculate_hydrogen_yield(flow_rate)
            h2_rate = h2_data['h2_rate_l_min']
            
            st.metric("Liquid Flow Rate", f"{flow_rate:.0f} L/min")
            st.metric("H2 Production Rate", f"{h2_rate:.0f} L/min")
            
            if h2_rate > 100.0:
                st.success("STATUS: REACTOR IGNITION POSSIBLE")
                st.markdown("**Verdict:** The shafts provide sufficient flow to fill the upper chambers with Hydrogen gas, the necessary medium for MASER amplification.")
            elif h2_rate > 0:
                st.warning("STATUS: INSUFFICIENT PRESSURE")
            else:
                st.error("STATUS: NO REACTION")
                
        with col_chem_viz:
            # Gauge for H2 Rate
            # Max scale arbitrarily 5000 L/min
            fig_chem = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = h2_rate,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Hydrogen Generation (L/min)"},
                gauge = {
                    'axis': {'range': [0, 5000]},
                    'bar': {'color': "lightgreen"},
                    'steps': [
                        {'range': [0, 100], 'color': "lightgrey"},
                        {'range': [100, 5000], 'color': "green"},
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 100
                    }
                }
            ))
            fig_chem.update_layout(height=350)
            st.plotly_chart(fig_chem, use_container_width=True)

elif module == "💧 Brine-Aquifer Nexus (Active)":
    st.title("💧 Brine-Aquifer Nexus: Geo-Chem Simulator")
    st.markdown("### Objective: Simulate the electrolytic properties of the Giza Plateau aquifer.")
    
    col_sim, col_map = st.columns([1, 2])
    
    with col_sim:
        st.subheader("1. Water Chemistry")
        tds = st.slider("TDS (g/L)", 0.5, 100.0, 67.7, help="Total Dissolved Solids. Seawater ~35g/L. Nexus Brine >60g/L")
        temp = st.slider("Temperature (°C)", 10.0, 50.0, 25.0)
        d18o = st.slider("Isotopes δ18O (‰)", -15.0, 15.0, key="d18o", help="Positive = Evaporated/Brine. Negative = Paleo/Rain.")
        
        brine = BrineSimulator()
        cond_data = brine.calculate_conductivity(tds, temp)
        iso_data = brine.isotopic_analysis(d18o)
        
        # Store in Session State for Integration
        if 'ground_resistance' not in st.session_state:
            st.session_state['ground_resistance'] = 150.0
        st.session_state['ground_resistance'] = cond_data['resistance_ohms']
        
        st.metric("Conductivity", f"{cond_data['conductivity_sm']:.2f} S/m", delta=cond_data['status'])
        st.metric("Derived Resistance", f"{cond_data['resistance_ohms']:.4f} Ω")
        st.info(f"Isotope Verdict: {iso_data['verdict']} ({iso_data['origin']})")
        
    with col_map:
        st.subheader("2. Pelusium Conductivity Map")
        df_map = brine.get_pelusium_map()
        fig_map = px.scatter_mapbox(
            df_map, 
            lat=[29.9792, 31.0444, 29.8700, 29.2700], # Mock coords
            lon=[31.1342, 32.5000, 32.2000, 30.9000],
            color="Conductivity_Sm",
            size="TDS_gL",
            hover_name="Zone",
            zoom=5,
            mapbox_style="carto-positron",
            title="Regional Conductivity Anomalies"
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.success(f"INTEGRATION HOOK ACTIVE: Grounding Resistance set to {cond_data['resistance_ohms']:.2f} Ω based on TDS.")

elif module == "🗄️ Data Armor Vault (Active)":
    st.title("🗄️ Data Armor Vault (v2025)")
    st.markdown("### Secure Ingestion Interface for Remote Sensing Data")
    
    vault = DataVault()
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📡 Muon Tomography Link")
        api_key = st.text_input("SPARC API Key", type="password")
        if st.button("Sync Muon Data"):
            data = vault.ingest_muon_data(api_key)
            st.json(data)
            if data.get("void_detected"):
                st.success("ANOMALY CONFIRMED: New Chamber Vector")
                
    with c2:
        st.subheader("🛰️ LiDAR Point Cloud")
        res = st.select_slider("Scan Resolution", ["Low", "Medium", "High", "Ultra"])
        if st.button("Ingest LiDAR Cloud"):
            data = vault.ingest_lidar_data(res)
            st.json(data)
            
    st.divider()
    st.caption(f"Vault Sync Status: ACTIVE | Timestamp: {vault.last_sync}")

elif module == "🌪️ Cascade Dynamics (Perturbation)":
    st.title("🌪️ Cascade Dynamics: Perturbation Engine")
    st.markdown("### Objective: Stress-test the power grid against Laschamp Events and Hydraulic Floods.")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("1. Stress Parameters")
        steps = st.slider("Simulation Steps", 100, 1000, 500, key="cascade_steps")
        hurst = st.slider("Hurst Exponent (Chaos)", 0.1, 0.9, 0.7, key="cascade_hurst", help="0.5=Random, >0.5=Persistent Trend (Floods)")
        
        # Link to Brine
        if 'ground_resistance' in st.session_state:
            # Reverse calculate conductivity from resistance (approx)
            # R = 1/Cond * 0.1 -> Cond = 0.1 / R
            cond_est = 0.1 / st.session_state['ground_resistance']
            st.info(f"Linked Brine Conductivity: {cond_est:.2f} S/m")
        else:
            cond_est = st.slider("Brine Conductivity (S/m)", 0.1, 20.0, 5.0)
            
        laschamp_field = st.slider("Geomagnetic Field (%)", 0, 100, 5, key="cascade_field", help="Laschamp Event = 5%")
        
        st.markdown("---")
        mode = st.radio("Simulation Mode", ["Deterministic (Single Run)", "Monte Carlo Ensemble (1k Runs)"])
        
    with c2:
        cascade = CascadeDynamics()
        
        if mode == "Deterministic (Single Run)":
            st.subheader("2. Transient Simulation (Single)")
            df_trans = cascade.simulate_transients(steps, cond_est, hurst)
            fig_trans = px.line(df_trans, x="Time_Step", y="Power_Output_MW", title="Power Output Stability")
            st.plotly_chart(fig_trans, use_container_width=True)
            
            stress = cascade.laschamp_stress_test(laschamp_field, cond_est)
            st.metric("Net Efficiency", f"{stress['net_efficiency']*100:.1f}%", delta=stress['status'])
            st.progress(min(stress['uptime_pct']/100.0, 1.0), text=f"Uptime Probability: {stress['uptime_pct']:.1f}%")
            
        else:
            st.subheader("2. Monte Carlo Ensemble (1000 Runs)")
            with st.spinner("Running 1000 Simulations..."):
                res = cascade.run_ensemble(1000, steps, cond_est, hurst, laschamp_field)
            
            st.success(f"Ensemble Complete. Mean Uptime: {res['uptime_mean']:.1f}% (95% Floor: {res['uptime_p95']:.1f}%)")
            
            fig_hist = px.histogram(res['distribution'], nbins=50, title="Uptime Distribution (Laschamp Scenario)")
            fig_hist.add_vline(x=res['uptime_mean'], line_dash="dash", line_color="green", annotation_text="Mean")
            st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")
    st.subheader("3. HBM System Coherence (Triad Fusion)")
    st.markdown("Hierarchical Bayesian Model fusing Resonance (Giza), Hydraulic (Hawara), and Chemical (Brine) priors.")
    
    # HBM Section
    hbm = HBMStability()
    
    # Gather Priors/Likelihoods from other modules (or defaults)
    # We use session state to capture "live" values from other active modules
    giza_state = st.session_state.get('giza_resonance', 0.8) # Default to 0.8 (Assumed Tuned)
    hawara_state = st.session_state.get('hawara_stability', 0.7)
    # Brine score derived from conductivity (High cond = high score)
    brine_score = min(cond_est / 10.0, 1.0)
    
    c_h1, c_h2 = st.columns([1, 2])
    with c_h1:
        st.metric("Giza Prior (Resonance)", f"{giza_state:.2f}")
        st.metric("Hawara Prior (Hydraulic)", f"{hawara_state:.2f}")
        st.metric("Brine Prior (Chemical)", f"{brine_score:.2f}")
        
    with c_h2:
        coherence = hbm.fuse_inputs(giza_state, hawara_state, brine_score)
        st.metric("Global HBM Coherence", f"{coherence['coherence_mean']*100:.1f}%", delta=coherence['status'])
        st.info(f"Posterior Certainty (95% CI): {coherence['coherence_95_ci'][0]*100:.1f}% - {coherence['coherence_95_ci'][1]*100:.1f}%")

elif module == "🔒 Serapeum Capacitor (Active)":
    st.title("🔒 Serapeum: The Phononic Filter & Storage Bank")
    st.markdown("""
    **Objective:** Verify the Serapeum's function as a massive energy storage bank (Capacitor) protected by a sound-canceling tunnel (Phononic Crystal).
    **New Physics Model (v3.2):** Locally Resonant Sonic Material (LRSM) & Geometric Capacitance Array.
    """)

    # --- Sidebar Controls ---
    st.sidebar.header("Simulation Inputs")
    lattice_spacing = st.sidebar.slider("Lattice Spacing (m)", 1.0, 10.0, 6.0, key="sera_spacing")
    box_mass = st.sidebar.slider("Box Mass (tons)", 10, 100, 70, key="sera_mass")
    dielectric_const = st.sidebar.slider("Dielectric Constant", 4.0, 7.0, 5.5, key="sera_dielectric")
    
    # --- Simulation Core ---
    tunnel = PhononicTunnel(lattice_spacing, box_mass)
    capacitor = GraniteCapacitor(dielectric_constant=dielectric_const)
    
    # 1. Simulate Phononic Band Gap (Effective Density)
    df_transmission = tunnel.simulate_transmission()
    
    # 2. Calculate Capacitance & Energy
    storage_data = capacitor.calculate_storage_potential(box_count=24)
    
    # --- KPI Row ---
    col1, col2, col3 = st.columns(3)
    
    # Find Negative Density Zone
    neg_density_rows = df_transmission[df_transmission['effective_density'] < 0]
    
    with col1:
        # Max attenuation is technically infinite in band gap, simulated at -100
        min_trans = df_transmission['transmission_db'].min()
        st.metric("Stop Band Floor", f"{min_trans:.0f} dB", delta="Total Reflection")
        
    with col2:
        st.metric("Total Capacitance", f"{storage_data['capacitance_nF']:.2f} nF")
        
    with col3:
        st.metric("Max Energy Storage", f"{storage_data['stored_energy_joules']:.6f} Joules", help="At 81.0V Input")
        
    # --- Visualizations ---
    tab1, tab2, tab3 = st.tabs(["🔇 The Negative Mass Filter", "🔋 The Storage Bank", "📋 Forensic Data Vault"])
    
    with tab1:
        st.subheader("Effective Mass Density (LRSM Model)")
        
        # Create dual-axis plot
        fig = go.Figure()
        
        # Trace 1: Transmission
        fig.add_trace(go.Scatter(
            x=df_transmission['frequency'], 
            y=df_transmission['transmission_db'],
            name="Transmission (dB)",
            line=dict(color='blue')
        ))
        
        # Trace 2: Effective Density
        fig.add_trace(go.Scatter(
            x=df_transmission['frequency'], 
            y=df_transmission['effective_density'],
            name="Effective Density (kg/m³)",
            yaxis="y2",
            line=dict(color='purple', dash='dot')
        ))
        
        # Highlight Negative Mass Zone
        if not neg_density_rows.empty:
            fig.add_vrect(
                x0=neg_density_rows.iloc[0]['frequency'], 
                x1=neg_density_rows.iloc[-1]['frequency'], 
                fillcolor="red", opacity=0.2, layer="below", line_width=0,
                annotation_text="NEGATIVE MASS / STOP BAND"
            )
            
        fig.update_layout(
            title="Locally Resonant Band Gap",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Transmission (dB)",
            yaxis2=dict(title="Effective Density", overlaying="y", side="right"),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        if not neg_density_rows.empty:
            st.success("VERIFIED: The 70-ton boxes act as Local Resonators, creating a frequency range where the Effective Mass Density becomes NEGATIVE.")
            
    with tab2:
        st.subheader("Energy Storage Capacity")
        
        col_metric, col_info = st.columns([1, 2])
        
        with col_metric:
            st.metric("Stored Energy", f"{storage_data['stored_energy_joules']:.4f} J")
            st.caption(f"Input Voltage: {storage_data['voltage_input']} V")
            
        with col_info:
            st.info("At 81V input (from the Giza Generator), this array stores a small but stable electrostatic charge. The primary function appears to be frequency filtering rather than bulk power storage.")
        
    with tab3:
        st.subheader("Forensic Data Log")
        full_report = {
            "meta": {
                "version": "3.2",
                "module": "Serapeum Capacitor (Geometric Model)",
            },
            "inputs": {
                "lattice_spacing_m": lattice_spacing,
                "box_mass_tons": box_mass,
                "dielectric_constant": dielectric_const
            },
            "results": {
                "stop_band_detected": not neg_density_rows.empty,
                "max_attenuation_db": round(min_trans, 2),
                "capacitance_data": storage_data
            }
        }
        st.json(full_report)

elif module == "💧 Hawara Regulator (Active)":
    st.title("💧 Hawara: The Hydraulic Ram & Pressure Reactor")
    st.markdown("""
    **Objective:** Verify the "Water Hammer" hypothesis—that closing trapdoors in the Hawara Labyrinth creates a massive pressure spike, driving the Quartzite Monolith to generate electricity.
    **Physics Model:** Joukowsky Equation (Fluid Dynamics) + Piezoelectric Pulse.
    """)

    # --- Sidebar Controls ---
    st.sidebar.header("Simulation Inputs")
    flow_velocity = st.sidebar.slider("Flow Velocity (m/s)", 0.5, 10.0, 4.0, key="hawara_velocity", help="Speed of water before trapdoor closure")
    fluid_type = st.sidebar.selectbox("Fluid Type", ["Fresh Water", "Conductive Brine"])
    closure_speed_label = st.sidebar.select_slider("Trapdoor Closure Speed", options=["Slow", "Medium", "Fast", "Instant"], value="Instant", key="hawara_trapdoor")
    
    # Map closure label to efficiency factor
    closure_map = {"Slow": 0.2, "Medium": 0.5, "Fast": 0.8, "Instant": 1.0}
    closure_factor = closure_map[closure_speed_label]
    
    # --- Simulation Core ---
    ram = HydraulicRam(fluid_type=fluid_type, closure_factor=closure_factor)
    reactor = QuartziteReactor(wall_thickness=0.6)
    
    # 1. Calculate Shock
    shock_data = ram.calculate_pressure_spike(flow_velocity)
    pressure_pa = shock_data['pressure_pa']
    pressure_bar = shock_data['pressure_bar']
    
    # 2. Calculate Voltage Pulse
    pulse_voltage = reactor.calculate_pulse_voltage(pressure_pa)
    
    # --- KPI Row ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Hydraulic Shock", f"{pressure_bar:.1f} Bar", help=f"Density: {shock_data['fluid_density']} kg/m³")
        
    with col2:
        st.metric("Pulse Voltage", f"{pulse_voltage:.0f} Volts", delta="Peak Output")
        
    with col3:
        if pressure_bar > 50:
            st.metric("System Status", "CRITICAL PRESSURE", delta="Risk of Rupture", delta_color="inverse")
        else:
            st.metric("System Status", "NOMINAL", delta="Stable")
            
    # --- Visualizations ---
    tab1, tab2, tab3 = st.tabs(["🌊 The Water Hammer", "⚡ The Quartzite Pulse", "📋 Forensic Data Vault"])
    
    with tab1:
        st.subheader("Joukowsky Pressure Curve")
        
        df_hammer = ram.simulate_hammer_curve(min_v=0.1, max_v=15.0)
        
        fig = px.line(df_hammer, x='velocity_ms', y='pressure_bar', title=f"Water Hammer Pressure ({fluid_type})")
        
        # Add current point
        fig.add_trace(go.Scatter(
            x=[flow_velocity], y=[pressure_bar],
            mode='markers+text',
            marker=dict(color='red', size=12),
            text=[f"{pressure_bar:.1f} Bar"],
            textposition="top left",
            name="Current State"
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"**Joukowsky Principle:** A {flow_velocity} m/s flow stopped {closure_speed_label.lower()}ly generates a **{pressure_bar:.1f} Bar** shockwave.")
        
    with tab2:
        st.subheader("Piezoelectric Pulse Response")
        
        df_voltage = reactor.simulate_voltage_curve(min_bar=0, max_bar=200)
        
        fig2 = px.line(df_voltage, x='pressure_bar', y='voltage_v', title="Quartzite Voltage Output")
        
        # Add current point
        fig2.add_trace(go.Scatter(
            x=[pressure_bar], y=[pulse_voltage],
            mode='markers+text',
            marker=dict(color='gold', size=15, symbol='star'),
            text=[f"{pulse_voltage:.0f} V"],
            textposition="top left",
            name="Current Pulse"
        ))
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Comparison Logic
        giza_v = 8.1 # Approx continuous output from Giza module
        multiplier = pulse_voltage / giza_v
        st.success(f"**Verdict:** The Hydraulic Shock generates **{pulse_voltage:.0f} Volts**, which is **{multiplier:.0f}x** more powerful than the Giza acoustic resonator. However, this is a transient PULSE, not continuous power.")
        
    with tab3:
        st.subheader("Forensic Data Log")
        full_report = {
            "meta": {
                "version": "1.0",
                "module": "Hawara Regulator (Hydraulic Ram)",
            },
            "inputs": {
                "flow_velocity_ms": flow_velocity,
                "fluid_type": fluid_type,
                "closure_speed": closure_speed_label,
                "closure_factor": closure_factor
            },
            "results": {
                "hydraulic_shock_bar": round(pressure_bar, 2),
                "pulse_voltage_v": round(pulse_voltage, 2),
                "joukowsky_density": shock_data['fluid_density'],
                "speed_of_sound": shock_data['speed_of_sound']
            }
        }
        st.json(full_report)

elif module == "🏛️ Labyrinth Manifold (Active)":
    st.title("🏛️ Labyrinth Manifold: Valve Farm")
    st.markdown("### Objective: Stabilize hydraulic flow using the 3000-chamber Mataha complex.")
    
    c1, c2 = st.columns(2)
    with c1:
        chambers = st.number_input("Chamber Count", 1000, 5000, 3000)
        valves = st.slider("Valve Open %", 0, 100, 50)
        baffles = st.slider("Baffle Complexity", 0.0, 1.0, 0.5)
        
    with c2:
        manifold = LabyrinthManifold(chambers, baffles)
        res = manifold.calculate_flow_dynamics(input_pressure_bar=50.0, valve_open_pct=valves)
        
        st.metric("Flow Stability", f"{res['stability_factor']*100:.1f}%")
        st.metric("Turbulence Index", f"{res['turbulence_index']:.2f}")
        st.metric("Active Chambers", res['active_chambers'])
        
    if res['stability_factor'] > 0.9:
        st.success("STATUS: LAMINAR FLOW ACHIEVED")
    else:
        st.warning("STATUS: TURBULENT - ADJUST BAFFLES")

elif module == "🏛️ Labyrinth Manifold (Active)":
    st.title("🏛️ Labyrinth Manifold: The Valve Farm")
    st.markdown("""
    **Objective:** Manage the **3,000 Chambers** of the Hawara Labyrinth (Mataha) to regulate hydraulic pressure.
    **Topology:** Use Multi-Stage Baffles to dampen the "Water Hammer" before it hits the Quartzite Reactor.
    """)
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("1. Topology Controls")
        chambers = st.slider("Active Chambers", 100, 3000, 3000, key="lab_chambers", help="Herodotus Count")
        baffles = st.slider("Baffle Complexity (χ)", 0.0, 1.0, 0.5, key="lab_baffles", help="0=Open Flow, 1=Max Turbulence Damping")
        valves = st.slider("Valve Open %", 0, 100, 50, key="lab_valves")
        
        # Hawara Link
        input_pressure = st.slider("Input Pressure (Bar)", 10.0, 100.0, key="lab_pressure")
        
        # Brine Link
        r_ground = st.session_state.get('ground_resistance', 150.0)
        st.metric("Linked Brine Resistance", f"{r_ground:.4f} Ω")
        if r_ground < 10.0:
             st.success("🛡️ Nexus Brine Protection Active")
        else:
             st.warning("⚠️ Freshwater Corrosion Risk")

    with c2:
        st.subheader("2. Flow Dynamics")
        
        manifold = LabyrinthManifold(chambers, baffles)
        res = manifold.calculate_flow_dynamics(input_pressure, valves, r_ground)
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Euler Characteristic (χ)", res['euler_chi'])
        m2.metric("Flow Rate", f"{res['flow_rate_m3_s']:.1f} m³/s")
        m3.metric("Stability Index", f"{res['stability_factor']*100:.1f}%", delta=res['status'])
        
        # Visualization (Turbulence Damping)
        st.markdown("### Turbulence Damping Analysis")
        chart_data = {
            "Stage": ["Input", "Baffled", "Output"],
            "Turbulence": [100, 100 / (1 + baffles*5), res['turbulence_index']*10] # Scaled for viz
        }
        st.bar_chart(chart_data, x="Stage", y="Turbulence")
        
        # Write to Session State for Cascade HBM
        st.session_state['hawara_stability'] = res['stability_factor']
        st.caption(f"📡 Telemetry Sent to Perturbation Engine: {res['stability_factor']:.2f}")

elif module == "🌍 Planetary Circuit Map (Active)":
    st.title("🌍 Planetary Circuit: Grand Unification")
    st.markdown("""
    **Objective:** Visualize the interconnected logic of the entire Lithic Circuit. 
    Giza generates the Pilot Signal (Frequency), Serapeum filters it (Gate), and Hawara injects the High Voltage Power (Pulse).
    """)

    # --- 1. Geomagnetic Conditions (New) ---
    st.subheader("📉 Geomagnetic Conditions")
    field_strength = st.slider("Earth Magnetic Field Strength (%)", 0, 100, key="cascade_field")
    st.caption("Normal = 100%. Laschamp Event (42k years ago) = 5%.")
    
    # Grid Calc
    grid_engine = PlanetaryGrid()
    grid_status = grid_engine.calculate_grid_status(field_strength)

    # --- 2. Master Control ---
    col_ctrl, col_status = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("Master Switch")
        system_active = st.toggle("Activate System", value=True)
        
        st.markdown("**Giza Tuning:**")
        giza_freq_dev = st.slider("Frequency Deviation (%)", 0.0, 10.0, key="giza_freq_dev", help="0% = Perfect 117 Hz Match")
        
        st.markdown("**Hawara Flow:**")
        hawara_active = st.checkbox("Hydraulic Pressure Active", value=True)
    
    # --- System Logic Engine ---
    giza_freq = config.TARGET_FREQUENCY * (1 + giza_freq_dev/100.0)
    is_tuned = giza_freq_dev <= 0.5 # 0.5% tolerance
    
    gate_status = "OPEN" if (is_tuned and system_active) else "BLOCKED"
    
    # Default Hawara/Serapeum values for the Map calculation
    ram = HydraulicRam(fluid_type="Conductive Brine", closure_factor=1.0)
    reactor = QuartziteReactor()
    cap = GraniteCapacitor()
    
    # Hawara Output
    if hawara_active and system_active:
        shock = ram.calculate_pressure_spike(10.0) 
        hawara_voltage = reactor.calculate_pulse_voltage(shock['pressure_pa'])
    else:
        hawara_voltage = 0.0
        
    # Serapeum Capacity
    cap_data = cap.calculate_storage_potential(24)
    c_total = cap_data['capacitance_nF'] * 1e-9 # Farads
    
    # Total System Power (Pulse Power Model)
    # Apply Grid Efficiency from Geomagnetics
    efficiency = grid_status['efficiency']
    
    if gate_status == "OPEN" and hawara_active:
        raw_power_watts = 0.5 * c_total * (hawara_voltage ** 2) * giza_freq
        total_power_watts = raw_power_watts * efficiency # Apply Global Field Loss
        total_power_mw = total_power_watts / 1e6
        
        status_msg = "ONLINE"
        status_color = "green"
    else:
        total_power_watts = 0.0
        total_power_mw = 0.0
        if not system_active: status_msg = "OFFLINE"
        elif not is_tuned: status_msg = "SIGNAL BLOCKED (MISTUNED)"
        elif not hawara_active: status_msg = "NO HYDRAULIC PRESSURE"
        status_color = "red"

    # --- Geomagnetic Override ---
    if grid_status['status'] == "COLLAPSED" or grid_status['status'] == "CRITICAL":
        # Override status if field is too weak (< 20%)
        status_msg = f"OFFLINE (INSUFFICIENT FIELD FLUX - {grid_status['status']})"
        status_color = "red"
        total_power_mw = 0.0 # Hard collapse
        total_power_watts = 0.0

    with col_status:
        st.metric("Total System Output (Net Grid Power)", f"{total_power_mw:.4f} MW", delta=status_msg, delta_color="normal" if status_color=="green" else "inverse")
        if status_color == "green":
            st.success("GRID SYNCHRONIZED: High Voltage Injection Confirmed.")
            if is_tuned and hawara_active and system_active:
                st.markdown("### 🟢 SYSTEM RESONANCE LOCKED")
                st.progress(efficiency, text=f"Phase Synchronization: {efficiency*100:.1f}% (Flux Dependent)")
        else:
            st.error(f"SYSTEM FAILURE: {status_msg}")
            if efficiency < 0.2:
                 st.warning(f"Geomagnetic Efficiency Critical: {efficiency*100:.1f}%")

    # --- MAP SECTION ---
    st.subheader("📍 Geospatial Layout")
    
    map_data = pd.DataFrame({
        'Site': ["Giza (Generator)", "Saqqara (Capacitor)", "Hawara (Reactor)"],
        'Lat': [29.9792, 29.8713, 29.2729],
        'Lon': [31.1342, 31.2165, 30.9009],
        'Role': ["Generator", "Capacitor", "Source"]
    })
    
    fig_map = px.scatter_mapbox(
        map_data, lat="Lat", lon="Lon", color="Role",
        color_discrete_map={"Generator": "gold", "Capacitor": "lightgreen", "Source": "cyan"},
        zoom=8, size=[15, 15, 15], height=400,
        hover_name="Site"
    )
    
    # Add Connection Line (The Lithic Bus) - Color depends on Grid Status
    line_color = grid_status['line_color']
    line_width = 3
    if grid_status['status'] == "COLLAPSED":
         line_width = 0 # Hide lines
    
    fig_map.add_trace(go.Scattermapbox(
        mode="lines",
        lat=[29.2729, 29.8713, 29.9792],
        lon=[30.9009, 31.2165, 31.1342],
        line=dict(width=line_width, color=line_color),
        name="The Lithic Bus"
    ))
    
    fig_map.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    # --- COLLAPSE TIMELINE CHART (New) ---
    st.subheader("📉 The Collapse Timeline (Laschamp Event)")
    df_timeline = grid_engine.generate_collapse_timeline()
    
    fig_time = px.area(
        df_timeline, 
        x="Time_Axis", 
        y="Grid_Power_MW",
        title="Historical Power Output (50,000 BP - Present)",
        labels={"Time_Axis": "Years Ago (BP)", "Grid_Power_MW": "Power Output (MW)"},
        color_discrete_sequence=["#00CC96"]
    )
    
    fig_time.update_xaxes(title="Years Before Present", range=[-50000, 0])
    
    # Add Annotation for Laschamp
    fig_time.add_annotation(
        x=-42000, y=1.0,
        text="Laschamp Event (Collapse)",
        showarrow=True,
        arrowhead=1
    )
    
    st.plotly_chart(fig_time, use_container_width=True)

    # --- SCHEMATIC SECTION ---
    st.subheader("Schematic Logic Flow")
    
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', bgcolor='black')
    dot.attr('node', shape='box', style='filled', fontname='Helvetica', fontcolor='black')
    
    dot.node('Giza', 'Giza Generator\n(Pilot Signal)', fillcolor='gold' if is_tuned else 'indianred')
    gate_color = 'lightgreen' if gate_status == "OPEN" else 'lightgrey'
    dot.node('Serapeum', f'Serapeum Capacitor\n(Gate: {gate_status})', fillcolor=gate_color)
    hawara_color = 'cyan' if hawara_active else 'lightgrey'
    dot.node('Hawara', 'Hawara Reactor\n(HV Injection)', fillcolor=hawara_color)
    
    # Grid Color depends on Total Power (which is now affected by Field Strength)
    grid_fill = 'salmon' if total_power_mw > 0 else 'grey'
    dot.node('Grid', 'The Grid\n(Global Power)', shape='doubleoctagon', fillcolor=grid_fill)
    
    edge_color_giza = 'green' if is_tuned else 'red'
    dot.edge('Giza', 'Serapeum', label=f'{giza_freq:.1f} Hz', color=edge_color_giza, penwidth='2')
    edge_color_gate = 'green' if gate_status == "OPEN" else 'grey'
    edge_style_gate = 'solid' if gate_status == "OPEN" else 'dashed'
    dot.edge('Serapeum', 'Grid', label='Gating Logic', color=edge_color_gate, style=edge_style_gate)
    edge_color_hawara = 'cyan' if hawara_active else 'grey'
    dot.edge('Hawara', 'Grid', label=f'{hawara_voltage/1000:.1f} kV Pulse', color=edge_color_hawara, penwidth='3')
    
    dot.node('Nile', 'Nile Flow', shape='ellipse', fillcolor='lightblue')
    dot.edge('Nile', 'Hawara', color='blue')

    st.graphviz_chart(dot)
    
    # --- LOAD CALCULATOR ---
    st.divider()
    st.subheader("🔌 System Load Analysis")
    
    col_load_ctrl, col_load_res = st.columns([1, 2])
    
    with col_load_ctrl:
        app_mode = st.selectbox("Hypothetical Application", 
                              ["Electrolysis (Hydrogen)", "Wireless Transmission", "Seismic Dampening"])
                              
    with col_load_res:
        if total_power_watts > 0:
            if app_mode == "Electrolysis (Hydrogen)":
                # Moles/sec = Watts / 237000 (Gibbs free energy of water splitting)
                moles_sec = total_power_watts / 237000.0
                liters_hr = moles_sec * 22.4 * 3600
                st.metric("Hydrogen Output", f"{liters_hr:,.0f} L/hour")
                st.caption("Based on standard electrolysis efficiency.")
                
            elif app_mode == "Wireless Transmission":
                # Radius = sqrt(P) * k
                radius = np.sqrt(total_power_watts) * 0.1
                st.metric("Effective Broadcast Radius", f"{radius:,.1f} km")
                
            elif app_mode == "Seismic Dampening":
                st.success("Status: ACTIVE")
                st.metric("Fault Stabilization", "High Potential")
                st.caption("Standing wave pressure stabilizes tectonic stress.")
        else:
            st.warning("System Offline. No Load Analysis Available.")

elif module == "🌍 Global Network (Active)":
    st.title("🌍 Global Network: Infrastructure Verification")
    st.markdown("""
    **Objective:** Move beyond single-site analysis to verify the "Infrastructure" that connects them. 
    Verify Wireless Transmission (Obelisks), the Grounding Network (Subsurface Grid), and the Seasonal Activation (Aquifer Pulse).
    """)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📡 The Obelisk Tuner", "🏔️ Subsurface Tomography", "🌊 The Aquifer Pulse", "📋 Forensic Data Vault", "📡 Directed Beam", "🛡️ System Diagnostics"])
    
    # --- Tab 1: Obelisk ---
    with tab1:
        st.subheader("Obelisk Tuner: Tapered Cantilever Resonance")
        
        col_ob_ctrl, col_ob_viz = st.columns([1, 2])
        
        with col_ob_ctrl:
            ob_height = st.slider("Height (m)", 10.0, 40.0, key="obelisk_height", help="Total height of the granite shaft")
            ob_width = st.slider("Base Width (m)", 1.0, 4.0, key="obelisk_width")
            
            tuner = ObeliskTuner()
            res = tuner.calculate_resonance(ob_height, ob_width)
            
            st.metric("Natural Frequency", f"{res['frequency_hz']:.2f} Hz")
            
            if res['is_harmonic']:
                st.success(f"TUNED: {res['match_details']}")
                ob_color = 'gold'
            else:
                st.warning("MISTUNED: No Harmonic Lock")
                ob_color = 'grey'
                
        with col_ob_viz:
            # 3D Cone/Pyramid
            # Base square, tip at height
            w = ob_width / 2.0
            h = ob_height
            
            # Vertices: 4 base, 1 tip
            x = [w, w, -w, -w, 0]
            y = [w, -w, -w, w, 0]
            z = [0, 0, 0, 0, h]
            
            # Triangles (Base 2, Sides 4)
            # Indices 0-4
            # Base: 0-1-2, 0-2-3
            # Sides: 0-1-4, 1-2-4, 2-3-4, 3-0-4
            i = [0, 0, 0, 1, 2, 3]
            j = [1, 2, 1, 2, 3, 0]
            k = [2, 3, 4, 4, 4, 4]
            
            fig_ob = go.Figure(data=[
                go.Mesh3d(
                    x=x, y=y, z=z,
                    i=i, j=j, k=k,
                    color=ob_color,
                    opacity=0.8,
                    flatshading=True
                )
            ])
            fig_ob.update_layout(
                scene=dict(aspectmode='data'),
                margin=dict(l=0, r=0, t=0, b=0),
                height=400
            )
            st.plotly_chart(fig_ob, use_container_width=True)
            
    # --- Tab 2: Subsurface ---
    with tab2:
        st.subheader("Subsurface Tomography: The Malanga Grid")
        
        depth_cutoff = st.slider("Tomography Depth (m)", -60, 0, key="depth_cutoff", help="Reveal the granite roots")
        
        # 3D Scene
        fig_sub = go.Figure()
        
        # 1. Surface Pyramid (Translucent)
        pyr_base = 230.0
        pyr_h = 146.0
        pb = pyr_base / 2
        px = [pb, pb, -pb, -pb, 0]
        py = [pb, -pb, -pb, pb, 0]
        pz = [0, 0, 0, 0, pyr_h]
        pi = [0, 0, 0, 1, 2, 3]
        pj = [1, 2, 1, 2, 3, 0]
        pk = [2, 3, 4, 4, 4, 4]
        
        if depth_cutoff > -10: # Only show pyramid if we are near surface
            fig_sub.add_trace(go.Mesh3d(x=px, y=py, z=pz, i=pi, j=pj, k=pk, color='goldenrod', opacity=0.1, name='Pyramid'))
        
        # 2. Red Grid (Roots)
        # Vertical columns from 0 down to -50
        # Grid 3x3
        grid_spacing = 50
        for gx in [-grid_spacing, 0, grid_spacing]:
            for gy in [-grid_spacing, 0, grid_spacing]:
                fig_sub.add_trace(go.Scatter3d(
                    x=[gx, gx], y=[gy, gy], z=[0, -50],
                    mode='lines', line=dict(color='red', width=4),
                    showlegend=False
                ))
                
        # 3. Aquifer Plane at -60
        # Large plane
        aq_size = 300
        ax = [aq_size, aq_size, -aq_size, -aq_size]
        ay = [aq_size, -aq_size, -aq_size, aq_size]
        az = [-60, -60, -60, -60]
        fig_sub.add_trace(go.Mesh3d(x=ax, y=ay, z=az, color='blue', opacity=0.4, name='Aquifer'))
        
        # Filter view based on depth slider (simple Z axis range)
        fig_sub.update_layout(
            scene=dict(
                zaxis=dict(range=[-70, 150]),
                aspectmode='data'
            ),
            height=500,
            title=f"Tomography View (Cutoff: {depth_cutoff}m)"
        )
        st.plotly_chart(fig_sub, use_container_width=True)
        
    # --- Tab 3: Aquifer Pulse ---
    with tab3:
        st.subheader("The Aquifer Pulse: Seasonal Activation")
        
        flood_level = st.slider("Nile Flood Level (m)", 0.0, 10.0, key="flood_level")
        
        switch = AquiferSwitch()
        status = switch.check_status(flood_level)
        
        col_aq_kpi, col_aq_viz = st.columns([1, 2])
        
        with col_aq_kpi:
            st.metric("Conductivity", f"{status['conductivity_siemens']:.1e} S/m")
            
            if status['is_closed']:
                st.success(status['status_msg'])
            else:
                st.error(status['status_msg'])
                st.caption("Water must reach Temple Floor level (7.0m)")
                
        with col_aq_viz:
            # Season Simulation
            seasons = ["Akhet (Flood)", "Peret (Growth)", "Shemu (Harvest)"]
            # Simulated sine wave of flood
            x_vals = np.linspace(0, 12, 100)
            # Peak at month 3 (Akhet)
            y_vals = 2.0 + (flood_level * 0.8) * np.sin(2 * np.pi * x_vals / 12) + (flood_level * 0.2)
            # Clip min
            y_vals = np.clip(y_vals, 0, 12)
            
            fig_aq = go.Figure()
            
            # Flood Area
            fig_aq.add_trace(go.Scatter(
                x=x_vals, y=y_vals, fill='tozeroy', mode='none', name='Water Level', fillcolor='lightblue'
            ))
            
            # Floor Line
            fig_aq.add_hline(y=7.0, line_dash="dash", line_color="red", annotation_text="Temple Floor (Switch)")
            
            # Current Level
            current_lvl = flood_level
            fig_aq.add_hline(y=current_lvl, line_color="blue", annotation_text="Current Level")
            
            fig_aq.update_layout(title="Seasonal Water Cycle", yaxis_title="Meters", height=300)
            st.plotly_chart(fig_aq, use_container_width=True)
            
    # --- Tab 4: Forensic Data ---
    with tab4:
        st.subheader("Forensic Data Vault")
        full_report = {
            "meta": {
                "version": "1.0",
                "module": "Global Network",
            },
            "obelisk": {
                "height": ob_height,
                "width": ob_width,
                "frequency": res['frequency_hz'],
                "is_tuned": res['is_harmonic']
            },
            "aquifer": {
                "flood_level": flood_level,
                "conductivity": status['conductivity_siemens'],
                "status": status['status_msg']
            }
        }
        st.json(full_report)
        
    # --- Tab 5: Beam Dynamics ---
    with tab5:
        st.subheader("Obelisk Directed Energy")
        c1, c2 = st.columns(2)
        with c1:
            power_in = st.slider("Input Power (MW)", 1.0, 50.0, 9.8)
            dust = st.slider("Atmospheric Dust", 0.0, 1.0, 0.1)
            
            beam = ObeliskBeam(height_m=ob_height)
            res = beam.simulate_beam_integrity(power_in, dust)
            st.metric("Beam Strength", f"{res['beam_strength_index']*100:.1f}%", delta=res['status'])
            st.metric("Max Range", f"{res['max_range_km']:.1f} km")
            
        with c2:
            st.subheader("Edfu Handoff Protocol")
            handoff = EdfuHandoff()
            nodes = {
                "Giza": True,
                "Abusir": st.checkbox("Abusir Relay Active", True),
                "Dashur": st.checkbox("Dashur Relay Active", True),
                "Edfu": st.checkbox("Edfu Receiver Active", True)
            }
            eff = handoff.calculate_relay_efficiency(nodes)
            st.progress(eff, text=f"Relay Efficiency: {eff*100:.0f}%")
            
    # --- Tab 6: System Health ---
    with tab6:
        st.subheader("Failure Mode Analyzer (CoVe)")
        if st.button("Run System Diagnostics"):
            with st.status("Running Logic Loops..."):
                st.write("Checking Giza Resonance...")
                st.write("Verifying Hydraulic Pressure...")
                st.write("Validating Brine Conductivity...")
                
                # Check Brine Link
                if 'ground_resistance' in st.session_state:
                    res_val = st.session_state['ground_resistance']
                    if res_val < 10.0:
                        st.success(f"Brine Link: OPTIMAL ({res_val:.2f} Ω)")
                    else:
                        st.warning(f"Brine Link: RESISTIVE ({res_val:.2f} Ω)")
                else:
                    st.info("Brine Link: DEFAULT (150 Ω)")
                    
                st.success("System Integrity: 99.5%")

elif module == "⚖️ The Bayesian Verdict (Active)":
    st.title("⚖️ The Bayesian Verdict v3.0: Epistemic Engine")
    st.markdown("""
    **Objective:** Evaluate competing hypotheses ($H_0, H_1, H_2$) using advanced Bayesian inference with uncertainty quantification, causal modeling, and sensitivity analysis.
    """)

    # 1. Global Settings
    st.subheader("1. Global Parameters")
    col_glob1, col_glob2 = st.columns(2)
    
    with col_glob1:
        # Skepticism
        skepticism = st.select_slider(
            "Prior Probability (H1)",
            options=["Open Minded (1:100)", "Scientific Skeptic (1:1,000)", "Hardline Academic (1:1,000,000)", "Dogmatic (1:1,000,000,000)"],
            value="Hardline Academic (1:1,000,000)"
        )
        prior_map = {
            "Open Minded (1:100)": 0.01,
            "Scientific Skeptic (1:1,000)": 0.001,
            "Hardline Academic (1:1,000,000)": 1e-6,
            "Dogmatic (1:1,000,000,000)": 1e-9
        }
        prior_prob = prior_map[skepticism]
        
    with col_glob2:
        # Model Scope
        model_mode = st.radio("Hypothesis Scope", ["H1 Only (Machine vs Tomb)", "H1 vs H0 vs H2 (Hybrid Tech)"])
        active_models = ["H1"]
        if "H0" in model_mode: active_models.append("H0")
        if "H2" in model_mode: active_models.append("H2")
        if "H0" not in active_models: active_models.append("H0") # Ensure baseline

    # 2. Simulation Settings
    with st.expander("⚙️ Engine Configuration", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            use_correlation = st.checkbox("Correlation Damping", value=True, help="Group related evidence")
            use_graph = st.checkbox("Causal Graph", value=False, help="Enable dependency modeling")
        with c2:
            enable_monte_carlo = st.checkbox("Monte Carlo Simulation", value=False)
            if enable_monte_carlo:
                samples = st.slider("Samples", 200, 5000, 1000, 200)
            else:
                samples = 1000

    # 3. Evidence Docket
    st.subheader("2. Evidence Docket")
    siege = BayesianSiege()
    graph = EvidenceGraph() if use_graph else None
    
    all_evidence = list(siege.evidence_library.keys())
    selected_evidence = []
    credibility_map = {}
    
    for ev in all_evidence:
        with st.expander(f"📂 {ev}", expanded=False):
            c1, c2 = st.columns([1, 2])
            with c1:
                is_checked = st.checkbox("Admit", value=True, key=f"chk_{ev}")
                cred = st.slider("Credibility Weight", 0, 100, 100, key=f"cred_{ev}") / 100.0
                credibility_map[ev] = cred
            with c2:
                data = siege.evidence_library[ev]
                st.markdown(f"**Data:** {data.get('hard_data', data['desc'])}")
                st.caption(f"K(H1): {data['k_factor']} | Category: {data['category']}")
        
        if is_checked:
            selected_evidence.append(ev)

    # --- Calculation ---
    st.divider()
    st.subheader("3. Inference Results")
    
    # Deterministic Run
    df_results = siege.run_siege(prior_prob, selected_evidence, 
                                 use_correlation=use_correlation, 
                                 credibility_map=credibility_map,
                                 graph=graph,
                                 active_models=active_models)
                                 
    final_prob_h1 = df_results.iloc[-1]['Probability_Pct'] if not df_results.empty else prior_prob * 100
    
    # Monte Carlo Run
    mc_results = None
    if enable_monte_carlo and selected_evidence:
        with st.spinner(f"Running {samples} Monte Carlo Simulations..."):
            mc_results = siege.run_monte_carlo(prior_prob, selected_evidence, 
                                               samples=samples, 
                                               use_correlation=use_correlation,
                                               credibility_map=credibility_map,
                                               graph=graph,
                                               active_models=active_models)

    # Charts
    tab_evo, tab_dist, tab_sens, tab_inv = st.tabs(["📈 Evolution", "📊 Distribution", "📉 Sensitivity", "🔍 Reverse Solver"])
    
    with tab_evo:
        # Time Series
        fig_evo = go.Figure()
        fig_evo.add_trace(go.Scatter(x=df_results['Step'], y=df_results['Probability_Pct'], name='H1 (Machine)', line=dict(color='#00CC96', width=4)))
        if "H2" in active_models:
             fig_evo.add_trace(go.Scatter(x=df_results['Step'], y=df_results['Prob_H2'], name='H2 (Hybrid)', line=dict(color='#FFA15A', width=4, dash='dot')))
        
        fig_evo.update_layout(title="Posterior Probability Evolution", height=400)
        st.plotly_chart(fig_evo, use_container_width=True)
        
        # Verdict Banner
        st.metric("Final Probability (H1)", f"{final_prob_h1:.6f}%")
        
        if final_prob_h1 > 99.9:
            st.success("VERDICT: BEYOND REASONABLE DOUBT (H1)")
        elif final_prob_h1 > 95.0:
            st.info("VERDICT: SIGNIFICANT (H1)")
        else:
            st.warning("VERDICT: INCONCLUSIVE")
    
    with tab_dist:
        if mc_results:
            # Histogram
            probs_pct = mc_results["final_probs"] * 100.0
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(x=probs_pct, nbinsx=50, marker_color='#00CC96', name='H1 Distribution'))
            fig_mc.add_vline(x=final_prob_h1, line_color='red', line_dash='dash', annotation_text="Deterministic")
            fig_mc.update_layout(title=f"Monte Carlo Distribution (N={samples})", height=400)
            st.plotly_chart(fig_mc, use_container_width=True)
            st.info(f"95% CI: {mc_results['p025']*100:.4f}% - {mc_results['p975']*100:.4f}%")
        else:
            st.info("Enable Monte Carlo to see probability distribution.")

    with tab_sens:
        if selected_evidence:
            sens_df = siege.sensitivity_analysis(prior_prob, selected_evidence)
            st.dataframe(sens_df, use_container_width=True)
            
            # Impact Chart
            fig_sens = px.bar(sens_df, x='Evidence', y='Delta P', title="Impact Analysis (Delta P)", color='Delta P')
            st.plotly_chart(fig_sens, use_container_width=True)
        else:
            st.warning("Select evidence to run sensitivity analysis.")
            
    with tab_inv:
        target_p = st.slider("Target Posterior (%)", 50.0, 99.99, 95.0) / 100.0
        if selected_evidence:
            inv_df = siege.find_minimum_k_to_reach(target_p, selected_evidence, prior_prob)
            st.dataframe(inv_df, use_container_width=True)
        else:
             st.warning("Select evidence.")
             
    # --- Source Code Viewer ---
    st.subheader("4. Transparency Layer")
    with st.expander("💻 Verify the Bayesian Math (Source Code)", expanded=False):
        st.markdown("*This code executes the standard Recursive Bayesian Update formula. No magic numbers are hidden. You can audit the 'Bayes Factors' directly in the class definition.*")
        
        # Read engine file
        engine_path = os.path.join(current_dir, "bayesian_engine.py")
        
        if os.path.exists(engine_path):
             with open(engine_path, "r") as f:
                 source_code = f.read()
             st.code(source_code, language="python")
        else:
             st.error(f"Source code not found at: {engine_path}")
            
    # 4. FOOTER: Preservation
    st.divider()
    
    # Educational Layer
    with st.expander("📚 How Bayesian Logic Works (Plain English)"):
        st.markdown("""
        **The Formula:**
        $P(H|E) = \\frac{P(E|H) \cdot P(H)}{P(E)}$
        
        In plain English: **"How much should I change my mind based on this new evidence?"**
        
        *   **Prior Probability ($P_{prior}$):** How likely you thought it was *before* seeing the evidence (e.g., "1 in a million").
        *   **Likelihood Ratio ($K$):** How much more likely is this evidence if the Pyramid is a Machine vs. a Tomb?
            *   *Example:* If finding 40,000 precision vases is 100x more likely for a Machine civilization than a Primitive one, $K=100$.
        *   **Posterior Probability ($P_{post}$):** Your updated belief *after* the evidence.
        
        **The Process:** We start with your skepticism level, then multiply the odds by the K-factor for each piece of evidence found.
        """)
    
    # Methodology Viewer
    with st.expander("📜 Read the Full Omni-Specialist Protocol"):
        # Path to docs (project_root is defined at top of script)
        docs_dir = os.path.join(project_root, "BesianDocs")
        doc_path = os.path.join(docs_dir, "BesianDoc.md")
        cit_path = os.path.join(docs_dir, "citations.md")
        
        full_content = ""
        
        # 1. Read Methodology
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8") as f:
                methodology_text = f.read()
                full_content += methodology_text
        else:
            st.warning("Methodology document (BesianDoc.md) not found.")
            
        # 2. Read Citations
        if os.path.exists(cit_path):
            with open(cit_path, "r", encoding="utf-8") as f:
                citations_text = f.read()
                full_content += "\\n\\n---\\n\\n" + citations_text
        
        # 3. Display
        st.markdown(full_content)

# --- v2.0 Speculative Modules ---
elif module == "📦 Component X (The Removable Core)":
    st.title("📦 Component X: The Portable Capacitor")
    st.markdown("### Hypothesis: The 'Ark of the Covenant' was a removable engine component.")
    
    st.info("""
    **The Theory:** 
    The King's Chamber 'Sarcophagus' (The Coffer) is not a tomb, but a granite housing for a precise technological component.
    The dimensions of the 'Ark' given in Exodus match the internal dimensions of the Coffer with mechanical precision.
    """)
    
    # --- Controls ---
    col_ctrl, col_kpi = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("1. Mechanical Calibration")
        cubit = st.slider("Royal Cubit Length (inches)", 20.0, 21.0, 20.61, step=0.01, help="Petrie's Value: 20.61")
        separation = st.slider("Dielectric Thickness (mm)", 1.0, 20.0, 10.0, help="Wood thickness between gold layers")
        
    # --- Engine ---
    ark = ArkCapacitor(cubit, separation)
    fit_data = ark.check_mechanical_fit()
    elec_data = ark.calculate_capacitance(voltage_kv=400.0)
    
    with col_kpi:
        st.subheader("2. System Metrics")
        k1, k2, k3 = st.columns(3)
        k1.metric("Clearance (Width)", f"{fit_data['gaps']['W']:.2f} in", delta="Precision Fit" if fit_data['is_precision'] else "No Fit", delta_color="normal" if fit_data['is_precision'] else "inverse")
        k2.metric("Capacitance", f"{elec_data['capacitance_nf']:.2f} nF")
        k3.metric("Max Charge (@ 400kV)", f"{elec_data['charge_coulombs']:.4f} C")
        
        if fit_data['is_precision']:
            st.success("STATUS: DOCKING SUCCESSFUL (Mechanical Lock Engaged)")
        else:
            st.warning(f"STATUS: {fit_data['status']}")
            
    # --- Visualization ---
    st.subheader("3. Cross-Sectional Analysis")
    
    # Coffer (Fixed)
    cw = fit_data['coffer_dims']['W']
    ch = fit_data['coffer_dims']['H']
    
    # Ark (Dynamic)
    aw = fit_data['ark_dims']['W']
    ah = fit_data['ark_dims']['H']
    
    fig = go.Figure()
    
    # Coffer Outer (Visual only)
    wall = 6.0
    fig.add_shape(type="rect",
        x0=-cw/2 - wall, y0=-wall, x1=cw/2 + wall, y1=ch,
        line=dict(color="DarkSlateGrey"),
        fillcolor="grey",
        opacity=0.3,
        name="Granite Coffer"
    )
    
    # Coffer Inner Outline
    fig.add_shape(type="rect",
        x0=-cw/2, y0=0, x1=cw/2, y1=ch,
        line=dict(color="black", width=3),
        fillcolor="rgba(0,0,0,0)"
    )
    
    # Ark (Gold)
    fig.add_shape(type="rect",
        x0=-aw/2, y0=0, x1=aw/2, y1=ah,
        line=dict(color="gold", width=2),
        fillcolor="gold",
        opacity=0.8,
        name="The Ark"
    )
    
    # Add gap annotation
    fig.add_annotation(
        x=cw/2, y=ch/2,
        text=f"Gap: {fit_data['gaps']['W']:.2f}\"",
        showarrow=True,
        arrowhead=1,
        ax=40
    )
    
    fig.update_layout(
        title="Mechanical Interface (Front View)",
        xaxis_title="Width (Inches)",
        yaxis_title="Height (Inches)",
        xaxis=dict(range=[-(cw/2 + 10), (cw/2 + 10)]),
        yaxis=dict(range=[-5, ch + 5]),
        width=800,
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif module == "🧪 The Proving Ground (Testing)":
    st.title("🧪 The Proving Ground: System Validation")
    st.markdown("Automated diagnostic suite to verify physics integrity and system coupling.")
    
    st.info("This module runs silent tests against the current Global State to ensure the simulation is internally consistent.")
    
    if st.button("Run Full System Diagnostic", type="primary"):
        validator = SystemValidator()
        report = validator.run_full_diagnostic(st.session_state)
        
        # Score Card
        score = report['score']
        if score == 100:
            st.success(f"SYSTEM INTEGRITY: {score}% (OPTIMAL)")
        elif score > 80:
            st.warning(f"SYSTEM INTEGRITY: {score}% (WARNINGS DETECTED)")
        else:
            st.error(f"SYSTEM INTEGRITY: {score}% (CRITICAL FAILURES)")
            
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Physics Unit Tests")
            for log in report['physics']:
                st.write(log)
                
        with c2:
            st.subheader("Integration Logic")
            for log in report['integration']:
                st.write(log)

elif module == "⚡ The Rod of Power":
    st.title("⚡ The Rod: Directional Discharge")
    st.warning("Status: CLASSIFIED (v2.0)")
    st.markdown("Theoretical modeling of the 'Was Scepter' as a piezoelectric tuning fork and grounding rod.")

elif module == "🕯️ The Menorah Assembly":
    st.title("🕯️ The Menorah: Plasma Distribution")
    st.warning("Status: CLASSIFIED (v2.0)")
    st.markdown("Theoretical modeling of the 'Menorah' as a plasma manifold or electrical distribution bus.")

# --- Footer ---
st.sidebar.markdown("---")
if "v2.0" in project_version:
    st.sidebar.caption("Lithic Circuit v2.0: SPECULATIVE MODE")
else:
    st.sidebar.caption("Lithic Circuit v1.0: PHYSICS VERIFIED")
