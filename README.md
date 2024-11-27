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
