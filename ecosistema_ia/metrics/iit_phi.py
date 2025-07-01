"""Utilities for computing integrated information (Φ) in agent clusters."""

from itertools import combinations
from typing import List, Dict

# Placeholder algorithm for calculating integrated information.
# Real IIT calculations would require the PyPhi library and a model of
# agent connectivity/state transitions. For testing purposes we compute a
# simple connectivity based on spatial distance.

def calculate_phi_for_agent_cluster(agents: List) -> Dict[str, float]:
    """Return a rudimentary Φ estimate for a group of agents.

    The current implementation measures the ratio of close connections
    between agents in the same z-layer. It serves as a lightweight
    stand-in when PyPhi is unavailable.
    """
    n = len(agents)
    if n < 2:
        return {"phi": 0.0}

    connected = 0
    for a, b in combinations(agents, 2):
        if a.z == b.z and abs(a.x - b.x) <= 1 and abs(a.y - b.y) <= 1:
            connected += 1

    possible = n * (n - 1) / 2
    phi_value = connected / possible if possible else 0.0
    return {"phi": phi_value}


__all__ = ["calculate_phi_for_agent_cluster"]
