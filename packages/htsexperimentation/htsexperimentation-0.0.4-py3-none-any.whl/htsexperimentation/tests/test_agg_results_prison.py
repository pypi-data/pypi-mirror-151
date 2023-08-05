import unittest
from ..compute_results.compute_res_funcs import calculate_agg_results_all_datasets


class TestModel(unittest.TestCase):
    def setUp(self):
        self.datasets = ["prison"]
        self.algorithms = ["gpf"]

    def test_results_gpf_parsing_prison(self):
        self.assertTrue(
            calculate_agg_results_all_datasets(
                self.datasets,
                self.algorithms,
                "mase",
                path="htsexperimentation/tests/results_probabilistic",
            )[0].shape
            == (90, 6),
        )
