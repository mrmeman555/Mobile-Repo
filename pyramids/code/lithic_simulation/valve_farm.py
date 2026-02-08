import numpy as np

class LabyrinthManifold:
    def __init__(self, chamber_count: int = 3000, baffle_complexity: float = 0.5):
        """
        baffle_complexity: 0.0 (Open Hall) to 1.0 (Mataha Maze).
        """
        self.chambers = chamber_count
        self.baffles = baffle_complexity 
        
    def calculate_flow_dynamics(self, input_pressure_bar: float, valve_open_pct: float, brine_resistance: float = 150.0) -> dict:
        """
        Models flow through the Euler Grid.
        brine_resistance: Lower (Saltier) = Better Corrosion Resistance (Per triad notes).
        """
        if valve_open_pct <= 0:
            return {
                "flow_rate_m3_s": 0.0,
                "resistance_dynamic": float('inf'),
                "turbulence_index": 0.0,
                "stability_factor": 0.0,
                "euler_chi": 1,
                "active_chambers": 0,
                "status": "CLOSED"
            }
            
        # 1. Euler Characteristic (Simplified Topology)
        # Chi = V - E + F. High complexity (more baffles) increases effective Chi for damping.
        # We treat 'baffles' as increasing the topological 'genus' or complexity.
        euler_chi = int(self.chambers * (0.1 + self.baffles))
        
        # 2. Resistance & Flow
        r_valves = 1.0 / (valve_open_pct / 100.0) 
        r_topology = 1.0 + (self.baffles * 5.0) # Baffles add resistance
        total_resistance = r_valves * r_topology
        
        flow_rate = input_pressure_bar / total_resistance
        
        # 3. Turbulence Damping (The Baffle Effect)
        # Raw turbulence scales with Flow Rate
        raw_turbulence = flow_rate * 0.8
        
        # --- PHYSICS FIX: BOOST DAMPING POWER ---
        # Changed divisor from 500.0 to 100.0 to reflect Herodotus-scale efficiency
        damping_factor = 1.0 + (euler_chi / 100.0) 
        
        residual_turbulence = raw_turbulence / damping_factor
        
        # 4. Brine Corrosion Factor (Triad Uplift)
        # High Brine (Low Resistance) = electrochemical protection -> Higher stability cap
        # Resistance 150 (Fresh) -> Factor 0.8
        # Resistance 0.1 (Nexus) -> Factor 1.0
        corrosion_stability = 1.0 - (min(brine_resistance, 150.0) / 750.0) # Max 20% penalty for fresh water
        
        # 5. Final Stability
        # Inverse of turbulence, scaled by corrosion factor
        stability = (1.0 / (1.0 + residual_turbulence)) * corrosion_stability
        stability = np.clip(stability, 0.0, 1.0)
        
        status = "STABLE"
        if stability < 0.8:
            status = "TURBULENT"
        if stability < 0.4:
            status = "CRITICAL"
            
        return {
            "flow_rate_m3_s": flow_rate,
            "resistance_dynamic": total_resistance,
            "turbulence_index": residual_turbulence,
            "stability_factor": stability,
            "euler_chi": euler_chi,
            "active_chambers": int(self.chambers * (valve_open_pct/100.0)),
            "status": status
        }
