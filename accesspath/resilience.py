"""Loopless route alternatives and closure-aware rerouting."""

from __future__ import annotations

from dataclasses import replace
import heapq
from .router import Constraints, NoRoute, route


def close_edges(graph, closures):
    """Return a new graph; closure pairs are directed, so callers choose both ways."""
    closures = set(map(tuple, closures))
    for pair in closures:
        if (
            len(pair) != 2
            or pair[0] not in graph
            or not any(edge.to == pair[1] for edge in graph[pair[0]])
        ):
            raise ValueError(f"unknown closure edge: {pair}")
    return {
        node: [
            replace(edge, closed=True) if (node, edge.to) in closures else edge
            for edge in edges
        ]
        for node, edges in graph.items()
    }


def _path_result(graph, nodes, constraints):
    # Every pair came from a permitted edge. Reconstruct its direct edge cost,
    # rather than allowing the leg solver to take an unrelated indirect path.
    distance = cost = 0.0
    features = []
    for start, end in zip(nodes, nodes[1:]):
        edges = [
            edge
            for edge in graph[start]
            if edge.to == end
            and not edge.closed
            and edge.surface <= constraints.max_surface
            and not (constraints.avoid_stairs and edge.kind == "stairs")
            and not (constraints.avoid_elevators and edge.kind == "elevator")
        ]
        edge = min(
            edges,
            key=lambda item: constraints.distance_weight * item.distance
            + constraints.difficulty_weight * item.surface,
        )
        distance += edge.distance
        cost += (
            constraints.distance_weight * edge.distance
            + constraints.difficulty_weight * edge.surface
        )
        features.append(edge.kind)
    return {
        "nodes": nodes,
        "distance": round(distance, 3),
        "cost": round(cost, 3),
        "features": features,
        "explanation": "Loopless alternative satisfying all selected constraints",
    }


def route_alternatives(graph, start, end, constraints=Constraints(), count=3):
    """Yen-style spur enumeration over node-distinct paths, bounded to ten outputs."""
    if type(count) is not int or not 1 <= count <= 10:
        raise ValueError("count must be 1..10")
    first = route(graph, start, end, constraints)
    accepted = [first]
    candidates = []
    discovered = {tuple(first["nodes"])}
    while len(accepted) < count:
        previous = accepted[-1]["nodes"]
        for index in range(len(previous) - 1):
            root = previous[: index + 1]
            removed_nodes = set(root[:-1])
            excluded = {
                (item["nodes"][index], item["nodes"][index + 1])
                for item in accepted
                if len(item["nodes"]) > index + 1 and item["nodes"][: index + 1] == root
            }
            spur_graph = {
                node: [
                    edge
                    for edge in edges
                    if edge.to not in removed_nodes and (node, edge.to) not in excluded
                ]
                for node, edges in graph.items()
                if node not in removed_nodes
            }
            try:
                spur = route(spur_graph, root[-1], end, constraints)
            except NoRoute:
                continue
            nodes = root[:-1] + spur["nodes"]
            key = tuple(nodes)
            if key in discovered:
                continue
            discovered.add(key)
            result = _path_result(graph, nodes, constraints)
            heapq.heappush(candidates, (result["cost"], key, result))
        if not candidates:
            break
        accepted.append(heapq.heappop(candidates)[2])
    return [
        {
            **item,
            "rank": index + 1,
            "extra_distance": round(item["distance"] - first["distance"], 3),
        }
        for index, item in enumerate(accepted)
    ]


def reroute(graph, start, end, closures, constraints=Constraints()):
    baseline = route(graph, start, end, constraints)
    updated = close_edges(graph, closures)
    try:
        replacement = route(updated, start, end, constraints)
    except NoRoute:
        return {
            "reachable": False,
            "baseline": baseline,
            "replacement": None,
            "reason": "No permitted route remains after the reported closures",
        }
    return {
        "reachable": True,
        "baseline": baseline,
        "replacement": replacement,
        "changed": baseline["nodes"] != replacement["nodes"],
        "detour_distance": round(replacement["distance"] - baseline["distance"], 3),
    }
