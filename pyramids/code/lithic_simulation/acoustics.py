import math
from typing import Dict, List

# Robust Import Logic for Config
try:
    from lithic_simulation import config
except ImportError:
    try:
        from . import config
    except ImportError:
        import config

class ResonantChamber:
    def __init__(self, length: float, width: float, height: float):
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height

    def calculate_room_modes(self, max_order: int = 9) -> Dict[str, List[float]]:
        """Calculates axial standing wave frequencies for X, Y, Z axes up to the 9th harmonic."""
        modes = {'x': [], 'y': [], 'z': []}
        c = config.SPEED_OF_SOUND_AIR
        
        dims = {'x': self.length, 'y': self.width, 'z': self.height}
        
        for axis, d in dims.items():
            # Calculate harmonics 1 through 9
            for n in range(1, max_order + 1):
                f = (c / 2) * (n / d)
                modes[axis].append(f)
        return modes

    def check_resonance_match(self, modes: Dict[str, List[float]], target: float, tolerance_percent: float = 0.05) -> Dict:
        """
        Scans all harmonics to see if any match the target frequency.
        Returns match status and details of the closest harmonic.
        """
        all_harmonics = []
        for axis, freqs in modes.items():
            for i, f in enumerate(freqs):
                all_harmonics.append({'axis': axis, 'order': i+1, 'freq': f})
        
        # Find closest harmonic
        closest = min(all_harmonics, key=lambda x: abs(x['freq'] - target))
        deviation = abs(closest['freq'] - target)
        max_dev = target * tolerance_percent
        
        return {
            "is_match": deviation <= max_dev,
            "closest_harmonic": closest,
            "deviation": deviation
        }

    def calculate_helmholtz_neck_length(self, neck_area: float, target_freq: float) -> float | None:
        """
        Solves for Neck Length (L) given a Target Frequency using Helmholtz equation 
        with End Correction. Returns None if geometry is impossible (negative length).
        
        Standard Formula: f = (c / 2pi) * sqrt(A / (V * L_effective))
        L_effective = L_physical + Correction
        Correction approx 0.85 * radius (for flanged pipe approximation)
        """
        c = config.SPEED_OF_SOUND_AIR
        # Calculate effective radius from area (assuming square/circle equivalence for correction)
        r = math.sqrt(neck_area / math.pi)
        correction = 0.85 * r
        
        # Rearranged Helmholtz to solve for Effective Length
        # L_eff = (A * c^2) / (V * 4pi^2 * f^2)
        
        numerator = neck_area * (c ** 2)
        denominator = self.volume * 4 * (math.pi ** 2) * (target_freq ** 2)
        
        l_effective = numerator / denominator
        
        # Calculate physical length
        l_physical = l_effective - correction
        
        if l_physical < 0:
            return None
        
        return l_physical

    def calculate_strouhal_resonance(self, wind_speed_kmh: float, shaft_width_m: float = 0.21, temperature_c: float = 25.0) -> dict:
        strouhal_number = 0.15
        velocity_ms = wind_speed_kmh * 0.27778
        c = 331.3 + (0.606 * temperature_c) # Speed of sound adjustment
        f_vortex = (strouhal_number * velocity_ms) / shaft_width_m
        shaft_length = 60.0 # Assuming a 60m shaft length for pipe resonance
        f_pipe = c / (2 * shaft_length) # Fundamental for open-open pipe
        return {
            "fundamental": f_vortex,
            "harmonics": [f_vortex, f_vortex*2, f_vortex*3, f_vortex*4],
            "velocity_ms": velocity_ms,
            "pipe_resonance": f_pipe
        }

class BigVoidResonator:
    def __init__(self, length_meters: float, temperature_c: float = 20.0):
        self.length = length_meters
        self.temperature = temperature_c

    def calculate_fundamental_frequency(self) -> float:
        """Calculates fundamental standing wave frequency: f = c / (2L)"""
        # Recalculate c to account for temperature changes
        c = 331.3 * math.sqrt(1 + (self.temperature / 273.15))
        return c / (2 * self.length)

    def check_harmonic_coupling(self, target_freq: float = 117.0, tolerance_percent: float = 0.05) -> dict:
        """
        Checks if the target frequency is an integer multiple of the Void's fundamental.
        Returns a dict with match status and harmonic ratio.
        """
        fundamental = self.calculate_fundamental_frequency()
        if fundamental == 0:
            return {"is_match": False, "ratio": 0.0, "fundamental": 0.0}
            
        ratio = target_freq / fundamental
        nearest_int = round(ratio)
        
        # Check if close to integer
        if nearest_int == 0:
            deviation = 1.0
        else:
            deviation = abs(ratio - nearest_int) / nearest_int
            
        is_match = deviation <= tolerance_percent
        
        return {
            "is_match": is_match,
            "ratio": ratio,
            "nearest_harmonic": nearest_int,
            "fundamental": fundamental,
            "deviation": deviation
        }

class ResonatorArray:
    def __init__(self, slot_count: int = 27, array_length_m: float = 47.0, input_frequency: float = 117.0):
        """
        Models the Grand Gallery's 27 resonator slots as a Phased Array.
        """
        self.slot_count = slot_count
        self.array_length = array_length_m
        self.frequency = input_frequency
        self.spacing = array_length_m / slot_count if slot_count > 0 else 0
        
    def simulate_amplification(self, input_db: float, coherence_percent: float) -> dict:
        """
        Simulates signal growth.
        Gain = 20 * log10(N) * Efficiency.
        """
        efficiency = coherence_percent / 100.0
        
        if self.slot_count <= 0:
            gain = 0.0
        else:
            # Constructive Interference (Coherent Sum) -> 20 log10(N)
            base_gain = 20 * math.log10(self.slot_count)
            gain = base_gain * efficiency
            
        output_db = input_db + gain
        
        # Generate Profile
        profile = []
        current_db = input_db
        
        for i in range(self.slot_count + 1):
            dist = i * self.spacing
            # Linear approximation of gain distribution
            if i > 0:
                step_gain = gain / self.slot_count
                current_db += step_gain
                
            profile.append({
                "distance_m": dist,
                "slot_index": i,
                "signal_db": current_db
            })
            
        return {
            "total_gain_db": gain,
            "output_db": output_db,
            "profile": profile
        }
