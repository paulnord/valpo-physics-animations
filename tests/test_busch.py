"""Check the saved scene's actual trajectory helper without rewriting it."""
import ast
from pathlib import Path
import unittest
import numpy as np

SOURCE = Path(__file__).resolve().parents[1] / 'electron_beams/BuschBeamCinematic.py'

class BuschTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse(SOURCE.read_text())
        scene = next(node for node in tree.body if isinstance(node, ast.ClassDef))
        construct = next(node for node in scene.body if isinstance(node, ast.FunctionDef))
        helper = next(node for node in construct.body
                      if isinstance(node, ast.FunctionDef) and node.name == 'pos')
        # Read the original geometry constants, not copies of the physics formula.
        selected = [node for node in construct.body if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id in
                            {'x0', 'x_screen', 'L', 'vx', 't_screen'} for t in node.targets)]
        scope = {'np': np}
        exec(compile(ast.Module(body=selected+[helper], type_ignores=[]), str(SOURCE), 'exec'), scope)
        self.pos, self.scope = scope['pos'], scope

    def test_zero_field(self):
        t = self.scope['t_screen']
        np.testing.assert_allclose(self.pos(t, .2, 0), [self.scope['x_screen'], .2*t, 0])

    def test_integer_turn_focus(self):
        t = self.scope['t_screen']
        for turns in (1, 2):
            for vy in (-.2, 0, .2):
                np.testing.assert_allclose(self.pos(t, vy, turns*2*np.pi/t),
                                           [self.scope['x_screen'], 0, 0], atol=1e-12)

    def test_launch_and_symmetry(self):
        for omega in (0, .1, 1):
            np.testing.assert_allclose(self.pos(0, .2, omega), [self.scope['x0'], 0, 0])
            np.testing.assert_allclose(self.pos(3, .2, omega)[1:], -self.pos(3, -.2, omega)[1:])

if __name__ == '__main__':
    unittest.main()
