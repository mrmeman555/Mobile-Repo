import numpy as np

class GroundingHeat:
    def __init__(self, system_power_mw: float, voltage_kv: float, ground_resistance_ohms: float):
        self.power = system_power_mw * 1e6 # Watts
        self.voltage = voltage_kv * 1e3 # Volts
        self.resistance = ground_resistance_ohms
        
        # Constants
        self.density_limestone = 2500.0 # kg/m^3
        self.specific_heat = 900.0 # J/kgK (0.9 kJ/kgK)
        self.mass_zone = self.density_limestone * 10.0 # 10 m^3 zone
        
    def calculate_temperature_delta(self, cooling_factor: float = 0.0007) -> dict:
        """
        Calculates resistive heating delta T.
        """
        # 1. Current (I = P/V)
        if self.voltage == 0:
            current = 0.0
        else:
            current = self.power / self.voltage
            
        # 2. Heat (Q = I^2 * R)
        heat_watts = (current ** 2) * self.resistance
        
        # 3. Temp Rise (dT = Q / (m * c * cooling))
        # Adjusted formula to match prompt structure but yield Celsius
        # Cooling factor represents steady-state heat dissipation efficiency
        denominator = self.mass_zone * self.specific_heat * cooling_factor
        
        if denominator == 0:
            delta_t = 0.0
        else:
            delta_t = heat_watts / denominator
            
        return {
            "current_amps": current,
            "heat_watts": heat_watts,
            "delta_t_celsius": delta_t
        }

