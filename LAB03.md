# Practical 03 - Uninformed Search

## Implementation

`SearchAgent` implements BFS with a FIFO queue, DFS with a LIFO stack, and UCS with a priority queue. Each algorithm performs graph search and returns an offline action plan. The environment percept exposes its grid size, walls and all food positions.

## Answers

1. The state space is the set of possible world states and transitions. The search tree is the algorithm's generated paths through that space; the same state may appear through different paths.
2. The `reached` set prevents repeated expansion and cycles. Without it, DFS can revisit the same grid cells indefinitely.
3. Every grid move costs one. BFS explores by increasing path depth, so its first solution has the fewest moves. DFS follows one deep branch and may find a much longer solution first.
4. BFS stores the full frontier at a depth and needs exponential space, approximately O(b^d). DFS mainly stores the current path and remaining siblings, approximately O(bm), so it uses less memory but may explore very deep paths.
