import numpy as np
import pandas as pd
try:
    from . import config
except ImportError:
    import config

class PhononicTunnel:
    def __init__(self, lattice_spacing: float, scatterer_mass_tons: float, host_speed: float = 3000.0):
        self.lattice_spacing = lattice_spacing
        self.scatterer_mass = scatterer_mass_tons * 1000.0 # Convert to kg
        self.host_speed = host_speed
        self.host_density = 2400.0 # Limestone density kg/m^3
        
        # Liu et al. (2000) Parameters for Locally Resonant Sonic Material (LRSM)
        # Filling Fraction (Volume of scatterer / Volume of unit cell)
        # Assume box ~ 20m^3, tunnel segment ~ 6m x 3m x 3m = 54m^3
        self.filling_fraction = 20.0 / 54.0 
        
        # Resonance Frequency of the Scatterer (The Box)
        # Modeled as a mass on a stiffness spring (floor coupling)
        # Target ~20 Hz natural frequency for infrasound blocking
        self.resonance_freq_hz = 20.0 
        self.resonance_omega = 2 * np.pi * self.resonance_freq_hz

    def calculate_effective_density(self, freqs: np.ndarray) -> np.ndarray:
        """
        Calculates Effective Mass Density (rho_eff) using the LRSM model.
        rho_eff = rho_0 * (1 - F * w_res^2 / (w^2 - w_res^2))
        
        When w is slightly above w_res, rho_eff becomes NEGATIVE.
        This creates a 'Stop Band' where sound cannot propagate.
        """
        omegas = 2 * np.pi * freqs
        
        # Avoid division by zero at exact resonance
        omegas_safe = np.where(omegas == self.resonance_omega, omegas + 1e-6, omegas)
        
        numerator = self.filling_fraction * (self.resonance_omega ** 2)
        denominator = (omegas_safe ** 2) - (self.resonance_omega ** 2)
        
        term = numerator / denominator
        rho_eff = self.host_density * (1 - term)
        
        return rho_eff

    def simulate_transmission(self, min_freq: float = 1.0, max_freq: float = 50.0) -> pd.DataFrame:
        """
        Simulates acoustic transmission based on Effective Density.
        If rho_eff < 0, Transmission -> -100 dB (Total Reflection).
        """
        freqs = np.linspace(min_freq, max_freq, 500)
        rho_eff = self.calculate_effective_density(freqs)
        
        transmission = []
        
        for rho in rho_eff:
            if rho < 0:
                # Negative Mass Regime = Band Gap = No Transmission
                transmission.append(-100.0)
            else:
                # Pass Band (Simplified low loss)
                transmission.append(-2.0)
        
        return pd.DataFrame({
            'frequency': freqs,
            'transmission_db': transmission,
            'effective_density': rho_eff
        })

class GraniteCapacitor:
    def __init__(self, dielectric_constant: float = 5.5, wall_thickness: float = 0.4):
        self.dielectric_constant = dielectric_constant
        self.wall_thickness = wall_thickness
        self.epsilon_0 = 8.854e-12 # Vacuum permittivity F/m

    def calculate_storage_potential(self, box_count: int = 24) -> dict:
        """
        Calculates Geometric Capacitance and Stored Energy.
        C = (k * e0 * A) / d
        U = 0.5 * C * V^2
        """
        # 1. Calculate Internal Surface Area (2lw + 2lh + 2wh)
        # Box Dims: 3.8m x 2.3m x 2.1m
        l, w, h = 3.8, 2.3, 2.1
        box_internal_area = 2 * (l*w + l*h + w*h) # Approx 43.1 m^2
        
        # 2. Calculate Single Box Capacitance (Farads)
        # C = (k * e0 * A) / d
        c_single = (self.dielectric_constant * self.epsilon_0 * box_internal_area) / self.wall_thickness
        
        # 3. Calculate Array Total (Parallel)
        c_total = c_single * box_count
        
        # 4. Calculate Stored Energy (Joules)
        # Max Voltage input from Giza Generator ~ 81.0 Volts
        v_giza = 81.0
        joules = 0.5 * c_total * (v_giza ** 2)
        
        # Return strictly formatted dictionary including voltage_input for UI
        return {
            'capacitance_nF': c_total * 1e9,
            'stored_energy_joules': joules,
            'voltage_input': v_giza
        }
