"""
Multi-Echelon Supply Chain Network Linear Programming Optimizer.
Formulates and solves a 3-Echelon multi-commodity flow optimization problem minimizing total network cost:
1. Raw Material Purchasing & Inbound Transportation Tariffs
2. Plant-Level Production Conversion Costs (with BOM requirements)
3. Finished Goods Outbound Distribution Logistics Costs
Powered by native SciPy HiGHS Dual-Simplex / Interior-Point LP Solver.
"""

import numpy as np
import pandas as pd
from scipy.optimize import linprog


class SupplyChainOptimizer:
    """
    Exact Linear Programming Solver for Multi-Echelon Supply Chain Networks using native SciPy HiGHS.
    """

    def __init__(self, network_data):
        self.data = network_data
        self.suppliers = network_data['suppliers']
        self.materials = network_data['materials']
        self.factories = network_data['factories']
        self.products = network_data['products']
        self.customers = network_data['customers']

        self.sup_stock = network_data['supplier_stock']
        self.mat_cost = network_data['material_cost']
        self.inbound_ship = network_data['inbound_shipping']
        self.bom = network_data['bom']
        self.prod_cap = network_data['production_capacity']
        self.prod_cost = network_data['production_cost']
        self.demand = network_data['customer_demand']
        self.outbound_ship = network_data['outbound_shipping']

    def solve_network(self):
        """
        Builds and solves the exact supply chain network Linear Program (LP) using SciPy HiGHS.
        Returns:
            dict containing status, total cost breakdown, and operational flow volumes.
        """
        # Variable mapping:
        # 1. orders[f, m, s] -> num_factories * num_materials * num_suppliers (60 vars)
        order_keys = [(f, m, s) for f in self.factories for m in self.materials for s in self.suppliers]
        order_map = {k: idx for idx, k in enumerate(order_keys)}

        # 2. prod[f, p] -> num_factories * num_products (12 vars)
        prod_keys = [(f, p) for f in self.factories for p in self.products]
        prod_map = {k: len(order_keys) + idx for idx, k in enumerate(prod_keys)}

        # 3. deliv[f, c, p] -> num_factories * num_customers * num_products (48 vars)
        deliv_keys = [(f, c, p) for f in self.factories for c in self.customers for p in self.products]
        deliv_map = {k: len(order_keys) + len(prod_keys) + idx for idx, k in enumerate(deliv_keys)}

        num_vars = len(order_keys) + len(prod_keys) + len(deliv_keys)
        c = np.zeros(num_vars)

        # Objective Function Coefficients:
        # Min Procurement + Inbound Freight + Production Cost + Outbound Distribution Freight
        for (f, m, s), idx in order_map.items():
            c[idx] = float(self.mat_cost.loc[s, m] + self.inbound_ship.loc[s, f])

        for (f, p), idx in prod_map.items():
            c[idx] = float(self.prod_cost.loc[f, p])

        for (f, c_name, p), idx in deliv_map.items():
            c[idx] = float(self.outbound_ship.loc[f, c_name])

        A_ub = []
        b_ub = []

        # Constraint 1: Supplier Capacity Limits
        # sum_f orders[f, m, s] <= stock[s, m]
        for s in self.suppliers:
            for m in self.materials:
                row = np.zeros(num_vars)
                for f in self.factories:
                    row[order_map[(f, m, s)]] = 1.0
                A_ub.append(row)
                b_ub.append(float(self.sup_stock.loc[s, m]))

        # Constraint 2: Factory Production Capacity Limits
        # sum_p prod[f, p] <= cap[f]
        for f in self.factories:
            row = np.zeros(num_vars)
            for p in self.products:
                row[prod_map[(f, p)]] = 1.0
            A_ub.append(row)
            b_ub.append(float(self.prod_cap.loc[f, 'Capacity']))

        # Constraint 3: Bill of Materials (BOM) Raw Material Balance
        # -sum_s orders[f, m, s] + sum_p bom[p, m] * prod[f, p] <= 0
        for f in self.factories:
            for m in self.materials:
                row = np.zeros(num_vars)
                for s in self.suppliers:
                    row[order_map[(f, m, s)]] = -1.0
                for p in self.products:
                    row[prod_map[(f, p)]] = float(self.bom.loc[p, m])
                A_ub.append(row)
                b_ub.append(0.0)

        # Constraint 4: Factory Flow Conservation
        # -prod[f, p] + sum_c deliv[f, c, p] <= 0
        for f in self.factories:
            for p in self.products:
                row = np.zeros(num_vars)
                row[prod_map[(f, p)]] = -1.0
                for c_name in self.customers:
                    row[deliv_map[(f, c_name, p)]] = 1.0
                A_ub.append(row)
                b_ub.append(0.0)

        # Constraint 5: Customer Demand Satisfaction
        # -sum_f deliv[f, c, p] <= -demand[p, c]
        for c_name in self.customers:
            for p in self.products:
                row = np.zeros(num_vars)
                for f in self.factories:
                    row[deliv_map[(f, c_name, p)]] = -1.0
                A_ub.append(row)
                b_ub.append(-float(self.demand.loc[p, c_name]))

        A_ub = np.array(A_ub)
        b_ub = np.array(b_ub)

        # Solve using SciPy HiGHS Dual-Simplex Continuous LP Solver
        res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method='highs')

        if not res.success:
            return {
                "status": "Infeasible" if "infeasible" in res.message.lower() else "Solver_Failed",
                "solver_message": res.message,
                "total_optimal_cost": 0.0,
                "procurement_and_inbound_cost": 0.0,
                "manufacturing_cost": 0.0,
                "distribution_shipping_cost": 0.0,
                "total_units_demanded": float(self.demand.values.sum()),
                "total_units_produced": 0.0
            }

        x_sol = res.x
        total_cost = float(res.fun)

        # Calculate cost breakdown
        procurement_cost = sum(
            x_sol[order_map[(f, m, s)]] * (self.mat_cost.loc[s, m] + self.inbound_ship.loc[s, f])
            for (f, m, s) in order_keys
        )
        manufacturing_cost = sum(
            x_sol[prod_map[(f, p)]] * self.prod_cost.loc[f, p]
            for (f, p) in prod_keys
        )
        distribution_cost = sum(
            x_sol[deliv_map[(f, c_name, p)]] * self.outbound_ship.loc[f, c_name]
            for (f, c_name, p) in deliv_keys
        )
        total_produced = sum(x_sol[prod_map[(f, p)]] for (f, p) in prod_keys)

        return {
            "status": "Optimal_Converged (HiGHS)",
            "solver_message": res.message,
            "total_optimal_cost": round(total_cost, 2),
            "procurement_and_inbound_cost": round(float(procurement_cost), 2),
            "manufacturing_cost": round(float(manufacturing_cost), 2),
            "distribution_shipping_cost": round(float(distribution_cost), 2),
            "total_units_demanded": float(self.demand.values.sum()),
            "total_units_produced": round(float(total_produced), 2)
        }
