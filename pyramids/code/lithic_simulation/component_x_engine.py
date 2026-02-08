import math

class ArkCapacitor:
    def __init__(self, cubit_length_inches: float = 20.61, plate_separation_mm: float = 10.0):
        self.cubit = cubit_length_inches
        self.separation_m = plate_separation_mm / 1000.0
        
        # Ark Dimensions (Exodus 25:10) in Cubits
        # 2.5 long x 1.5 wide x 1.5 high
        self.ark_dims_cubits = {'L': 2.5, 'W': 1.5, 'H': 1.5}
        
        # Coffer Dimensions (Petrie) in Inches
        # Inner dimensions are key for fit
        self.coffer_dims_inches = {'L': 78.06, 'W': 26.81, 'H': 34.42}
        
    def get_ark_dimensions_inches(self):
        return {
            'L': self.ark_dims_cubits['L'] * self.cubit,
            'W': self.ark_dims_cubits['W'] * self.cubit,
            'H': self.ark_dims_cubits['H'] * self.cubit
        }
        
    def check_mechanical_fit(self) -> dict:
        ark = self.get_ark_dimensions_inches()
        coffer = self.coffer_dims_inches
        
        # Calculate gaps (Clearance)
        gap_L = coffer['L'] - ark['L']
        gap_W = coffer['W'] - ark['W']
        # Height is less critical for "fitting inside" as long as it's not taller than the room, 
        # but typically we compare against Coffer Depth if it's meant to sit "in" it.
        # Petrie's 34.42 is height.
        gap_H = coffer['H'] - ark['H'] 
        
        # Docking Logic: Must fit in L and W. 
        # "Precision Docking Fit" if Clearance is positive but < 1.0 inch
        
        fits_L = gap_L > 0
        fits_W = gap_W > 0
        
        # Check if fit is "Precision" (Tight)
        # Usually Width is the tightest dimension
        is_precision = (0 < gap_W < 1.0)
        
        status = "NO FIT (TOO LARGE)"
        if fits_L and fits_W:
            if is_precision:
                status = "PRECISION DOCKING FIT"
            else:
                status = "LOOSE FIT"
                
        return {
            'ark_dims': ark,
            'coffer_dims': coffer,
            'gaps': {'L': gap_L, 'W': gap_W, 'H': gap_H},
            'status': status,
            'is_precision': is_precision
        }

    def calculate_capacitance(self, voltage_kv: float = 400.0) -> dict:
        # Parallel Plate Capacitor
        # C = k * e0 * A / d
        # Area: Exodus describes overlaying "inside and out". 
        # We treat it as a box capacitor.
        # Surface Area approx = 2 * (L*W + L*H + W*H)
        
        ark = self.get_ark_dimensions_inches()
        L_m = ark['L'] * 0.0254
        W_m = ark['W'] * 0.0254
        H_m = ark['H'] * 0.0254
        
        # External Surface Area (m^2)
        surface_area_m2 = 2 * (L_m * W_m + L_m * H_m + W_m * H_m) 
        
        k_acacia = 2.5
        epsilon_0 = 8.854e-12
        
        # C = (k * e0 * A) / d
        if self.separation_m <= 0:
            capacitance_f = 0.0
        else:
            capacitance_f = (k_acacia * epsilon_0 * surface_area_m2) / self.separation_m
        
        # Energy U = 0.5 * C * V^2
        voltage_v = voltage_kv * 1000.0
        energy_j = 0.5 * capacitance_f * (voltage_v ** 2)
        
        # Charge Q = C * V
        charge_c = capacitance_f * voltage_v
        
        return {
            'capacitance_nf': capacitance_f * 1e9,
            'energy_joules': energy_j,
            'charge_coulombs': charge_c,
            'surface_area_m2': surface_area_m2
        }

