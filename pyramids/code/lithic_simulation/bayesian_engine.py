import pandas as pd
import numpy as np

class BayesianSiege:
    def __init__(self):
        # Evidence Library
        # Updated for v3.0 with H0, H1, H2 K-factors
        # H0 = Primitive (Baseline, K=1 relative to itself)
        # H1 = Advanced Machine
        # H2 = Hybrid / Lost Tech
        
        self.evidence_library = {
            "Saqqara Vases": {
                "desc": "40,000 stone vessels with <0.001 inch tolerance.",
                "hard_data": "Tolerance: < 0.001 inch (High RPM Lathe Markings)",
                "k_factor": 100.0, # Legacy/H1
                "k_min": 50.0,
                "k_max": 200.0,
                "k_H0": 1.0,
                "k_H1": 100.0,
                "k_H2": 10.0,
                "category": "Manufacturing"
            },
            "Granite Core #7": {
                "desc": "0.1 inch/rev feed rate (Impossible for copper saws).",
                "hard_data": "Feed Rate: 0.100 inch per revolution (Petrie Measurement)",
                "k_factor": 500.0,
                "k_min": 200.0,
                "k_max": 1000.0,
                "k_H0": 1.0,
                "k_H1": 500.0,
                "k_H2": 25.0,
                "category": "Manufacturing"
            },
            "Serapeum Flatness": {
                "desc": "Optically flat surfaces (2/10,000 inch error).",
                "hard_data": "Tolerance: < 0.0002 inch (5 microns) over 100 tons",
                "k_factor": 200.0,
                "k_min": 100.0,
                "k_max": 400.0,
                "k_H0": 1.0,
                "k_H1": 200.0,
                "k_H2": 15.0,
                "category": "Precision"
            },
            "Giza Resonance": {
                "desc": "Chamber tuned to 117 Hz (F#) standing wave.",
                "hard_data": "Frequency: 117 Hz (F#) - Matches 432 Hz Temperament",
                "k_factor": 50.0,
                "k_min": 20.0,
                "k_max": 100.0,
                "k_H0": 1.0,
                "k_H1": 50.0,
                "k_H2": 5.0,
                "category": "Acoustics"
            },
            "Big Void Resonance": {
                "desc": "30m Void creates 1:20 harmonic step-down.",
                "hard_data": "Frequency: 5.72 Hz (1/20th of 117 Hz) - Harmonic Lock",
                "k_factor": 100.0,
                "k_min": 40.0,
                "k_max": 250.0,
                "k_H0": 1.0,
                "k_H1": 100.0,
                "k_H2": 8.0,
                "category": "Acoustics"
            },
            "Hawara Monolith": {
                "desc": "110-ton Quartzite Pressure Vessel geometry.",
                "hard_data": "Weight: 110 Tons - Single Cut Quartzite Monolith",
                "k_factor": 100.0,
                "k_min": 50.0,
                "k_max": 200.0,
                "k_H0": 1.0,
                "k_H1": 100.0,
                "k_H2": 10.0,
                "category": "Engineering"
            }
        }

    def _calculate_effective_k(self, k_raw: float, credibility: float) -> float:
        """Applies Credibility Weighting: K_eff = 1 + c * (K - 1)"""
        return 1.0 + credibility * (k_raw - 1.0)

    def run_siege(self, prior_prob: float, active_evidence: list, 
                  use_correlation: bool = True, 
                  credibility_map: dict = None,
                  graph = None,
                  active_models: list = None) -> pd.DataFrame:
        """
        v3.0 Bayesian Engine Update.
        Supports Multi-Model, Credibility, Causal Graph, and Correlation Damping.
        """
        if active_models is None: active_models = ["H1"]
        if credibility_map is None: credibility_map = {}
        
        # Initialize Priors
        # Normalize priors across active models + H0
        # We assume H0 is always implicit baseline if not explicitly modeled, but here we track explicit probs.
        # Logic: prior_prob is P(H1).
        # Remainder (1 - P(H1)) is distributed to H0 and H2 (if active).
        
        probs = {}
        probs["H1"] = prior_prob
        
        remainder = 1.0 - prior_prob
        other_models = [m for m in ["H0", "H2"] if m in active_models or m == "H0"]
        
        # Ensure H0 is always tracked for Odds calculation relative to it
        if "H0" not in other_models: other_models.append("H0")
            
        if not other_models:
            # Should not happen if H0 implied
             probs["H0"] = remainder
        else:
            split = remainder / len(other_models)
            for m in other_models:
                probs[m] = split
                
        # Convert to Odds relative to H0 (Baseline)
        # O_i = P(Hi) / P(H0)
        # O_0 = 1.0
        
        odds = {m: probs[m] / probs["H0"] for m in probs}
        
        steps = []
        
        # Initial Step
        steps.append({
            "Step": "Prior",
            "Description": "Initial Belief",
            "K_Factor": 1.0,
            "Probability_Pct": probs["H1"] * 100,
            **{f"Prob_{m}": probs.get(m, 0)*100 for m in ["H0", "H1", "H2"]}
        })
        
        # Correlation Logic (Pre-calc effective K for H1)
        # Note: Correlation currently only implemented for H1 damping logic in original spec.
        # v3.0: We apply damping to the K-factors of all models? 
        # Original spec: "Use geometric mean... Apply that once per category".
        # We will apply this to the K-factor values for each model.
        
        # Map Category -> Effective K per Model
        cat_eff_ks = {m: {} for m in odds}
        
        if use_correlation:
            cat_groups = {m: {} for m in odds}
            
            for key in active_evidence:
                if key in self.evidence_library:
                    cat = self.evidence_library[key]["category"]
                    ev_data = self.evidence_library[key]
                    
                    for m in odds:
                        k_key = f"k_{m}"
                        k_val = ev_data.get(k_key, 1.0 if m == "H0" else ev_data["k_factor"])
                        
                        if cat not in cat_groups[m]: cat_groups[m][cat] = []
                        cat_groups[m][cat].append(k_val)
            
            for m in odds:
                for cat, ks in cat_groups[m].items():
                    if ks:
                        prod = np.prod(ks)
                        cat_eff_ks[m][cat] = prod ** (1.0/len(ks))

        seen_categories = set()
        current_posteriors = {key: 0.0 for key in active_evidence} # For Graph
        
        for key in active_evidence:
            if key not in self.evidence_library: continue
            
            ev = self.evidence_library[key]
            cat = ev["category"]
            cred = credibility_map.get(key, 1.0)
            
            # Determine Base K for each model
            step_ks = {}
            
            for m in odds:
                k_key = f"k_{m}"
                raw_k = ev.get(k_key, 1.0 if m == "H0" else ev["k_factor"])
                
                # 1. Correlation Damping
                if use_correlation:
                    if cat in seen_categories:
                        k_base = 1.0
                    else:
                        k_base = cat_eff_ks[m].get(cat, raw_k)
                else:
                    k_base = raw_k
                    
                # 2. Credibility Weighting
                k_cred = self._calculate_effective_k(k_base, cred)
                
                # 3. Causal Graph
                if graph:
                    # Use posterior of H1 from previous step for graph influence?
                    # Spec: "Use posterior probability from previous steps."
                    # Which posterior? Probably the "Machine Hypothesis" (H1).
                    # We track evidence 'occurrence' posteriors? 
                    # No, graph implies "Evidence A increases prob of Evidence B".
                    # Graph modifier: 1 + sum(parent_posteriors * weight)
                    # Wait, parent_posterior refers to the probability of the HYPOTHESIS after Parent evidence?
                    # Or probability of the PARENT EVIDENCE being true?
                    # In this engine, we assume evidence IS true (observed).
                    # Interpreting spec: "parent_posteriors" likely means the H1 probability *after* the parent step.
                    # Let's use the H1 probability from the last step.
                    
                    # Actually, the graph usually models dependency between evidence nodes.
                    # "Serapeum Flatness -> Giza Resonance".
                    # If Saqqara Vases (Parent) happened, does it make Granite Core (Child) more likely?
                    # The implementation requested: "K_modified = K_effective * (1 + Σ(parent_posteriors * edge_weight))"
                    # "parent_posteriors" is ambiguous.
                    # I will use the H1 Probability from the *previous step* in the chain.
                    # But the graph is defined on Evidence Keys.
                    # So I need to map Evidence Key -> Step Index -> Posterior?
                    # No, graph edges are Evidence -> Evidence.
                    # So I look up if Parent Evidence has been processed.
                    # If so, what was the H1 Posterior *at that step*?
                    
                    modifier = graph.get_influence_modifier(key, current_posteriors)
                    k_final = k_cred * modifier
                else:
                    k_final = k_cred
                    
                step_ks[m] = k_final
            
            if use_correlation: seen_categories.add(cat)
            
            # Update Odds
            for m in odds:
                odds[m] *= step_ks[m]
                
            # Normalize Probabilities
            total_odds = sum(odds.values())
            current_probs = {m: odds[m] / total_odds for m in odds}
            
            # Store H1 posterior for Graph
            current_posteriors[key] = current_probs["H1"]
            
            step_data = {
                "Step": key,
                "Description": ev["desc"],
                "K_Factor": step_ks["H1"], # Show H1 K for continuity
                "Probability_Pct": current_probs["H1"] * 100,
                **{f"Prob_{m}": current_probs.get(m, 0)*100 for m in ["H0", "H1", "H2"]}
            }
            steps.append(step_data)
            
        return pd.DataFrame(steps)

    def run_monte_carlo(self, prior_prob: float, active_evidence: list, 
                        samples: int = 1000, 
                        use_correlation: bool = True,
                        credibility_map: dict = None,
                        graph = None,
                        active_models: list = None) -> dict:
        
        if active_models is None: active_models = ["H1"]
        if credibility_map is None: credibility_map = {}
        
        final_probs_h1 = []
        
        # Metadata
        ev_meta = [self.evidence_library[k] for k in active_evidence if k in self.evidence_library]
        
        # Base Odds (Same initialization as run_siege)
        # Simplified for MC: Just tracking H1 vs H0 for the distribution unless Multi-model requested
        # Prompt says "Produce a distribution of final posterior probabilities."
        # Usually refers to H1.
        
        # Initialize Priors logic again
        remainder = 1.0 - prior_prob
        other_models = [m for m in ["H0", "H2"] if m in active_models or m == "H0"]
        if "H0" not in other_models: other_models.append("H0")
        
        probs_init = {"H1": prior_prob}
        if not other_models: probs_init["H0"] = remainder
        else:
            split = remainder / len(other_models)
            for m in other_models: probs_init[m] = split
            
        odds_init = {m: probs_init[m] / probs_init["H0"] for m in probs_init}

        for _ in range(samples):
            run_odds = odds_init.copy()
            
            # Sample Ks
            # 1. Sample raw K for H1 (and H2)
            # Use loguniform
            
            sampled_ks_h1 = []
            
            # Correlation grouping per sample
            cat_groups_h1 = {}
            
            for i, ev in enumerate(ev_meta):
                key = active_evidence[i]
                cred = credibility_map.get(key, 1.0)
                
                # Sample H1 K
                k_min = ev.get("k_min", ev["k_factor"] * 0.5)
                k_max = ev.get("k_max", ev["k_factor"] * 2.0)
                log_k = np.random.uniform(np.log(k_min), np.log(k_max))
                k_raw_h1 = np.exp(log_k)
                
                # Apply Credibility
                k_cred_h1 = self._calculate_effective_k(k_raw_h1, cred)
                
                # Store for correlation
                if use_correlation:
                    cat = ev["category"]
                    if cat not in cat_groups_h1: cat_groups_h1[cat] = []
                    cat_groups_h1[cat].append(k_cred_h1)
                else:
                    run_odds["H1"] *= k_cred_h1
                    
                # Handle H2/H0 if needed (Simplified: Fix H2 relative to sampled H1? Or independent?)
                # For MC, let's just vary H1 to show uncertainty in "Machine Hypothesis" strength.
                # H0 stays 1. H2 stays fixed ratio? 
                # Let's assume H2 also varies similarly or stays fixed. 
                # Fix H2 for speed/simplicity unless required.
                if "H2" in run_odds:
                    k_raw_h2 = ev.get("k_H2", 10.0)
                    k_cred_h2 = self._calculate_effective_k(k_raw_h2, cred)
                    run_odds["H2"] *= k_cred_h2

            if use_correlation:
                # Apply effective Ks
                for cat, ks in cat_groups_h1.items():
                    prod = np.prod(ks)
                    eff_k = prod ** (1.0/len(ks))
                    run_odds["H1"] *= eff_k
            
            # Normalize
            total = sum(run_odds.values())
            final_probs_h1.append(run_odds["H1"] / total)
            
        arr = np.array(final_probs_h1)
        return {
            "final_probs": arr,
            "mean": np.mean(arr),
            "median": np.median(arr),
            "p025": np.percentile(arr, 2.5),
            "p975": np.percentile(arr, 97.5)
        }

    def find_minimum_k_to_reach(self, target_prob: float, active_evidence: list, prior_prob: float) -> pd.DataFrame:
        """
        Reverse Inference: Solves for min K required for each evidence item 
        to reach target_prob, assuming all OTHER evidence is held constant.
        """
        # Base Odds without any evidence
        base_odds = prior_prob / (1.0 - prior_prob)
        target_odds = target_prob / (1.0 - target_prob)
        
        # Run full chain to get current Total K
        full_run = self.run_siege(prior_prob, active_evidence, use_correlation=False) # Simplification
        # Total K = Final Odds / Base Odds
        current_final_prob = full_run.iloc[-1]["Probability_Pct"] / 100.0
        current_final_odds = current_final_prob / (1.0 - current_final_prob)
        total_k_system = current_final_odds / base_odds
        
        results = []
        
        for key in active_evidence:
            if key not in self.evidence_library: continue
            
            ev = self.evidence_library[key]
            current_k = ev["k_factor"]
            
            # K_others = K_total / K_this
            k_others = total_k_system / current_k
            
            # O_target = O_base * K_others * K_req
            # K_req = O_target / (O_base * K_others)
            
            if base_odds * k_others == 0:
                k_req = 0 # Impossible
            else:
                k_req = target_odds / (base_odds * k_others)
                
            results.append({
                "Evidence": key,
                "Current K": current_k,
                "Required K": k_req,
                "Delta": k_req - current_k
            })
            
        return pd.DataFrame(results)

    def sensitivity_analysis(self, prior_prob: float, active_evidence: list) -> pd.DataFrame:
        """
        Calculates P_with and P_without for each item.
        """
        # Baseline
        base_run = self.run_siege(prior_prob, active_evidence)
        p_with = base_run.iloc[-1]["Probability_Pct"]
        
        results = []
        for key in active_evidence:
            # Run without this key
            subset = [k for k in active_evidence if k != key]
            if not subset:
                p_without = prior_prob * 100
            else:
                run_wo = self.run_siege(prior_prob, subset)
                p_without = run_wo.iloc[-1]["Probability_Pct"]
                
            results.append({
                "Evidence": key,
                "P_with": p_with,
                "P_without": p_without,
                "Delta P": p_with - p_without
            })
            
        return pd.DataFrame(results)
