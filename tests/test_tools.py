import unittest
from accesspath.router import Edge,route
from accesspath.profiles import constraints_for
from accesspath.map_validation import validate_graph,closure_summary
from accesspath.alternatives import route_options
class ToolTests(unittest.TestCase):
 def test_profiles_enforce_constraints(self):self.assertTrue(constraints_for("step-free").avoid_stairs)
 def test_validator_and_closure_summary(self):
  g={"A":[Edge("B",-1),Edge("C",1,closed=True)],"B":[],"C":[]};self.assertTrue(any(x["issue"]=="non-positive distance" for x in validate_graph(g)));self.assertEqual(closure_summary(g),[("A","C","path")])
 def test_alternatives_are_labeled(self):
  g={"A":[Edge("B",1)],"B":[]};self.assertEqual(route_options(g,"A","B",constraints_for("step-free"))[0]["label"],"recommended")
