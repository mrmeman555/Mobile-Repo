import numpy as np
import pandas as pd

class CascadeDynamics:
    def __init__(self):
        self.base_efficiency = 0.95
        
    def simulate_transients(self, steps: int, brine_conductivity: float, hurst: float = 0.7) -> pd.DataFrame:
        """
        Simulates system power output over time with Hurst-exponent noise.
        """
        # Noise Generation
        noise = np.random.normal(0, 0.1, steps)
        
        # Brine Damping (Conductivity acts as stabilizer)
        damping = 1.0 + (brine_conductivity * 0.5)
        damped_noise = noise / damping
        
        # Signal Construction
        time = np.arange(steps)
        # Random Walk with Drift (Hurst proxy)
        signal = 100.0 + (np.cumsum(damped_noise) * 5.0)
        
        # Floods (Poisson)
        spikes = np.random.poisson(0.05, steps) * 20.0
        signal += spikes
        
        # Clip and return
        signal = np.clip(signal, 0, 200)
        
        # Stability Metric: Inverse of Coefficient of Variation
        # High Mean, Low Std => High Stability
        if np.std(signal) == 0:
            stability = 10.0
        else:
            stability = np.mean(signal) / (np.std(signal) * 10.0)
        
        stability = min(stability, 1.0)
        
        return pd.DataFrame({
            "Time_Step": time,
            "Power_Output_MW": signal,
            "Noise_Level": damped_noise,
            "Stability_Index": stability
        })

    def run_ensemble(self, runs: int, steps: int, brine_conductivity: float, hurst: float, laschamp_pct: float) -> dict:
        """
        Monte Carlo Ensemble Runner for Stability Analysis.
        """
        uptime_scores = []
        stability_scores = []
        
        for _ in range(runs):
            # 1. Transient Sim
            df = self.simulate_transients(steps, brine_conductivity, hurst)
            # Take the stability index from the run
            stab_scalar = df["Stability_Index"].iloc[0] # They are all same in the DF column? No, it's scalar in DF.
            stability_scores.append(stab_scalar)
            
            # 2. Laschamp Stress (Scalar calc)
            stress = self.laschamp_stress_test(laschamp_pct, brine_conductivity)
            uptime_scores.append(stress['uptime_pct'])
            
        # Stats
        uptimes = np.array(uptime_scores)
        stabilities = np.array(stability_scores)
        
        return {
            "uptime_mean": np.mean(uptimes),
            "uptime_p95": np.percentile(uptimes, 5.0), # Conservative 95% (lower bound)
            "stability_mean": np.mean(stabilities),
            "stability_std": np.std(stabilities),
            "distribution": uptimes # Return full array for histogram
        }

    def laschamp_stress_test(self, field_strength_pct: float, brine_conductivity: float) -> dict:
        """
        Calculates efficiency during Geomagnetic Collapse.
        """
        field_factor = (field_strength_pct / 100.0) ** 2
        
        # Brine Compensation
        brine_factor = min(brine_conductivity / 20.0, 0.9)
        
        # Perturbation: Add random variance to the stress test for MC
        variance = np.random.normal(0, 0.05)
        
        final_efficiency = field_factor + (brine_factor * (1.0 - field_factor)) + variance
        final_efficiency = np.clip(final_efficiency, 0.0, 1.0)
        
        uptime = final_efficiency * 100.0
        
        return {
            "net_efficiency": final_efficiency,
            "uptime_pct": uptime,
            "status": "STABLE" if uptime > 80 else "CRITICAL"
        }

class HBMStability:
    """
    Hierarchical Bayesian Model for System Coherence.
    Uses Conjugate Priors (Gaussian-Gaussian) to fuse module outputs.
    """
    def __init__(self):
        # Prior: The system is generally stable (Mean=0.8, Precision=10)
        self.prior_mean = 0.8
        self.prior_precision = 10.0 # Precision = 1/Variance
        
    def fuse_inputs(self, resonance_score: float, hydraulic_score: float, brine_score: float) -> dict:
        """
        Fuses scores (0.0 - 1.0) from Giza, Hawara, and Network.
        """
        # Likelihoods from subsystems
        # We treat each module's score as an observation of the "True System Health"
        # Obs ~ N(TrueHealth, Sigma)
        # Assume modules have varying reliability (Precision)
        
        obs = [
            (resonance_score, 20.0), # Giza (High Precision)
            (hydraulic_score, 15.0), # Hawara (Med Precision)
            (brine_score, 5.0)       # Brine (Variable/Low Precision context)
        ]
        
        # Gaussian Update
        # Mean_post = (PriorMean*PriorPrec + Sum(Obs * ObsPrec)) / (PriorPrec + Sum(ObsPrec))
        # Prec_post = PriorPrec + Sum(ObsPrec)
        
        numerator = (self.prior_mean * self.prior_precision)
        denominator = self.prior_precision
        
        for val, prec in obs:
            numerator += val * prec
            denominator += prec
            
        post_mean = numerator / denominator
        post_std = np.sqrt(1.0 / denominator)
        
        return {
            "coherence_mean": post_mean,
            "coherence_std": post_std,
            "coherence_95_ci": [post_mean - 1.96*post_std, post_mean + 1.96*post_std],
            "status": "OPTIMAL" if post_mean > 0.85 else "NOMINAL" if post_mean > 0.7 else "DEGRADED"
        }
