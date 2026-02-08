class EvidenceGraph:
    def __init__(self):
        self.edges = {}  # Child -> [(Parent, Weight)]
        
        # Define static graph structure
        # Saqqara Vases -> Granite Core #7 (0.3)
        # Granite Core #7 -> Serapeum Flatness (0.6)
        # Serapeum Flatness -> Giza Resonance (0.5)
        self.add_edge("Saqqara Vases", "Granite Core #7", 0.3)
        self.add_edge("Granite Core #7", "Serapeum Flatness", 0.6)
        self.add_edge("Serapeum Flatness", "Giza Resonance", 0.5)

    def add_edge(self, parent: str, child: str, weight: float):
        if child not in self.edges:
            self.edges[child] = []
        self.edges[child].append((parent, weight))

    def get_influence_modifier(self, child: str, current_posteriors: dict) -> float:
        """
        Calculates the modifier: 1 + Σ(parent_posterior * edge_weight)
        current_posteriors: dict mapping Evidence Key -> Current Probability (0-1)
        """
        if child not in self.edges:
            return 1.0
            
        total_influence = 0.0
        for parent, weight in self.edges[child]:
            # Use parent's posterior if available (it should be if order matches)
            # If parent hasn't been evaluated or isn't in chain, assume 0 influence?
            # Or assume prior? "Use posterior probability from previous steps."
            # If parent is not in active evidence, its posterior is effectively the Prior? 
            # Or 0 (not proven)?
            # I'll assume if parent is in current_posteriors, use it. Else 0.
            parent_prob = current_posteriors.get(parent, 0.0)
            total_influence += parent_prob * weight
            
        return 1.0 + total_influence

