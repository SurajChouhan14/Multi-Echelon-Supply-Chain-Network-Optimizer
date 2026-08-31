"""
Multi-Echelon Supply Chain Network Linear Programming Optimizer.
Formulates and solves a 3-Echelon multi-commodity flow optimization problem minimizing total network cost:
1. Raw Material Purchasing & Inbound Transportation Tariffs
2. Plant-Level Production Conversion Costs (with BOM requirements)
3. Finished Goods Outbound Distribution Logistics Costs
"""

import pulp
import pandas as pd
import numpy as np


class SupplyChainOptimizer:
    """
    Exact Linear Programming Solver for Multi-Echelon Supply Chain Networks using PuLP with CBC solver.
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
        Builds and solves the exact supply chain network Linear Program (LP).
        Returns:
            dict containing status, total cost breakdown, and operational flow volumes.
        """
        prob = pulp.LpProblem("Multi_Echelon_Supply_Chain_Optimization", pulp.LpMinimize)

        # Decision Variables (100% Continuous Flow Variables):
        # 1. orders[f, m, s]: Raw material m ordered by factory f from supplier s
        orders = pulp.LpVariable.dicts(
            "orders",
            ((f, m, s) for f in self.factories for m in self.materials for s in self.suppliers),
            lowBound=0, cat=pulp.LpContinuous
        )

        # 2. production_volume[f, p]: Product p produced at factory f
        production_volume = pulp.LpVariable.dicts(
            "prod_vol",
            ((f, p) for f in self.factories for p in self.products),
            lowBound=0, cat=pulp.LpContinuous
        )

        # 3. delivery[f, c, p]: Product p delivered from factory f to customer c
        delivery = pulp.LpVariable.dicts(
            "delivery",
            ((f, c, p) for f in self.factories for c in self.customers for p in self.products),
            lowBound=0, cat=pulp.LpContinuous
        )

        # Objective Function:
        # Min Procurement + Inbound Freight + Production Cost + Outbound Distribution Freight
        prob += (
            pulp.lpSum(
                orders[f, m, s] * (self.mat_cost.loc[s, m] + self.inbound_ship.loc[s, f])
                for f in self.factories for m in self.materials for s in self.suppliers
            )
            + pulp.lpSum(
                production_volume[f, p] * self.prod_cost.loc[f, p]
                for f in self.factories for p in self.products
            )
            + pulp.lpSum(
                delivery[f, c, p] * self.outbound_ship.loc[f, c]
                for f in self.factories for c in self.customers for p in self.products
            )
        )

        # Constraint 1: Supplier Capacity Limits
        for s in self.suppliers:
            for m in self.materials:
                prob += (
                    pulp.lpSum(orders[f, m, s] for f in self.factories) <= float(self.sup_stock.loc[s, m]),
                    f"SupplierCapacity_{s}_{m}"
                )

        # Constraint 2: Factory Production Capacity Limits
        for f in self.factories:
            prob += (
                pulp.lpSum(production_volume[f, p] for p in self.products) <= float(self.prod_cap.loc[f, 'Capacity']),
                f"FactoryCapacity_{f}"
            )

        # Constraint 3: Bill of Materials (BOM) Raw Material Balance
        for f in self.factories:
            for m in self.materials:
                prob += (
                    pulp.lpSum(orders[f, m, s] for s in self.suppliers)
                    >= pulp.lpSum(production_volume[f, p] * float(self.bom.loc[p, m]) for p in self.products),
                    f"BOM_Requirement_{f}_{m}"
                )

        # Constraint 4: Factory Flow Conservation
        for f in self.factories:
            for p in self.products:
                prob += (
                    production_volume[f, p] >= pulp.lpSum(delivery[f, c, p] for c in self.customers),
                    f"FactoryFlow_{f}_{p}"
                )

        # Constraint 5: Customer Demand Satisfaction
        for c in self.customers:
            for p in self.products:
                prob += (
                    pulp.lpSum(delivery[f, c, p] for f in self.factories) >= float(self.demand.loc[p, c]),
                    f"CustomerDemand_{c}_{p}"
                )

        # Solve using PuLP with CBC solver
        solver = pulp.PULP_CBC_CMD(msg=0)
        prob.solve(solver)

        status_str = pulp.LpStatus[prob.status]
        is_optimal = (prob.status == pulp.LpStatusOptimal or prob.status == 1)
        total_cost = float(pulp.value(prob.objective)) if is_optimal else 0.0

        if not is_optimal:
            return {
                "status": status_str,
                "total_optimal_cost": 0.0,
                "procurement_and_inbound_cost": 0.0,
                "manufacturing_cost": 0.0,
                "distribution_shipping_cost": 0.0,
                "total_units_demanded": float(self.demand.values.sum()),
                "total_units_produced": 0.0
            }

        # Calculate cost breakdown
        procurement_cost = sum(
            orders[f, m, s].varValue * (self.mat_cost.loc[s, m] + self.inbound_ship.loc[s, f])
            for f in self.factories for m in self.materials for s in self.suppliers
            if orders[f, m, s].varValue is not None
        )
        manufacturing_cost = sum(
            production_volume[f, p].varValue * self.prod_cost.loc[f, p]
            for f in self.factories for p in self.products
            if production_volume[f, p].varValue is not None
        )
        distribution_cost = sum(
            delivery[f, c, p].varValue * self.outbound_ship.loc[f, c]
            for f in self.factories for c in self.customers for p in self.products
            if delivery[f, c, p].varValue is not None
        )

        total_produced = sum(
            production_volume[f, p].varValue for f in self.factories for p in self.products
            if production_volume[f, p].varValue is not None
        )

        return {
            "status": status_str,
            "total_optimal_cost": round(total_cost, 2),
            "procurement_and_inbound_cost": round(float(procurement_cost), 2),
            "manufacturing_cost": round(float(manufacturing_cost), 2),
            "distribution_shipping_cost": round(float(distribution_cost), 2),
            "total_units_demanded": float(self.demand.values.sum()),
            "total_units_produced": round(float(total_produced), 2)
        }
