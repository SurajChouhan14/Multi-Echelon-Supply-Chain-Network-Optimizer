"""
Multi-Echelon Supply Chain Network Topology & Parameters Ingestion Module.
Defines a deterministic 3-Echelon multi-commodity network topology:
- 5 Raw Material Suppliers
- 3 Manufacturing Assembly Plants
- 4 Regional Customer Markets
- 4 Raw Material Categories & 4 Finished Product BOM Requirements
"""

import pandas as pd


class SupplyChainDataLoader:
    """
    Data generator and loader for Multi-Echelon Supply Chain Network Optimization.
    Provides deterministic topological parameters and operational constraints.
    """

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load_network_data(self):
        """
        Loads the deterministic multi-echelon supply chain parameters:
        1. Supplier stock & pricing
        2. Inbound/Outbound shipping tariffs
        3. Factory capacities & production costs
        4. Bill of Materials (BOM) & Customer demands
        """
        suppliers = ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D', 'Supplier E']
        materials = ['Material A', 'Material B', 'Material C', 'Material D']
        factories = ['Factory A', 'Factory B', 'Factory C']
        products = ['Product A', 'Product B', 'Product C', 'Product D']
        customers = ['Customer A', 'Customer B', 'Customer C', 'Customer D']

        # 1. Supplier Stock (units)
        df_sup_stock = pd.DataFrame(
            [[4000, 4500, 3800, 5000],
             [5000, 3900, 4200, 3700],
             [3800, 4800, 4500, 4000],
             [4500, 3800, 5000, 4500],
             [3900, 4200, 4000, 4800]],
            index=suppliers, columns=materials
        )

        # 2. Raw Material Costs ($/unit)
        df_mat_cost = pd.DataFrame(
            [[12.5, 15.0, 18.0, 10.0],
             [11.0, 16.5, 17.0, 11.5],
             [13.0, 14.0, 19.0, 9.5],
             [12.0, 15.5, 17.5, 10.5],
             [11.5, 16.0, 18.5, 10.0]],
            index=suppliers, columns=materials
        )

        # 3. Inbound Raw Material Shipping Tariffs ($/unit)
        df_inbound_ship = pd.DataFrame(
            [[2.5, 3.0, 4.5],
             [3.0, 2.0, 3.5],
             [4.0, 3.5, 2.0],
             [2.0, 4.0, 3.0],
             [3.5, 2.5, 2.5]],
            index=suppliers, columns=factories
        )

        # 4. Bill of Materials (BOM) Requirements
        df_bom = pd.DataFrame(
            [[2, 1, 1, 2],
             [1, 3, 2, 1],
             [3, 1, 2, 2],
             [2, 2, 1, 3]],
            index=products, columns=materials
        )

        # 5. Factory Production Capacity (units)
        df_prod_cap = pd.DataFrame(
            {'Capacity': [3000, 3500, 2800]},
            index=factories
        )

        # 6. Factory Conversion / Production Cost ($/unit)
        df_prod_cost = pd.DataFrame(
            [[15.0, 18.0, 14.0, 20.0],
             [14.0, 17.0, 15.0, 19.0],
             [16.0, 16.5, 13.5, 21.0]],
            index=factories, columns=products
        )

        # 7. Customer Demand (units)
        df_demand = pd.DataFrame(
            [[400, 600, 350, 500],
             [500, 300, 450, 600],
             [350, 550, 600, 400],
             [600, 450, 500, 350]],
            index=products, columns=customers
        )

        # 8. Outbound Finished Goods Shipping Tariffs ($/unit)
        df_outbound_ship = pd.DataFrame(
            [[3.5, 4.0, 5.0, 6.0],
             [5.0, 3.0, 4.5, 4.0],
             [6.0, 5.5, 3.0, 3.5]],
            index=factories, columns=customers
        )

        return {
            'suppliers': suppliers,
            'materials': materials,
            'factories': factories,
            'products': products,
            'customers': customers,
            'supplier_stock': df_sup_stock,
            'material_cost': df_mat_cost,
            'inbound_shipping': df_inbound_ship,
            'bom': df_bom,
            'production_capacity': df_prod_cap,
            'production_cost': df_prod_cost,
            'customer_demand': df_demand,
            'outbound_shipping': df_outbound_ship
        }
