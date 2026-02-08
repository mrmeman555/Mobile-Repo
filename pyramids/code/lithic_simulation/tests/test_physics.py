import pytest
import math
from lithic_simulation.acoustics import ResonantChamber
from lithic_simulation.piezo import PiezoGenerator
from lithic_simulation import config

def test_helmholtz_neck():
    """
    Verify Helmholtz calculation against a known physics example.
    """
    chamber = ResonantChamber(1, 1, 1) # Volume 1m^3
    chamber.volume = 0.001 # Override volume to 1 Liter
    
    target_f = 73.7
    neck_area = 0.0001
    
    calculated_l = chamber.calculate_helmholtz_neck_length(neck_area, target_f)
    
    # Expected physical length was 0.05m
    assert calculated_l == pytest.approx(0.05, abs=0.01)

def test_piezo_zero_voltage():
    """
    Verify that 0 dB (20 microPascals) produces the expected minimal voltage.
    V_single = g33 * eff * P * th
    V_single = 0.05 * 0.5 * 20e-6 * 2.0 = 1.0e-6 Volts
    
    BUT we now have 9 beams by default in simulate_voltage_sweep.
    V_total = V_single * 9 = 9.0e-6 Volts.
    """
    piezo = PiezoGenerator()
    # Note: default beam_count is 9
    df = piezo.simulate_voltage_sweep(0, 0, 0.5, 2.0)
    voltage = df['voltage'].iloc[0]
    assert voltage == pytest.approx(9.0e-6, rel=1e-3)

def test_room_modes():
    """Verify axial mode calculation for a simple 10m room."""
    # f = c / 2L = 343 / 20 = 17.15 Hz
    chamber = ResonantChamber(10.0, 10.0, 10.0)
    modes = chamber.calculate_room_modes(max_order=1)
    
    expected_freq = 343.0 / 20.0
    assert modes['x'][0] == pytest.approx(expected_freq)

def test_granite_constants():
    """Verify constants are loaded correctly."""
    assert config.SPEED_OF_SOUND_GRANITE == 5950.0
