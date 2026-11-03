"""Numerical checks independent of animation rendering."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ModelTests(unittest.TestCase):
    def test_centered_disks(self):
        model = load('convolution/circles.py')
        self.assertAlmostEqual(model.overlap_area(0), np.pi)
        self.assertEqual(model.overlap_area(2), 0)
        for x in np.linspace(0, 3, 21):
            self.assertAlmostEqual(model.overlap_area(x), model.overlap_area(-x))
            self.assertGreaterEqual(model.overlap_area(x), 0)

    def test_offset_and_eclipse(self):
        offset = load('convolution/offset_circles.py')
        stars = load('stars/partial_eclipse.py')
        self.assertAlmostEqual(offset.overlap_area(0), 2*np.pi/3-np.sqrt(3)/2)
        self.assertAlmostEqual(offset.overlap_area(np.sqrt(3)), 0, places=7)
        for x in np.linspace(-3, 3, 31):
            self.assertAlmostEqual(stars.flux(x), 1-offset.overlap_area(x)/(2*np.pi))
            self.assertTrue(0.5 <= stars.flux(x) <= 1)
        self.assertEqual(stars.flux(3), 1)

    def test_quadrature_variants(self):
        models = [load('langau/'+p) for p in
                  ['langau.py', 'langau_rectangles.py', 'langau_overlap_rectangles.py']]
        x = np.linspace(-2, 3, 21)
        baseline = models[0].quadrature(x, 100)
        self.assertTrue(np.all(np.isfinite(baseline)))
        self.assertTrue(np.all(baseline >= 0))
        for model in models[1:]:
            np.testing.assert_allclose(model.quadrature(x, 100), baseline)

    def test_smooth_convergence(self):
        model = load('langau/smooth_langau.py')
        x = np.linspace(-3, 7, 101)
        result = model.convolution(x, 160)
        self.assertTrue(np.all(np.isfinite(result)))
        self.assertTrue(np.all(result >= 0))
        np.testing.assert_allclose(result, model.convolution(x, 320), rtol=1e-8, atol=1e-10)

if __name__ == '__main__':
    unittest.main()
