"""Agent programs used by the SE3062 Intelligent Systems practicals."""

import heapq
import math
import random
from collections import deque


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


class SearchAgent:
    """Goal-based agent with uninformed offline planning strategies."""

    MOVES = (
        ("Up", (0, 1)), ("Right", (1, 0)),
        ("Down", (0, -1)), ("Left", (-1, 0)),
    )

    def __init__(self, active_algo="BFS"):
        self.plan = []
        self.active_algo = active_algo

    @staticmethod
    def _valid(pos, walls, grid_size):
        x, y = pos
        return 0 <= x < grid_size[0] and 0 <= y < grid_size[1] and pos not in walls

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        walls = set(map(tuple, walls))
        frontier = deque([(tuple(start_pos), [])])
        reached = {tuple(start_pos)}
        while frontier:
            current, path = frontier.popleft()
            if current == tuple(goal_pos):
                return path
            for action, (dx, dy) in self.MOVES:
                neighbor = (current[0] + dx, current[1] + dy)
                if self._valid(neighbor, walls, grid_size) and neighbor not in reached:
                    reached.add(neighbor)
                    frontier.append((neighbor, path + [action]))
        return None

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        walls = set(map(tuple, walls))
        frontier = [(tuple(start_pos), [])]
        reached = set()
        while frontier:
            current, path = frontier.pop()
            if current == tuple(goal_pos):
                return path
            if current in reached:
                continue
            reached.add(current)
            for action, (dx, dy) in reversed(self.MOVES):
                neighbor = (current[0] + dx, current[1] + dy)
                if self._valid(neighbor, walls, grid_size) and neighbor not in reached:
                    frontier.append((neighbor, path + [action]))
        return None

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        walls = set(map(tuple, walls))
        frontier = [(0, tuple(start_pos), [])]
        best_cost = {tuple(start_pos): 0}
        while frontier:
            cost, current, path = heapq.heappop(frontier)
            if current == tuple(goal_pos):
                return path
            if cost != best_cost.get(current):
                continue
            for action, (dx, dy) in self.MOVES:
                neighbor = (current[0] + dx, current[1] + dy)
                new_cost = cost + 1
                if (self._valid(neighbor, walls, grid_size)
                        and new_cost < best_cost.get(neighbor, float("inf"))):
                    best_cost[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor, path + [action]))
        return None

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

    def astar_search(self, start_pos, goal_pos, walls, grid_size,
                     heuristic_type="manhattan"):
        start, goal = tuple(start_pos), tuple(goal_pos)
        walls = set(map(tuple, walls))
        heuristic = (self.euclidean_distance if heuristic_type == "euclidean"
                     else self.manhattan_distance)
        frontier = [(heuristic(start, goal), 0, start, [])]
        reached_states = set()
        best_cost = {start: 0}
        while frontier:
            _, cost, current, path = heapq.heappop(frontier)
            if current == goal:
                return path
            if current in reached_states:
                continue
            reached_states.add(current)
            for action, (dx, dy) in self.MOVES:
                neighbor = (current[0] + dx, current[1] + dy)
                new_cost = cost + 1
                if (self._valid(neighbor, walls, grid_size)
                        and neighbor not in reached_states
                        and new_cost < best_cost.get(neighbor, float("inf"))):
                    best_cost[neighbor] = new_cost
                    heapq.heappush(frontier, (
                        new_cost + heuristic(neighbor, goal), new_cost,
                        neighbor, path + [action],
                    ))
        return None

    def sense_and_act(self, percept):
        if not self.plan:
            start = tuple(percept["agent_pos"])
            foods = [tuple(food) for food in percept["all_food"]]
            if not foods:
                return "Stay"
            goal = min(foods, key=lambda food: abs(food[0] - start[0]) + abs(food[1] - start[1]))
            method = {
                "BFS": self.bfs_search,
                "DFS": self.dfs_search,
                "UCS": self.ucs_search,
                "AStar": self.astar_search,
            }.get(self.active_algo, self.bfs_search)
            self.plan = method(start, goal, percept["walls"], percept["grid_size"]) or []
        return self.plan.pop(0) if self.plan else "Stay"
