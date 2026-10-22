# AccessPath

A route-planning experiment with stairs, elevators, closures, and surface difficulty as part of the route cost.

Python handles weighted pathfinding and mobility profiles. TypeScript compares the results and turns them into landmark directions or screen-reader-friendly explanations.

```sh
python3.12 -m unittest discover -s tests -v
python3.12 -m accesspath.cli sample/map.json entrance lobby --avoid-stairs
npm install
npm test
npm run build
```

The maps are synthetic. There is no GPS or live closure feed, so this is a prototype for exploring routing constraints, not a navigation safety service.
