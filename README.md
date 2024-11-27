# accesspath

routing with stairs, elevators, closures, rough surfaces etc.

Python for weighted paths / mobility profiles.
TypeScript for comparisons, landmark directions, screen-reader output.

```sh
python3.12 -m unittest discover -s tests -v
python3.12 -m accesspath.cli sample/map.json entrance lobby --avoid-stairs
npm install
npm test
npm run build
```

the maps are synthetic. there is no GPS or live closure feed, so this is a prototype for exploring routing constraints, not a navigation safety service.

## Implementation details

Multi-stop itineraries are available through `route_via(graph, stops, constraints)`. Every leg uses the same mobility restrictions, and invalid or non-finite edge weights are rejected before routing.

## Closure-aware alternatives

[resilience.py](accesspath/resilience.py) enumerates up to ten distinct loopless paths with a Yen-style spur search. Every candidate honors the same stairs, elevator, and surface restrictions. Parallel edges are compared using the selected cost model; alternatives are distinct by node sequence.

```sh
python -m accesspath.cli sample/map.json entrance lobby --avoid-stairs --alternatives 3
```

Closure pairs are directed; include the reverse pair for a two-way closure, and use actual endpoint names from the map. `reroute(graph, start, end, closures, constraints)` compares a baseline with the remaining permitted route, reports detour distance, and explicitly reports when closures leave no route. It never changes the caller's graph.

Tests cover directional closures, unreachable routes, loopless alternative ordering, mobility restrictions, invalid closures, and path-count limits. The CLI, Python package, and TypeScript presentation helpers are all source-bearing components.

## Reachability and connection outages

```sh
python -m accesspath.cli sample/map.json entrance lobby --avoid-stairs --reachable-budget 300
python -m accesspath.cli sample/map.json entrance lobby --avoid-stairs --reachable-budget 300 --outage-impact
```

Use actual endpoint names from your map. With `--reachable-budget`, the destination argument is unused: the report covers every reachable node from the start. Budgets are weighted routing costs, not estimated travel time. Results include distance, cost, and reconstructed paths; excluded nodes remain explicit. Mobility constraints apply throughout the catchment.

`reachability.py` also provides `outage_impact(..., edges=[('a','b')])`. Each directed closure is compared independently against the same baseline, reporting lost destinations and additional route cost. Reverse directions remain open unless separately specified. Analysis is read-only and bounded to 500 candidate connections. Zero-weight profiles and graph cycles are covered by regression checks. Accessibility depends on the map data and selected constraints; no terrain conditions are inferred.
