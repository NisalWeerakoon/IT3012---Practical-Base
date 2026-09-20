"""Agent programs used by the SE3062 Intelligent Systems practicals."""

import random


ACTIONS = ("Up", "Right", "Down", "Left")


class GreedyGridAgent:
    """The original starter agent retained for comparison."""

    def __init__(self):
        self.actions_pool = list(ACTIONS)

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """Selects an action only from the current local percept."""

    def sense_and_act(self, percept: dict) -> str:
        if percept.get("food_here"):
            return "Stay"
        if percept.get("wall_ahead"):
            return "Right"
        return "Up"


class ModelBasedAgent:
    """Uses a small internal model to avoid repeating failed moves."""

    def __init__(self):
        self.relative_pos = (0, 0)
        self.visited_cells = {self.relative_pos}
        self.last_action = None
        self._choice_index = 0

    def _record_last_transition(self, percept: dict) -> None:
        if not self.last_action or self.last_action == "Stay" or percept.get("hit_wall"):
            return
        x, y = self.relative_pos
        dx, dy = {
            "Up": (0, 1), "Right": (1, 0),
            "Down": (0, -1), "Left": (-1, 0)
        }[self.last_action]
        self.relative_pos = (x + dx, y + dy)
        self.visited_cells.add(self.relative_pos)

    def sense_and_act(self, percept: dict) -> str:
        self._record_last_transition(percept)
        if percept.get("food_here"):
            self.last_action = "Stay"
            return "Stay"

        blocked = {
            "Up": percept.get("wall_up", percept.get("wall_ahead", False)),
            "Right": percept.get("wall_right", False),
            "Down": percept.get("wall_down", False),
            "Left": percept.get("wall_left", False),
        }
        for offset in range(len(ACTIONS)):
            action = ACTIONS[(self._choice_index + offset) % len(ACTIONS)]
            dx, dy = {
                "Up": (0, 1), "Right": (1, 0),
                "Down": (0, -1), "Left": (-1, 0)
            }[action]
            candidate = (self.relative_pos[0] + dx, self.relative_pos[1] + dy)
            if not blocked[action] and candidate not in self.visited_cells:
                self._choice_index = (ACTIONS.index(action) + 1) % len(ACTIONS)
                self.last_action = action
                return action

        action = ACTIONS[self._choice_index]
        self._choice_index = (self._choice_index + 1) % len(ACTIONS)
        self.last_action = action
        return action
