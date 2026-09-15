import unittest
from unittest.mock import Mock

from visual_grid_game import VisualGridHuntGame, GridGameGUI
from agent import GreedyGridAgent


class Lab01Tests(unittest.TestCase):
    def test_traps_are_safe_and_unique(self):
        for _ in range(20):
            game = VisualGridHuntGame()
            self.assertEqual(len(game.toxic_traps), 3)
            forbidden = {(0, 0)} | game.walls | game.food_positions
            forbidden.update(tuple(p) for p in game.opponents)
            self.assertFalse(game.toxic_traps & forbidden)
            self.assertTrue(all(0 <= x < game.width and 0 <= y < game.height
                                for x, y in game.toxic_traps))

    def test_no_available_trap_cells(self):
        game = VisualGridHuntGame(1, 1, 0, 0, set())
        self.assertEqual(game.toxic_traps, set())

    def test_sensor_penalty_and_leaving(self):
        game = VisualGridHuntGame(3, 3, 0, 0, {(2, 0)})
        game.toxic_traps = {(1, 0)}
        self.assertFalse(game.get_percept()['smells_toxin'])
        game.execute_action('Right')
        self.assertEqual(game.score, -15)
        self.assertTrue(game.get_percept()['smells_toxin'])
        game.execute_action('Right')  # Blocked: wall penalty plus remaining on trap.
        self.assertEqual(game.score, -35)
        game.execute_action('Left')
        self.assertEqual(game.score, -35)
        self.assertFalse(game.get_percept()['smells_toxin'])

    def test_food_scoring(self):
        game = VisualGridHuntGame(3, 3, 0, 0, set())
        game.toxic_traps = {(2, 2)}
        game.food_positions = {(1, 0)}
        game.execute_action('Right')
        self.assertEqual(game.score, 20)
        self.assertFalse(game.food_positions)

    def test_draws_purple_trap(self):
        gui = GridGameGUI.__new__(GridGameGUI)
        gui.env = VisualGridHuntGame(3, 3, 0, 0, set())
        gui.env.toxic_traps = {(1, 1)}
        gui.cell_size = 40
        gui.canvas = Mock()
        gui.draw_grid()
        gui.canvas.create_polygon.assert_called_once_with(
            60, 48, 72, 60, 60, 72, 48, 60,
            fill='#9333ea', outline='#581c87')

    def test_starter_agent_runs(self):
        self.assertIn(GreedyGridAgent().sense_and_act({'agent_pos': [0, 0]}),
                      ['Up', 'Down', 'Left', 'Right'])


if __name__ == '__main__':
    unittest.main()
