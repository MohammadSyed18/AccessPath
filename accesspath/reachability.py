"""Budgeted accessible catchments and read-only connection-outage analysis."""

import heapq
import math
from .router import Constraints, route
from .resilience import close_edges


def reachable(graph, start, budget, constraints=Constraints()):
    if (
        isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or not math.isfinite(budget)
        or budget < 0
    ):
        raise ValueError("budget must be a finite nonnegative routing cost")
    # Reuse the route engine's graph and profile validation, even for a zero budget.
    route(graph, start, start, constraints)
    best = {start: (0.0, 0.0)}
    parents = {start: None}
    pending = [(0.0, 0.0, start)]
    while pending:
        cost, distance, node = heapq.heappop(pending)
        if best[node] != (cost, distance):
            continue
        for edge in graph[node]:
            if (
                edge.closed
                or edge.surface > constraints.max_surface
                or (constraints.avoid_stairs and edge.kind == "stairs")
                or (constraints.avoid_elevators and edge.kind == "elevator")
            ):
                continue
            candidate = (
                cost
                + constraints.distance_weight * edge.distance
                + constraints.difficulty_weight * edge.surface,
                distance + edge.distance,
            )
            if candidate[0] > budget or candidate >= best.get(
                edge.to, (math.inf, math.inf)
            ):
                continue
            best[edge.to] = candidate
            parents[edge.to] = node
            heapq.heappush(pending, (*candidate, edge.to))
    items = []
    for node, (cost, distance) in sorted(
        best.items(), key=lambda pair: (pair[1], pair[0])
    ):
        path = [node]
        while parents[path[-1]] is not None:
            path.append(parents[path[-1]])
        items.append(
            {
                "node": node,
                "cost": round(cost, 3),
                "distance": round(distance, 3),
                "path": list(reversed(path)),
            }
        )
    return {
        "start": start,
        "budget": budget,
        "reachable": items,
        "unreachable": sorted(set(graph) - set(best)),
    }


def outage_impact(graph, start, budget, constraints=Constraints(), *, edges=None):
    """Compare each directed closure independently, without changing the input map."""
    baseline = reachable(graph, start, budget, constraints)
    before = {item["node"]: item for item in baseline["reachable"]}
    selected = (
        sorted(set(tuple(edge) for edge in edges))
        if edges is not None
        else sorted(
            {
                (node, edge.to)
                for node, values in graph.items()
                for edge in values
                if not edge.closed
            }
        )
    )
    if len(selected) > 500:
        raise ValueError("outage analysis supports at most 500 directed connections")
    results = []
    for pair in selected:
        after = reachable(close_edges(graph, [pair]), start, budget, constraints)
        available = {item["node"]: item for item in after["reachable"]}
        lost = sorted(set(before) - set(available))
        detours = [
            {
                "node": node,
                "extra_cost": round(available[node]["cost"] - before[node]["cost"], 3),
            }
            for node in sorted(set(before) & set(available))
            if available[node]["cost"] > before[node]["cost"]
        ]
        results.append(
            {"closed_edge": list(pair), "lost_nodes": lost, "detours": detours}
        )
    results.sort(
        key=lambda item: (
            -len(item["lost_nodes"]),
            -len(item["detours"]),
            item["closed_edge"],
        )
    )
    return {"baseline": baseline, "outages": results}
