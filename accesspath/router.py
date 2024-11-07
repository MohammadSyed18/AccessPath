from __future__ import annotations
import heapq,json
from dataclasses import dataclass,asdict
from pathlib import Path
@dataclass(frozen=True)
class Edge: to:str;distance:float;kind:str="path";surface:float=0;closed:bool=False
@dataclass(frozen=True)
class Constraints: avoid_stairs:bool=False;avoid_elevators:bool=False;max_surface:float=1;distance_weight:float=1;difficulty_weight:float=4
class NoRoute(Exception):pass
def load(path:Path):
 raw=json.loads(path.read_text());g={str(n):[] for n in raw["nodes"]}
 for e in raw["edges"]:
  if e["from"] not in g or e["to"] not in g:raise ValueError("edge references unknown node")
  edge=Edge(e["to"],e["distance"],e.get("kind","path"),e.get("surface",0),e.get("closed",False));g[e["from"]].append(edge)
  if e.get("bidirectional",True):g[e["to"]].append(Edge(e["from"],edge.distance,edge.kind,edge.surface,edge.closed))
 return g
def route(graph,start,end,c=Constraints()):
 if start not in graph or end not in graph:raise ValueError("unknown endpoint")
 q=[(0.,0.,start,[])];best={start:0.}
 while q:
  cost,distance,node,steps=heapq.heappop(q)
  if node==end:
   kinds=[e.kind for _,e in steps];reasons=[f"avoided stairs" for _ in [0] if c.avoid_stairs]+[f"selected {round(distance,1)} distance units with surface penalty {round(cost-c.distance_weight*distance,1)}"]
   return {"nodes":[start]+[n for n,_ in steps],"distance":round(distance,3),"cost":round(cost,3),"features":kinds,"explanation":"; ".join(reasons)}
  if cost>best.get(node,float("inf")):continue
  for e in graph[node]:
   if e.closed or e.surface>c.max_surface or (c.avoid_stairs and e.kind=="stairs") or (c.avoid_elevators and e.kind=="elevator"):continue
   score=cost+c.distance_weight*e.distance+c.difficulty_weight*e.surface
   if score<best.get(e.to,float("inf")):best[e.to]=score;heapq.heappush(q,(score,distance+e.distance,e.to,steps+[(e.to,e)]))
 raise NoRoute(f"no route from {start} to {end} satisfies the selected constraints")
