from dataclasses import dataclass
from .router import Constraints
@dataclass(frozen=True)
class MobilityProfile: name:str;stairs:bool; elevators:bool;max_surface:float;difficulty_weight:float
PROFILES={"step-free":MobilityProfile("step-free",False,True,.5,6),"low-surface":MobilityProfile("low-surface",True,True,.2,10),"no-elevator":MobilityProfile("no-elevator",True,False,.7,4)}
def constraints_for(name):
 p=PROFILES.get(name)
 if not p:raise ValueError("unknown mobility profile")
 return Constraints(avoid_stairs=not p.stairs,avoid_elevators=not p.elevators,max_surface=p.max_surface,difficulty_weight=p.difficulty_weight)
