# -*- coding: utf-8 -*-

"""
@author: sabrina
"""


import abc
import dataclasses
import functools
import heapq
import itertools
import random
from math import dist,inf
# utility imports (typing and visualization)
from typing import Collection, List, NamedTuple, Mapping, Tuple


######### INTERFACES

class Point(NamedTuple):
    """2D point."""
    x: float
    y: float


class Segment(NamedTuple):
    """2D segment."""
    p1: Point
    p2: Point

    def intersect(self, s: "Segment") -> bool:
        """Intersection with another segment."""
        # unpack end points
        (x1, y1), (x2, y2) = self
        (x3, y3), (x4, y4) = s
        # relative vectors
        dxa, dxb = x2 - x1, x4 - x3
        dya, dyb = y2 - y1, y4 - y3
        delta = dxa*dyb - dya*dxb
        # check segments are not parallel
        if delta == 0:
            # check collinear
            new_delta = (x3-x1)*dya-(y3-y1)*dxa
            if new_delta == 0:
                La = dxa*dxa + dya*dya
                t0 = ((x3-x1)*dxa + (y3-y1)*dya)/La
                t1 = ((x4-x1)*dxa + (y4-y1)*dya)/La
                tmin, tmax = min(t0, t1), max(t0, t1)
                return ((0 <= t0 <= 1) or (0 <= t1 <= 1) or
                        (tmin <= 0 and tmax >= 1))
            # parallel non collinear
            return False
        # relative intersection coordinates
        s = ((x3-x1)*dyb - (y3-y1)*dxb) / delta
        t = ((x3-x1)*dya - (y3-y1)*dxa) / delta
        return (0 <= s <= 1) and (0 <= t <= 1)
       

class ARect(NamedTuple):
    """Axis-aligned rectangle."""
    bl_corner: Point  # top-left corner
    tr_corner: Point  # bottom-right corner

    def has_point(self, p: Point) -> bool:
        """Check whether point is inside rectangle."""
        (x1, y1), (x2, y2) = self  # unpack rectangle coordinates
        x, y = p  # unpack point coordinates
        return (x1 <= x <= x2) and (y1 <= y <= y2)

    def intersect_segment(self, s: Segment) -> bool:
        """Check intersection with a segment."""
        # test end point
        if self.has_point(s.p1) or self.has_point(s.p2):
            return True
        # unpack rectangle coordinates
        (x1, y1), (x2, y2) = self
        # compute corners
        c1, c2, c3, c4 = itertools.product((x1, x2), (y1, y2))
        pc1, pc2, pc3, pc4 = Point(*c1), Point(*c2), Point(*c3), Point(*c4)
        # sides
        sides = [Segment(pc1, pc2), Segment(pc2, pc4), Segment(pc4, pc3), Segment(pc3, pc1)]
        return any(side.intersect(s) for side in sides)
    

class CSpace(abc.ABC):
    """Abtract base class for configuration space.

    It is just the definition of the interface.
    """
    @abc.abstractmethod
    def sample_free(self) -> Point:
        """Sample a point in free space."""
        ...

    @abc.abstractmethod
    def coll_free(self, p1: Point, p2: Point) -> bool:
        """Check absence of collision between p1 and p2."""
        ...


def steer(p1: Point, p2: Point, eta: float) -> Point:
    """Go from p1 toward p2 stopping at most at distance eta."""
    d = dist(p1, p2)
    # close enough
    if d <= eta:
        return p2
    x1, y1 = p1
    x2, y2 = p2
    x = x1 + (x2 - x1) / d * eta
    y = y1 + (y2 - y1) / d * eta
    return Point(x, y)

def nearest(vertices: Collection[Point], p: Point) -> Point:
    """Closest point of p in vertices.

    This is a naive (but short) implementation.
    """
    dist_p = functools.partial(dist, p)  # distance-from-p function
    return min(vertices, key=dist_p)

def near(vertices: Collection[Point], p: Point, d: float) -> List[Point]:
    """Points in vertices closer to p than d.

    This is a naive (but short) implementation.
    """
    return [x for x in vertices if dist(p, x) <= d]



