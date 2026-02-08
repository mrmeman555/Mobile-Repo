import numpy as np

class ChemicalInjector:
    def __init__(self, shaft_width_m: float = 0.2, angle_deg: float = 39.0, fluid_type: str = "Dilute Sulfuric Acid"):
        self.width = shaft_width_m
        self.height = shaft_width_m # Square shaft
        self.angle = angle_deg
        self.fluid_type = fluid_type
        
        # Fluid Properties
        if "Acid" in fluid_type:
            self.molarity = 2.0 # Moles/Liter (Assumed concentration)
            self.density = 1100.0 # kg/m3 approx
        else:
            self.molarity = 0.0 # Water
            self.density = 1000.0
            
    def calculate_flow_rate(self, valve_open_pct: float) -> float:
        """
        Calculates gravity flow rate down the shaft using Manning's Equation.
        Returns Flow Rate in Liters/minute.
        """
        if valve_open_pct <= 0:
            return 0.0
            
        # Manning's Equation: V = (k/n) * Rh^(2/3) * S^(1/2)
        # n (roughness) ~ 0.015 for lined stone
        n = 0.015
        
        # Hydraulic Radius (Rh)
        # Assume flow depth proportional to valve? 
        # Simplified: Valve limits the effective Area.
        # Area = W * H * (valve/100)
        # But Manning depends on wetted perimeter. 
        # Let's simplify: Calculate MAX flow, then scale by valve %.
        
        area_full = self.width * self.height
        perimeter_full = 2 * (self.width + self.height)
        rh_full = area_full / perimeter_full
        
        # Slope (S) = sin(angle)
        slope = np.sin(np.radians(self.angle))
        
        # Velocity (Full)
        velocity = (1.0 / n) * (rh_full ** (2/3)) * (slope ** 0.5)
        
        # Max Flow (m3/s)
        q_max = velocity * area_full
        
        # Valve scaling (Linear assumption for control)
        q_actual = q_max * (valve_open_pct / 100.0)
        
        # Convert to L/min
        # 1 m3/s = 60,000 L/min
        return q_actual * 60000.0
        
    def calculate_hydrogen_yield(self, flow_rate_l_min: float) -> dict:
        """
        Calculates H2 gas generation from the chemical flow.
        Zn + H2SO4 -> ZnSO4 + H2
        Stoichiometry: 1 Mole Acid -> 1 Mole H2 Gas.
        """
        if self.molarity == 0:
            return {"h2_rate_l_min": 0.0, "reaction": "None (Water)"}
            
        # Moles of Acid per minute
        moles_acid_min = flow_rate_l_min * self.molarity
        
        # Moles of H2 Gas (1:1 ratio)
        moles_gas_min = moles_acid_min
        
        # Volume of Gas at STP (1 mole = 22.4 Liters)
        # Assuming King's Chamber pressure might compress it, but standard flow:
        h2_vol_l_min = moles_gas_min * 22.4
        
        return {
            "h2_rate_l_min": h2_vol_l_min,
            "reaction": "Zn + H2SO4 -> H2 (Active)"
        }

