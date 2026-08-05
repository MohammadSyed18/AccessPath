from .router import route,NoRoute
def route_options(graph,start,end,constraints):
 primary=route(graph,start,end,constraints);options=[{"label":"recommended",**primary}]
 try:
  shortest=route(graph,start,end,type(constraints)(avoid_stairs=constraints.avoid_stairs,avoid_elevators=constraints.avoid_elevators,max_surface=constraints.max_surface,distance_weight=1,difficulty_weight=0))
  if shortest["nodes"]!=primary["nodes"]:options.append({"label":"shortest permitted","nodes":shortest["nodes"],"distance":shortest["distance"],"cost":shortest["cost"],"features":shortest["features"],"explanation":shortest["explanation"]})
 except NoRoute:pass
 return options
