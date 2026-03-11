from pydantic import BaseModel
from typing import List, Tuple, Optional

class Facility(BaseModel):
    name: str
    category: str
    x: float
    y: float

class Edge(BaseModel):
    start_node: str
    end_node: str
    weight: Optional[float] = None # We will calculate this automatically

class Station(BaseModel):
    name: str
    map_url: str
    facilities: List[Facility]
    edges: List[Edge] # <--- Added this for Phase 2