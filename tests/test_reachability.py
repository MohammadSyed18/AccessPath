import unittest
from copy import deepcopy
from accesspath.router import Edge, Constraints
from accesspath.reachability import reachable, outage_impact


class ReachabilityTests(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "a": [Edge("b", 2), Edge("c", 1, "stairs")],
            "b": [Edge("c", 2)],
            "c": [Edge("d", 2)],
            "d": [],
            "isolated": [],
        }

    def test_budget_boundary_profile_and_paths(self):
        result = reachable(self.graph, "a", 4, Constraints(avoid_stairs=True))
        self.assertEqual(
            [item["node"] for item in result["reachable"]], ["a", "b", "c"]
        )
        self.assertEqual(result["reachable"][-1]["path"], ["a", "b", "c"])
        self.assertEqual(result["unreachable"], ["d", "isolated"])

    def test_zero_budget_and_zero_weight_cycle_terminate(self):
        self.graph["b"].append(Edge("a", 1))
        self.assertEqual(len(reachable(self.graph, "a", 0)["reachable"]), 1)
        self.assertEqual(
            len(
                reachable(
                    self.graph,
                    "a",
                    0,
                    Constraints(distance_weight=0, difficulty_weight=0),
                )["reachable"]
            ),
            4,
        )

    def test_outage_is_directed_read_only_and_sorted_by_loss(self):
        before = deepcopy(self.graph)
        impact = outage_impact(
            self.graph,
            "a",
            10,
            Constraints(avoid_stairs=True),
            edges=[("a", "b"), ("c", "d")],
        )
        self.assertEqual(impact["outages"][0]["lost_nodes"], ["b", "c", "d"])
        self.assertEqual(self.graph, before)

    def test_invalid_graph_budget_and_closure_fail(self):
        for budget in (-1, float("nan"), True):
            with self.assertRaises(ValueError):
                reachable(self.graph, "a", budget)
        with self.assertRaises(ValueError):
            outage_impact(self.graph, "a", 5, edges=[("a", "missing")])
