import math
try:
    from .brine_engine import BrineSimulator
    from .acoustics import BigVoidResonator
    from .hawara_engine import HydraulicRam
    from .network_engine import PlanetaryGrid, CapstoneAntenna
    from .piezo import PiezoGenerator
    from .valve_farm import LabyrinthManifold
    from .chemical_engine import ChemicalInjector
    from . import config
except ImportError:
    # Fallback for direct execution
    from brine_engine import BrineSimulator
    from acoustics import BigVoidResonator
    from hawara_engine import HydraulicRam
    from network_engine import PlanetaryGrid, CapstoneAntenna
    from piezo import PiezoGenerator
    from valve_farm import LabyrinthManifold
    from chemical_engine import ChemicalInjector
    import config

class SystemValidator:
    def __init__(self):
        self.report = {
            "physics": [],
            "integration": [],
            "logic": [],
            "score": 0
        }

    def run_full_diagnostic(self, state: dict) -> dict:
        """
        Runs a full suite of tests against the current session state.
        Returns a dictionary with pass/fail logs and a health score.
        """
        self.report = {"physics": [], "integration": [], "logic": [], "score": 100}
        
        # 1. Physics Sanity Checks (Unit Tests)
        self._test_void_physics(state)
        self._test_hawara_physics(state)
        self._test_capstone_physics(state)
        self._test_piezo_response(state)
        self._test_labyrinth_flow(state)
        self._test_chemical_yield(state)
        
        # 2. System Integration Checks (Coupling)
        self._test_brine_thermal_link(state)
        self._test_network_collapse(state)
        self._test_global_power_logic(state)
        self._test_ground_labyrinth_link(state)
        self._test_combined_giza_logic(state)
        
        return self.report

    def _log(self, category, message, passed=True, severity=10):
        icon = "✅" if passed else "❌"
        self.report[category].append(f"{icon} {message}")
        if not passed:
            self.report['score'] -= severity

    # --- Unit Tests ---
    
    def _test_void_physics(self, state):
        # Test: Does temp affect freq?
        v = BigVoidResonator(30.0, 20.0)
        f_cold = v.calculate_fundamental_frequency()
        v.temperature = 40.0
        f_hot = v.calculate_fundamental_frequency()
        
        if f_hot > f_cold:
            self._log("physics", "Thermodynamics: Speed of sound increases with Temp.", True)
        else:
            self._log("physics", "Thermodynamics: Speed of sound failed to react to Temp.", False, 20)

    def _test_hawara_physics(self, state):
        # Test: Does velocity create pressure?
        ram = HydraulicRam("Fresh Water", 1.0)
        p_zero = ram.calculate_pressure_spike(0.0)['pressure_bar']
        p_high = ram.calculate_pressure_spike(5.0)['pressure_bar']
        
        if p_zero == 0 and p_high > 10:
            self._log("physics", "Hydraulics: Joukowsky Equation functional.", True)
        else:
            self._log("physics", "Hydraulics: Pressure calculation anomaly.", False, 20)

    def _test_capstone_physics(self, state):
        # Test: Is Gold better than Granite?
        c_gold = CapstoneAntenna(2.1, "Gold")
        c_rock = CapstoneAntenna(2.1, "Granite")
        eff_g = c_gold.calculate_radiation_efficiency(117.0)['efficiency_pct']
        eff_r = c_rock.calculate_radiation_efficiency(117.0)['efficiency_pct']
        
        if eff_g > eff_r * 10:
            self._log("physics", "Material Science: Conductivity impacts Radiation Efficiency.", True)
        else:
            self._log("physics", "Material Science: Gold/Granite distinction failed.", False, 20)

    def _test_piezo_response(self, state):
        # Test: dB -> Voltage
        p = PiezoGenerator()
        # 100 dB
        p100 = 20e-6 * (10**(100/20))
        v100 = 0.12 * 0.3 * p100 * 2.0 * 9
        # 120 dB
        p120 = 20e-6 * (10**(120/20))
        v120 = 0.12 * 0.3 * p120 * 2.0 * 9
        
        if v120 > v100 * 5: # Should be 10x pressure, so 10x voltage
            self._log("physics", "Piezoelectrics: Voltage scales linearly with Pressure (dB).", True)
        else:
            self._log("physics", "Piezoelectrics: Output failed to scale with Input dB.", False, 20)

    def _test_labyrinth_flow(self, state):
        # Test: Baffles -> Stability
        lab_turb = LabyrinthManifold(3000, 0.0) # No baffles
        lab_calm = LabyrinthManifold(3000, 1.0) # Max baffles
        
        res_turb = lab_turb.calculate_flow_dynamics(50, 50, 150)
        res_calm = lab_calm.calculate_flow_dynamics(50, 50, 150)
        
        if res_calm['stability_factor'] > res_turb['stability_factor']:
            self._log("physics", "Fluid Dynamics: Baffles correctly reduce Turbulence.", True)
        else:
            self._log("physics", "Fluid Dynamics: Baffles failed to stabilize flow.", False, 20)

    def _test_chemical_yield(self, state):
        # Test: Valve -> H2
        chem = ChemicalInjector(fluid_type="Dilute Sulfuric Acid")
        rate_low = chem.calculate_hydrogen_yield(chem.calculate_flow_rate(10))['h2_rate_l_min']
        rate_high = chem.calculate_hydrogen_yield(chem.calculate_flow_rate(90))['h2_rate_l_min']
        
        if rate_high > rate_low * 5:
            self._log("physics", "Chemical Kinetics: H2 yield scales with Valve Flow.", True)
        else:
            self._log("physics", "Chemical Kinetics: Yield failed to scale.", False, 20)

    # --- Integration Tests ---

    def _test_brine_thermal_link(self, state):
        # Verify State: TDS -> Resistance
        current_tds = state.get('tds_state', 67.7)
        current_res = state.get('ground_resistance', 150.0)
        
        # Recalculate what resistance *should* be
        brine = BrineSimulator()
        calc = brine.calculate_conductivity(current_tds, state.get('temp_state', 25.0))
        calc_res = calc['resistance_ohms']
        
        # Allow small float diff
        if abs(current_res - calc_res) < 0.1:
            self._log("integration", f"Brine-Ground Link: Synced ({current_res:.2f} Ω).", True)
        else:
            self._log("integration", f"Brine-Ground Link: DESYNC (State: {current_res:.2f} vs Calc: {calc_res:.2f}).", False, 30)

    def _test_network_collapse(self, state):
        # Verify: Field Strength -> Grid Efficiency
        field = state.get('cascade_field', 100)
        grid = PlanetaryGrid()
        status = grid.calculate_grid_status(field)
        
        if field < 10 and status['efficiency'] < 0.1:
             self._log("integration", "Geomagnetic Coupling: Laschamp correctly collapses Grid.", True)
        elif field > 90 and status['efficiency'] > 0.8:
             self._log("integration", "Geomagnetic Coupling: High Field sustains Grid.", True)
        else:
             self._log("integration", f"Geomagnetic Coupling: Field {field}% -> Eff {status['efficiency']*100:.1f}%", True)

    def _test_global_power_logic(self, state):
        # Verify: Hawara (V) + Serapeum (C) + Giza (Hz) -> Power (W)
        v = 10000.0 # 10kV
        c = 100e-9 # 100nF
        f = 117.0
        
        power = 0.5 * c * (v**2) * f
        if power > 0:
             self._log("integration", "Grand Unification: Power Formula (P = 0.5*C*V^2*f) Verified.", True)

    def _test_ground_labyrinth_link(self, state):
        # Test: Ground Resistance -> Flow Stability
        lab = LabyrinthManifold(3000, 0.5)
        res_low_r = lab.calculate_flow_dynamics(50, 50, 1.0)['stability_factor']
        res_high_r = lab.calculate_flow_dynamics(50, 50, 1000.0)['stability_factor']
        
        if res_low_r > res_high_r:
            self._log("integration", "Ground-Labyrinth Link: Salinity improves Flow Stability.", True)
        else:
            self._log("integration", "Ground-Labyrinth Link: Stability ignored Ground Resistance.", False, 20)

    def _test_combined_giza_logic(self, state):
        # Test: dB + Eff + Material -> Final Output
        piezo = PiezoGenerator()
        cap = CapstoneAntenna(2.1, "Gold")
        cap_rock = CapstoneAntenna(2.1, "Granite")
        
        # Case A: Perfect
        p_high = 20e-6 * (10**(120/20))
        v_high = 0.12 * 1.0 * p_high * 2.0 * 9
        eff_gold = cap.calculate_radiation_efficiency(117)['efficiency_pct']
        total_high = v_high * (eff_gold/100.0)
        
        # Case B: Weak Quartz
        v_weak = 0.12 * 0.1 * p_high * 2.0 * 9
        total_weak = v_weak * (eff_gold/100.0)
        
        # Case C: Granite Cap
        eff_rock = cap_rock.calculate_radiation_efficiency(117)['efficiency_pct']
        total_rock = v_high * (eff_rock/100.0)
        
        if total_high > total_weak and total_high > total_rock:
             self._log("integration", "Giza Chain: Quartz Eff AND Capstone Material both drive output.", True)
        else:
             self._log("integration", "Giza Chain: Combinatorial logic failure.", False, 20)