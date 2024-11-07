import unittest
from accesspath.router import *
class RouterTests(unittest.TestCase):
 def setUp(self):self.g={"A":[Edge("B",1,"stairs"),Edge("C",2,"ramp",.1)],"B":[Edge("D",1)],"C":[Edge("D",2,"path",.1)],"D":[]}
 def test_shortest_route_can_use_stairs(self):self.assertEqual(route(self.g,"A","D")["nodes"],["A","B","D"])
 def test_constraint_selects_ramp_and_explains(self):
  r=route(self.g,"A","D",Constraints(avoid_stairs=True));self.assertEqual(r["nodes"],["A","C","D"]);self.assertIn("avoided stairs",r["explanation"])
 def test_closure_can_make_route_unavailable(self):
  g={"A":[Edge("B",1,closed=True)],"B":[]};self.assertRaises(NoRoute,route,g,"A","B")
 def test_surface_limit_is_hard_constraint(self):self.assertRaises(NoRoute,route,self.g,"A","D",Constraints(avoid_stairs=True,max_surface=0))
