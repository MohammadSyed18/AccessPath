import unittest
from accesspath.router import Edge, Constraints
from accesspath.resilience import route_alternatives, reroute, close_edges


class ResilienceTests(unittest.TestCase):
    def graph(self):
        return {
            "a": [Edge("b", 1), Edge("c", 2), Edge("d", 1, "stairs")],
            "b": [Edge("z", 1), Edge("a", 1)],
            "c": [Edge("z", 2), Edge("b", 1)],
            "d": [Edge("z", 1)],
            "z": [],
        }

    def test_distinct_loopless_paths_are_ranked_and_constraints_hold(self):
        options = route_alternatives(
            self.graph(), "a", "z", Constraints(avoid_stairs=True), count=5
        )
        self.assertEqual(len(options), 3)
        self.assertEqual(
            [item["cost"] for item in options], sorted(item["cost"] for item in options)
        )
        for option in options:
            self.assertEqual(len(option["nodes"]), len(set(option["nodes"])))
            self.assertNotIn("stairs", option["features"])
        self.assertEqual(options[0]["nodes"], ["a", "b", "z"])

    def test_closures_are_directional_and_leave_source_untouched(self):
        graph = self.graph()
        result = reroute(graph, "a", "z", [("a", "b")], Constraints(avoid_stairs=True))
        self.assertTrue(result["reachable"])
        self.assertTrue(result["changed"])
        self.assertFalse(graph["a"][0].closed)
        closed = close_edges(graph, [("a", "b")])
        self.assertFalse(closed["b"][1].closed)
        result = reroute(
            graph, "a", "z", [("a", "b"), ("a", "c")], Constraints(avoid_stairs=True)
        )
        self.assertFalse(result["reachable"])

    def test_invalid_closure_and_limit_are_rejected(self):
        with self.assertRaises(ValueError):
            close_edges(self.graph(), [("a", "missing")])
        with self.assertRaises(ValueError):
            route_alternatives(self.graph(), "a", "z", count=0)
        self.assertEqual(route_alternatives(self.graph(), "a", "a")[0]["nodes"], ["a"])


class AlternativeOracleTests(unittest.TestCase):
    def test_small_graph_costs_match_exhaustive_simple_path_oracle(self):
        import random

        rng = random.Random(19)
        for _ in range(30):
            nodes = list("abcde")
            graph = {node: [] for node in nodes}
            for source in nodes:
                for target in nodes:
                    if source != target and rng.random() < 0.45:
                        graph[source].append(Edge(target, rng.randint(1, 9)))
            costs = []

            def visit(node, seen, cost):
                if node == "e":
                    costs.append(cost)
                    return
                for edge in graph[node]:
                    if edge.to not in seen:
                        visit(edge.to, seen | {edge.to}, cost + edge.distance)

            visit("a", {"a"}, 0)
            if not costs:
                from accesspath.router import NoRoute

                with self.assertRaises(NoRoute):
                    route_alternatives(graph, "a", "e", count=5)
            else:
                actual = route_alternatives(graph, "a", "e", count=5)
                self.assertEqual([item["cost"] for item in actual], sorted(costs)[:5])
