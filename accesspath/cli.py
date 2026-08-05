import argparse,json
from pathlib import Path
from .router import *
def main():
 p=argparse.ArgumentParser();p.add_argument("map",type=Path);p.add_argument("start");p.add_argument("end");p.add_argument("--avoid-stairs",action="store_true");p.add_argument("--max-surface",type=float,default=1);a=p.parse_args();print(json.dumps(route(load(a.map),a.start,a.end,Constraints(avoid_stairs=a.avoid_stairs,max_surface=a.max_surface)),indent=2))
if __name__=="__main__":main()
