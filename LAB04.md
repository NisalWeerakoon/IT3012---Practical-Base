# Practical 04 - Informed Search

## Implementation

`SearchAgent` now provides Manhattan and Euclidean distance functions and A* search. A* orders the frontier by `f(n) = g(n) + h(n)`, retains best path costs, and supports either heuristic. The visual game starts with A* as its active planner.

Testing checkpoint: from (0, 0) to (3, 4), Manhattan distance is 7 and Euclidean distance is 5.0.

## Answers

1. UCS prioritizes the smallest accumulated path cost `g(n)`. A* prioritizes `g(n) + h(n)`, adding an estimate of the remaining cost.
2. On a four-way unit-cost grid, every path must cover at least the horizontal and vertical separation, so Manhattan distance never overestimates the true cost. A non-admissible heuristic could cause A* to return a suboptimal path.
3. With unit-cost diagonal moves, Manhattan distance can overestimate. Chebyshev distance is suitable; Euclidean distance is appropriate when diagonal cost reflects geometric distance.
4. A stronger all-food heuristic is the distance to the nearest food plus a minimum spanning tree cost over the remaining food. It estimates the work needed to connect every target.
