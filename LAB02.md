# Practical 02 - Agent Architectures

## Implementation

The environment exposes local wall and food sensors. `SimpleReflexAgent` uses current IF-THEN rules only. `ModelBasedAgent` stores its last action, relative position and visited cells.

## Answers

1. A table-driven agent needs an entry for every percept sequence. The number grows exponentially with the agent's lifetime, making complex environments such as chess infeasible.
2. The `food_here` and `wall_ahead` conditions in `SimpleReflexAgent.sense_and_act` are the condition-action rules.
3. Partial observability produces identical local percepts in different states. Without history, the agent repeats the same response and can cycle forever.
4. `_record_last_transition` predicts the new relative cell from the previous action. Local wall and food booleans form the sensor model; `visited_cells` preserves their history and supports an alternative action.
