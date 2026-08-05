# AccessPath

An accessibility-aware route-planning prototype over synthetic maps. Python provides weighted pathfinding, mobility profiles, map/closure validation, route alternatives, and explanations. TypeScript validates results, compares tradeoffs, produces landmark directions, and creates screen-reader-friendly route or failure messages.

Run `python3.12 -m unittest discover -s tests -v`, `python3.12 -m accesspath.cli sample/map.json entrance lobby --avoid-stairs`, `npm install`, `npm test`, and `npm run build`.

Map data is synthetic. This is not a navigation safety service; it has no live closure feed, geolocation, or guarantee that a modeled feature remains available.
