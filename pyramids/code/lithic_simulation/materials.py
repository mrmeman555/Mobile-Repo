from dataclasses import dataclass
try:
from . import config
except ImportError:
    import config

@dataclass
class GraniteBeam:
    length: float
    width: float
    height: float
    quartz_percentage: float = 0.30

    @property
    def volume(self) -> float:
        return self.length * self.width * self.height

    def calculate_mass(self) -> float:
        """Returns mass in kg based on Granite density."""
        return self.volume * config.GRANITE_DENSITY

    def calculate_static_stress(self, load_mass_kg: float) -> float:
        """
        Calculates static stress (Pressure) in Pascals (N/m^2).
        Force = Mass * Gravity (9.81)
        """
        area = self.length * self.width
        force = load_mass_kg * 9.81
        return force / area