@dataclasses.dataclass
class GraphPathPlanning(abc.ABC):
    """Incremental graph path planning abstract class."""
    cspace: CSpace  # environment
    start: Point  # starting point of the path
    goal: Point  # goal of the path planning

    @abc.abstractmethod
    def expand(self) -> List[Tuple[Point, Point]]:
        """Incremental step.
        
        Return:
            edges of graph.
        """
        ...

    def build_current_path(self) -> List[Point]:
        """Build current path from start to goal."""
        # default: no current path
        return []

    def build_final_path(self) -> List[Point]:
        """Build final path from start to goal."""
        return self.build_current_path()
    
@dataclasses.dataclass(frozen=True)
class ARectCSpace(CSpace):
    """Configuration space made of axis-aligned rectangular obstacles."""
    bounding_box: ARect  # exterior bounding box
    obstacles: Collection[ARect]  # obstacles as axis-aligned rectangles
    
    def sample_free(self, max_tries=100) -> Point:
        """Sample a point in free space."""
        (x1, y1), (x2, y2) = self.bounding_box
        for _ in range(max_tries):
            # sample point in bounding box
            p = Point(random.uniform(x1, x2), random.uniform(y1, y2))
            # check collision
            if any(obstacle.has_point(p) for obstacle in self.obstacles):
                continue
            return p
        raise RuntimeError(f"No point found after max = {max_tries} attempts.")

    def coll_free(self, p1: Point, p2: Point) -> bool:
        """Check absence of collision between p1 and p2."""
        if not self.bounding_box.has_point(p1) or not self.bounding_box.has_point(p2):
            return False
        s = Segment(p1, p2)
        if any(obstacle.intersect_segment(s) for obstacle in self.obstacles):
            return False
        return True
    

################### RRT* #####################
CostMap = Mapping[Point, float]

@dataclasses.dataclass
class RRTStar(GraphPathPlanning):
    """RRT* algorithm."""
    eta: float
    delta: float
    ...  
    
    def __post_init__(self) -> None:
        """Initialize internal search state."""
        
        self.parent_map = {self.start:None}
        self.V : Collection[Point] = [self.start]
        self.E : List[Tuple[Point, Point]] = []
        self.cost_map: CostMap = {self.start: 0.}
    
    def cout(self,a:Point,b:Point):
         """ cout entre a et b"""
         c = ((a.x-b.x)**2+(a.y -b.y)**2)**(0.5) #distance euclidienne
         return c
    
            
    def expand(self, N: int = 1) -> List[Tuple[Point, Point]]:
        """Perform N iterations of growing the tree.
        
        Return:
            edges of graph.
        """
        for i in range(N):
                    p_rand = self.cspace.sample_free()
                    p_nearest = nearest(self.V,p_rand)
                    p_new = steer(p_nearest,p_rand,self.eta)

                    if self.cspace.coll_free(p_nearest, p_new) :
                        P_near = near(self.V, p_rand, self.delta)
                        p_min = min(P_near,default=p_nearest, key=lambda x: self.cost_map[x] if(self.cspace.coll_free(p_new,x)) else inf)

                        self.V.append(p_new)
                        self.E.append([p_min, p_new])
                        self.parent_map[p_new]= p_min
                        self.cost_map[p_new]=self.cost_map[p_min]+ self.cout(p_min,p_new)
                        
                        for x in P_near :
                             distance = self.cost_map[p_new]+self.cout(p_new,x)
                             if distance < self.cost_map[x]:
                                  self.E.remove([self.parent_map[x],x])
                                  self.E.append([p_new,x])
                                  self.parent_map[x] = p_new
                                  self.cost_map[x] = distance
        return self.E
    
 

    def build_current_path(self) -> List[Point]:
        """Build current path from start to goal.

        The path is checked until the nearest vertex in the
        tree if there is no collision to the goal.
        Otherwise, an empty path is returned.
        """
        
        p_nearest = min(self.V, key=lambda point: self.cout(self.goal,point))
        if not(self.cspace.coll_free(self.goal,p_nearest)) : 
            return []
        path = [self.goal, p_nearest]
        n = p_nearest 
        while self.parent_map[n] is not None : # si vide : while current_node in parent_map:(est-ce que node vide ?) append(current)
            n = self.parent_map[n]
            path.append(n)
        return path
    

######################### TEST
    
# C-space
bounding_box = ARect(Point(1, 1), Point(30, 30))
obstacles = [
    ARect(Point(2, 8), Point(9, 15)),
    ARect(Point(9, 2), Point(16, 6)),
    ARect(Point(11, 8), Point(16, 13))
]
arect_cspace = ARectCSpace(bounding_box, obstacles)
