# AccessPath

An accessibility-aware route-planning prototype over synthetic maps. Python performs weighted shortest-path search across distance, surface difficulty, stairs, ramps, elevators, and closures while enforcing user constraints and explaining route choice. TypeScript validates results and creates screen-reader-friendly success and unavailable-route messages.

Run `python3.12 -m unittest discover -s tests -v`, `python3.12 -m accesspath.cli sample/map.json entrance lobby --avoid-stairs`, `npm install`, `npm test`, and `npm run build`.

Map data is synthetic. This is not a navigation safety service; it has no live closure feed, geolocation, or guarantee that a modeled feature remains available.
