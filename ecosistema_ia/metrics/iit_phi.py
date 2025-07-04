"""Utilities for computing integrated information (Φ) in agent clusters."""

from collections import deque
from typing import Dict, List


def _adjacency_matrix(agents: List) -> List[List[int]]:
    """Return adjacency matrix based on proximity in the same z-layer."""
    n = len(agents)
    matrix = [[0] * n for _ in range(n)]
    for i, a in enumerate(agents):
        for j, b in enumerate(agents[i + 1 :], start=i + 1):
            if a.z == b.z and abs(a.x - b.x) <= 1 and abs(a.y - b.y) <= 1:
                matrix[i][j] = matrix[j][i] = 1
    return matrix


def _shortest_paths(adj: List[List[int]], start: int) -> List[int]:
    """Breadth-first search distances from a node."""
    n = len(adj)
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    while queue:
        i = queue.popleft()
        for j, linked in enumerate(adj[i]):
            if linked and dist[j] == -1:
                dist[j] = dist[i] + 1
                queue.append(j)
    return dist


def calculate_phi_for_agent_cluster(agents: List) -> Dict[str, float]:
    """Estimate Φ using network efficiency over agent connections."""

    n = len(agents)
    if n < 2:
        return {"phi": 0.0}

    adj = _adjacency_matrix(agents)
    efficiency = 0.0
    for i in range(n):
        dist = _shortest_paths(adj, i)
        for j in range(i + 1, n):
            d = dist[j]
            if d > 0:
                efficiency += 1 / d
    possible = n * (n - 1) / 2
    phi_value = efficiency / possible if possible else 0.0
    return {"phi": phi_value}


__all__ = ["calculate_phi_for_agent_cluster"]
