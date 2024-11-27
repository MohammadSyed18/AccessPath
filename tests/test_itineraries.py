import unittest
from accesspath.router import Edge, Constraints, NoRoute, route, route_via


class Itineraries(unittest.TestCase):
    def test_stops_are_preserved_and_constraints_apply_to_all_legs(self):
        graph = {"a": [Edge("b", 2)], "b": [Edge("c", 3, kind="stairs")], "c": []}
        self.assertEqual(route_via(graph, ["a", "b", "c"])["distance"], 5)
        with self.assertRaises(NoRoute):
            route_via(graph, ["a", "b", "c"], Constraints(avoid_stairs=True))

    def test_dijkstra_rejects_negative_or_nonfinite_weights(self):
        for distance in [-1, float("nan"), float("inf")]:
            with self.assertRaises(ValueError):
                route({"a": [Edge("b", distance)], "b": []}, "a", "b")
