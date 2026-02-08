import numpy as np
import pandas as pd
try:
    from . import config
except ImportError:
    import config

class ObeliskTuner:
    def __init__(self):
        self.E = 60e9 # Young's Modulus (Pa) - Aswan Granite
        self.rho = 2700.0 # Density (kg/m3)

    def calculate_resonance(self, height_m: float, base_width_m: float) -> dict:
        """
        Calculates fundamental frequency of the Obelisk acting as a cantilever beam.
        Formula: f = (1.875^2 / (2*pi*L^2)) * sqrt(E*I / (rho*A))
        """
        I = (base_width_m ** 4) / 12.0
        A = base_width_m ** 2
        
        if height_m <= 0 or base_width_m <= 0:
            return {"frequency_hz": 0.0, "is_harmonic": False, "match_details": "Invalid"}

        term1 = (1.875 ** 2) / (2 * np.pi * (height_m ** 2))
        term2 = np.sqrt((self.E * I) / (self.rho * A))
        freq = term1 * term2
        
        target = config.TARGET_FREQUENCY # 117.0
        is_match = False
        match_type = "None"
        
        factors = [0.25, 0.5, 1.0, 2.0, 4.0]
        for f in factors:
            t = target * f
            if abs(freq - t) < 1.0:
                is_match = True
                match_type = f"Match: {t:.1f} Hz ({f}x Giza)"
                break
                
        return {
            "frequency_hz": freq,
            "is_harmonic": is_match,
            "match_details": match_type
        }

class AquiferSwitch:
    def __init__(self):
        self.floor_level = 7.0 # Meters (Temple Floor)
        
    def check_status(self, flood_level_m: float) -> dict:
        is_active = flood_level_m >= self.floor_level
        sigma = 0.5 if is_active else 1e-12
        status_msg = "CIRCUIT CLOSED: SYSTEM ONLINE" if is_active else "CIRCUIT OPEN: WAITING FOR FLOOD"
        return {
            "is_closed": is_active,
            "conductivity_siemens": sigma,
            "status_msg": status_msg
        }

class PlanetaryGrid:
    def __init__(self):
        self.base_power_mw = 9.8
        
    def calculate_grid_status(self, field_strength_pct: float) -> dict:
        efficiency = (field_strength_pct / 100.0) ** 2
        current_output = self.base_power_mw * efficiency
        
        if field_strength_pct < 5.0:
            status = "COLLAPSED"
            color = "rgba(0,0,0,0)"
        elif field_strength_pct < 20.0:
            status = "CRITICAL"
            color = "red"
        elif field_strength_pct < 80.0:
            status = "UNSTABLE"
            color = "orange"
        else:
            status = "STABLE"
            color = "#00FF00"
            
        return {
            "efficiency": efficiency,
            "output_mw": current_output,
            "status": status,
            "line_color": color
        }
        
    def generate_collapse_timeline(self) -> pd.DataFrame:
        years_bp = np.linspace(50000, 0, 500)
        field_strength = np.ones_like(years_bp) * 100.0
        center = 42000
        width = 2000
        dip_magnitude = 95.0
        dip = dip_magnitude * np.exp(-((years_bp - center)**2) / (2 * width**2))
        field_strength -= dip
        power = self.base_power_mw * ((field_strength / 100.0) ** 2)
        
        df = pd.DataFrame({
            "Year_BP": years_bp,
            "Field_Strength": field_strength,
            "Grid_Power_MW": power
        })
        df['Time_Axis'] = -df['Year_BP']
        return df

class CapstoneAntenna:
    def __init__(self, base_width_m: float, material: str = "Gold"):
        self.base_width = base_width_m
        self.height = base_width_m * 0.636
        self.material = material
        
        if material == "Gold":
            self.conductivity = 4.1e7
        elif material == "Electrum":
            self.conductivity = 3.5e7
        elif material == "Granite":
            self.conductivity = 1e-5
        else:
            self.conductivity = 1.0
            
    def calculate_radiation_efficiency(self, frequency_hz: float = 117.0) -> dict:
        if self.conductivity > 1e5:
            efficiency_pct = 90.0 + (self.conductivity / 1e8) * 10.0
            efficiency_pct = min(efficiency_pct, 99.9)
            mode = "EMITTER"
        else:
            efficiency_pct = 0.1
            mode = "RESISTOR (FAILURE)"
            
        power_mw = (self.base_width ** 2) * (efficiency_pct / 100.0) * 2.0
        
        return {
            "efficiency_pct": efficiency_pct,
            "broadcast_power_mw": power_mw,
            "mode": mode,
            "height_m": self.height
        }

class ObeliskBeam:
    def __init__(self, height_m: float, material_quartz_pct: float = 90.0):
        self.height = height_m
        self.quartz_content = material_quartz_pct
        
    def simulate_beam_integrity(self, power_mw: float, atmosphere_opacity: float) -> dict:
        """
        Simulates the coherence of the directed energy beam.
        atmosphere_opacity: 0.0 (Vacuum) to 1.0 (Sandstorm).
        """
        base_coherence = (self.quartz_content / 100.0) * np.sqrt(max(0, power_mw))
        attenuation = np.exp(-atmosphere_opacity * 5.0)
        final_strength = base_coherence * attenuation
        
        # Normalize strength for display (0-1 range)
        # If Power=10MW, sqrt=3.16. Max expected ~3.
        strength_norm = min(final_strength / 3.0, 1.0)
        
        return {
            "beam_strength_index": strength_norm,
            "max_range_km": strength_norm * 50.0,
            "status": "LOCKED" if strength_norm > 0.5 else "SCATTERING"
        }

class EdfuHandoff:
    def __init__(self):
        self.relay_nodes = ["Giza", "Abusir", "Dashur", "Edfu"]
        
    def calculate_relay_efficiency(self, node_status: dict) -> float:
        """
        node_status: dict of {NodeName: boolean_is_active}
        """
        active_count = sum([1 for n in self.relay_nodes if node_status.get(n, False)])
        return active_count / len(self.relay_nodes)
