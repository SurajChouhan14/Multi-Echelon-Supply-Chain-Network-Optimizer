"""
Automated Test Suite for Multi-Echelon Supply Chain Network Flow Optimizer.
Tests:
1. Topology & Demand Ingestion (7,500 demanded units across 4 products)
2. Global Minimum Network Cost ($986,883 exact optimum)
3. 100% Demand Satisfaction & Flow Conservation
4. Cost Component Additive Consistency (Procurement + Manufacturing + Distribution = Total)
5. Constraint-Binding Sensitivity Probe & Infeasibility Threshold
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import SupplyChainDataLoader
from src.supply_chain_optimizer import SupplyChainOptimizer


class TestMultiEchelonSupplyChain(unittest.TestCase):
    """
    Hard unit tests for 3-Echelon multi-commodity Linear Program optimization.
    """

    @classmethod
    def setUpClass(cls):
        cls.loader = SupplyChainDataLoader()
        cls.data = cls.loader.load_network_data()
        cls.optimizer = SupplyChainOptimizer(cls.data)
        cls.res = cls.optimizer.solve_network()

    def test_1_topology_and_demand_ingestion(self):
        """Verify 5 suppliers, 3 factories, 4 customer markets, and 7,500 units demanded."""
        self.assertEqual(len(self.data['suppliers']), 5)
        self.assertEqual(len(self.data['factories']), 3)
        self.assertEqual(len(self.data['customers']), 4)
        self.assertEqual(len(self.data['products']), 4)
        self.assertEqual(self.res['total_units_demanded'], 7500.0)

    def test_2_global_optimal_solution_and_cost(self):
        """Verify solver reaches proven global optimum at $986,883 total network cost."""
        self.assertEqual(self.res['status'], "Optimal")
        self.assertAlmostEqual(self.res['total_optimal_cost'], 986882.96, delta=1.0)

    def test_3_demand_satisfaction_and_flow_balance(self):
        """Verify 100% customer demand satisfaction with 0.0 units shortfall."""
        self.assertAlmostEqual(self.res['total_units_produced'], 7500.0, delta=0.1)
        self.assertEqual(self.res['total_units_produced'], self.res['total_units_demanded'])

    def test_4_cost_component_sum_consistency(self):
        """Verify Procurement + Manufacturing + Distribution sums exactly to total cost within rounding tolerance."""
        p_cost = self.res['procurement_and_inbound_cost']
        m_cost = self.res['manufacturing_cost']
        d_cost = self.res['distribution_shipping_cost']
        total = self.res['total_optimal_cost']

        self.assertAlmostEqual(p_cost + m_cost + d_cost, total, delta=0.05)
        self.assertAlmostEqual(p_cost, 839235.23, delta=1.0)
        self.assertAlmostEqual(m_cost, 121486.36, delta=1.0)
        self.assertAlmostEqual(d_cost, 26161.36, delta=1.0)

    def test_5_constraint_binding_sensitivity_and_infeasibility(self):
        """Verify factory capacity constraint is live (strict cost increase) and detects infeasibility."""
        # 1. Bottleneck tightening: Factory A capacity 3,000 -> 2,000
        tight_data = self.loader.load_network_data()
        tight_data['production_capacity'].loc['Factory A', 'Capacity'] = 2000.0
        tight_opt = SupplyChainOptimizer(tight_data)
        tight_res = tight_opt.solve_network()

        base_cost = self.res['total_optimal_cost']
        tight_cost = tight_res['total_optimal_cost']
        delta = tight_cost - base_cost

        # Assert strict cost increase due to capacity bottleneck
        self.assertGreater(tight_cost, base_cost)
        self.assertAlmostEqual(delta, 867.04, delta=5.0)

        # 2. Infeasibility test: Factory A capacity 3,000 -> 1,000 (Total capacity 7,300 < 7,500 demand)
        infeasible_data = self.loader.load_network_data()
        infeasible_data['production_capacity'].loc['Factory A', 'Capacity'] = 1000.0
        infeasible_opt = SupplyChainOptimizer(infeasible_data)
        infeasible_res = infeasible_opt.solve_network()

        self.assertEqual(infeasible_res['status'], "Infeasible")
        self.assertEqual(infeasible_res['total_optimal_cost'], 0.0)


if __name__ == '__main__':
    unittest.main()
