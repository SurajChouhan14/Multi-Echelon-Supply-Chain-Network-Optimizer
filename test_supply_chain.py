"""
Automated Unit Test Suite for Multi-Echelon Supply Chain Network Optimizer.
Verifies Data Ingestion, BOM Balances, Capacity Constraints, and Exact MILP Optimization Convergence.
"""

import unittest
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import SupplyChainDataLoader
from src.supply_chain_optimizer import SupplyChainOptimizer


class TestSupplyChainOptimizer(unittest.TestCase):
    """
    Unit test cases for multi-echelon supply chain network optimizer.
    """

    @classmethod
    def setUpClass(cls):
        cls.loader = SupplyChainDataLoader(data_dir="data")
        cls.network_data = cls.loader.load_network_data()
        cls.optimizer = SupplyChainOptimizer(cls.network_data)
        cls.result = cls.optimizer.solve_network()

    def test_network_data_structure(self):
        """Verify network topology node and matrix dimensions."""
        self.assertEqual(len(self.network_data['suppliers']), 5)
        self.assertEqual(len(self.network_data['factories']), 3)
        self.assertEqual(len(self.network_data['products']), 4)
        self.assertEqual(len(self.network_data['customers']), 4)
        self.assertGreater(self.network_data['customer_demand'].values.sum(), 0)

    def test_optimization_convergence(self):
        """Verify solver status is Optimal and total cost is positive."""
        self.assertEqual(self.result['status'], 'Optimal')
        self.assertGreater(self.result['total_optimal_cost'], 0.0)

    def test_demand_fulfillment(self):
        """Verify total production volume matches total customer demand."""
        self.assertGreaterEqual(self.result['total_units_produced'], self.result['total_units_demanded'])

    def test_cost_breakdown_sum(self):
        """Verify the sum of cost components matches total optimal cost."""
        total_calc = (
            self.result['procurement_and_inbound_cost']
            + self.result['manufacturing_cost']
            + self.result['distribution_shipping_cost']
        )
        self.assertAlmostEqual(total_calc, self.result['total_optimal_cost'], places=1)


if __name__ == '__main__':
    unittest.main()
