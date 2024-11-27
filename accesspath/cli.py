import argparse
import json
from pathlib import Path
from .router import load, Constraints
from .resilience import close_edges, route_alternatives
from .reachability import reachable, outage_impact


def main():
    parser = argparse.ArgumentParser(
        description="Accessible route alternatives with explicit closures"
    )
    parser.add_argument("map", type=Path)
    parser.add_argument("start")
    parser.add_argument("end")
    parser.add_argument("--avoid-stairs", action="store_true")
    parser.add_argument("--avoid-elevators", action="store_true")
    parser.add_argument("--max-surface", type=float, default=1)
    parser.add_argument("--alternatives", type=int, default=1)
    parser.add_argument("--closed-edge", action="append", default=[], metavar="FROM:TO")
    parser.add_argument("--reachable-budget", type=float)
    parser.add_argument("--outage-impact", action="store_true")
    args = parser.parse_args()
    try:
        graph = close_edges(
            load(args.map), [value.split(":") for value in args.closed_edge]
        )
        constraints = Constraints(
            avoid_stairs=args.avoid_stairs,
            avoid_elevators=args.avoid_elevators,
            max_surface=args.max_surface,
        )
        if args.reachable_budget is not None:
            result = (outage_impact if args.outage_impact else reachable)(
                graph, args.start, args.reachable_budget, constraints
            )
            print(json.dumps(result, indent=2))
            return
        if args.outage_impact:
            raise ValueError("--outage-impact requires --reachable-budget")
        print(
            json.dumps(
                route_alternatives(
                    graph, args.start, args.end, constraints, args.alternatives
                ),
                indent=2,
            )
        )
    except (ValueError, KeyError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
