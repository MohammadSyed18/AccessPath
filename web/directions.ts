import type {Route} from "./presenter.js";
export type LandmarkMap=Record<string,string>;
export function directions(route:Route,landmarks:LandmarkMap={}){return route.nodes.slice(1).map((node,index)=>({step:index+1,instruction:`Continue to ${landmarks[node]??node}${route.features[index]?` via ${route.features[index]}`:""}.`,feature:route.features[index]??"path"}))}
export function routeComparison(routes:(Route&{label:string})[]){return routes.map(r=>({label:r.label,distance:r.distance,cost:r.cost,summary:`${r.label}: ${r.distance} distance units; ${[...new Set(r.features)].join(", ")}`}))}
