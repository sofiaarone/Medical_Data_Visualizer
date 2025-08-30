import unittest
import seaborn as sns
import matplotlib as mpl

import medical_data_visualizer


class CatPlotTestCase(unittest.TestCase):
    def setUp(self):
        # before each test, generate the catplot figure
        self.fig = medical_data_visualizer.draw_cat_plot()

    def test_catplot_exists(self):
        # check if draw_cat_plot actually returns a matplotlib figure
        self.assertIsInstance(self.fig, mpl.figure.Figure)

    def test_catplot_axes(self):
        # catplot should have 2 panels (cardio = 0 and cardio = 1)
        axes = self.fig.get_axes()
        self.assertEqual(len(axes), 2)

    def test_catplot_xticklabels(self):
        # check that the x labels are the expected feature names
        axes = self.fig.get_axes()
        labels = [t.get_text() for t in axes[0].get_xticklabels()]
        expected_features = sorted(["active", "alco", "cholesterol", "gluc", "overweight", "smoke"])
        self.assertEqual(sorted(labels), expected_features)


class HeatMapTestCase(unittest.TestCase):
    def setUp(self):
        # before each test, generate the heatmap figure
        self.fig = medical_data_visualizer.draw_heat_map()

    def test_heatmap_exists(self):
        # check if draw_heat_map returns a matplotlib figure
        self.assertIsInstance(self.fig, mpl.figure.Figure)

    def test_heatmap_axes(self):
        # heatmap normally has 1 axis (plot) + possibly 1 colorbar axis
        axes = self.fig.get_axes()
        self.assertIn(len(axes), [1, 2])  # accepts 1 or 2 axes

    def test_heatmap_labels(self):
        # make sure the heatmap includes important features as labels
        axes = self.fig.get_axes()[0]
        xticklabels = [t.get_text() for t in axes.get_xticklabels()]
        self.assertIn("weight", xticklabels)
        self.assertIn("height", xticklabels)
        self.assertIn("ap_hi", xticklabels)
        self.assertIn("ap_lo", xticklabels)
        self.assertIn("cholesterol", xticklabels)


if __name__ == "__main__":
    unittest.main()