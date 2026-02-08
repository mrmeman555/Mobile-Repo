import numpy as np
import pandas as pd

# Robust Import Logic for Config
try:
    from lithic_simulation import config
except ImportError:
    try:
        from . import config
    except ImportError:
        import config

class PiezoGenerator:
    def simulate_voltage_sweep(self, min_db: float, max_db: float, efficiency: float, thickness: float, beam_count: int = 9, static_load_tons: float = 0, internal_pressure_pa: float = 0.0) -> pd.DataFrame:
        """
        Vectorized simulation of voltage output across a dB range.
        Includes beam stacking (9 beams) and pre-stress sensitivity multiplier.
        Optional: internal_pressure_pa (Chemical/Hydraulic Boost).
        """
        # Pre-Stress Multiplier: Compressed quartz is more sensitive
        # If static load > 500 tons, boost efficiency by 1.5x
        efficiency_multiplier = 1.5 if static_load_tons > 500 else 1.0
        effective_efficiency = efficiency * efficiency_multiplier
        
        # Create array of dB values
        db_values = np.linspace(min_db, max_db, 100)
        
        # Convert dB to Pressure (Pascals)
        # P = P_ref * 10^(dB/20), where P_ref is 20 microPascals (air)
        acoustic_pressure_pa = 20e-6 * (10 ** (db_values / 20))
        
        # Total Dynamic Stress
        total_stress_pa = acoustic_pressure_pa + internal_pressure_pa
        
        # Calculate Voltage per beam: V = g33 * efficiency * Pressure * thickness
        single_beam_voltage = config.VOLTAGE_CONSTANT_QUARTZ * effective_efficiency * total_stress_pa * thickness
        
        # Total Voltage (Series Stacking)
        total_voltage = single_beam_voltage * beam_count
        
        return pd.DataFrame({
            'db': db_values,
            'pressure_pa': total_stress_pa,
            'single_beam_voltage': single_beam_voltage,
            'voltage': total_voltage # Stacked voltage
        })
