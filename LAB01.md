# Practical 01 — Intelligent Systems

SE3062 · Faculty of Computing · 2026 Semester 2

Based on SLIIT-FacultyOfComputing/IT3012---Practical-Base, master commit
cdc0c0770145612c208dda91bfc7b48b377f092f.

## Part 1: Code analysis and PEAS

### 1. Four PEAS components
Performance measure, Environment, Actuators, Sensors.

### 2. Physical environment state
`self.width` and `self.height` define the grid dimensions. `self.agent_pos`,
`self.walls`, `self.food_positions`, and `self.opponents` represent the positions
of the agent, obstacles, food, and opponents. `self.score` tracks performance;
`self.steps` and `self.collision` track episode progress and collision status.

### 3. Single-agent or multi-agent?
The baseline class defaults to two adversarial opponents, so that configuration
is multi-agent. Each opponent moves independently and can collide with the
controlled agent. However, the supplied runnable demo explicitly sets
`num_opponents=0`, making that particular run single-agent.

### 4. Percept sequence
A percept sequence is the complete history of everything an agent has perceived
through its sensors up to the present time. One call to `get_percept()` provides
the current percept, not the complete history.

### 5. Which PEAS component is get_percept()?
Sensors: it supplies observations of the environment to the agent.

### 6. Observability
The baseline is partially observable. The dictionary exposes the agent position,
opponent positions, local food detection, wall and collision indicators, score,
and the number of remaining food items. It does not expose all food locations
or the wall layout. Seeing the entire canvas as a human does not give the agent
that information. Also, `hit_wall` checks the current position even though wall
entry is blocked, so it does not reliably report an attempted wall collision.

### 7. Wall penalty and PEAS
The Performance measure is updated through `self.score` when an attempted move
hits a wall.

### 8. Why evaluate external outcomes?
Performance should measure success at the task, such as collecting food and
avoiding hazards. Rewarding internal processing alone could reward computation
that does not improve outcomes. Resource use can be included when it is an
explicit task objective, but it should not replace measuring task success.

## Part 2: Toxic traps

### Implementation
- Place up to three traps within the grid, excluding the start, walls, food,
  and initial opponent positions. Sample without replacement to avoid duplicates
  and avoid an endless trap-placement loop when few cells are free.
- Add `smells_toxin`, true only when the agent occupies a trap cell.
- Deduct 15 points for each action ending on a trap. Staying on one is penalized
  again; moving away is not. Existing food and collision scoring still applies.
- Draw traps as purple diamonds in the GUI.

### 9. Hidden traps and observability
Hidden traps make safety-relevant state unavailable to the agent. An otherwise
fully observable environment would become partially observable. This starter
is already partially observable, so hiding traps increases the hidden information
without changing that classification.

### 10. Toxin sensing and rationality
The sensor identifies danger at the current location. A policy can use this
information to leave the trap and, if it remembers observed positions, avoid
returning to known traps. This can reduce expected score penalties. The sensor
does not reveal nearby traps or prevent the first entry penalty, and adding a
sensor alone does not change the starter's random action policy.

### 11. Vacuum World exploit
The standard example is a vacuum rewarded for the amount of dirt it cleans:
it could dump dirt back onto the floor and clean it repeatedly to gain reward.
A better measure rewards keeping the environment clean over time.
This is the standard textbook example; the exact Lecture 01 wording has not
been verified against a supplied lecture file in this task.

## Running and verification
Run `python visual_grid_game.py`, then click Start Simulation. Purple diamonds
mark traps. The demo keeps its original random movement and zero opponents.
Run `python -m unittest test_lab01 -v` for the focused Lab 01 checks.

The supplied `test_suite.py` imports SimpleReflexAgent, ModelBasedAgent, and
SearchAgent, which are not in this starter. Those later agent exercises have
not been implemented as part of Lab 01. A missing `random` import in the supplied
GreedyGridAgent has been repaired.
