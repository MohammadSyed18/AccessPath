def validate_graph(graph):
 issues=[]
 for node,edges in graph.items():
  if not edges:issues.append({"node":node,"issue":"isolated or destination-only node"})
  for edge in edges:
   if edge.distance<=0:issues.append({"node":node,"issue":"non-positive distance"})
   if not 0<=edge.surface<=1:issues.append({"node":node,"issue":"surface difficulty outside 0..1"})
 return issues
def closure_summary(graph):
 return sorted({(node,e.to,e.kind) for node,edges in graph.items() for e in edges if e.closed})
