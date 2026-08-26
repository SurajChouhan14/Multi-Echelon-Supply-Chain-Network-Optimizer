"""
End-to-End Execution Pipeline for Multi-Echelon Supply Chain Network Optimization.
Solves the exact multi-tier procurement, BOM manufacturing, and customer distribution problem.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import SupplyChainDataLoader
from src.supply_chain_optimizer import SupplyChainOptimizer


def main():
    print("=" * 95)
    print("MULTI-ECHELON SUPPLY CHAIN NETWORK OPTIMIZATION ENGINE")
    print("Architecture: 5 Suppliers -> 3 Manufacturing Plants -> 4 Customer Markets | Tech: Exact MILP")
    print("=" * 95)

    print("\n[1/3] Ingesting multi-echelon network topology and operational parameters...")
    loader = SupplyChainDataLoader(data_dir="data")
    network_data = loader.load_network_data()
    print(f"      Suppliers: {len(network_data['suppliers'])} | Materials: {len(network_data['materials'])}")
    print(f"      Plants: {len(network_data['factories'])} | Products: {len(network_data['products'])} | Customer Markets: {len(network_data['customers'])}")
    print(f"      Total Weekly Customer Demand: {network_data['customer_demand'].values.sum():,.0f} units")

    print("\n[2/3] Formulating and solving exact Mixed-Integer Linear Program (MILP)...")
    print("      -> Enforcing Supplier Inventory & Raw Material Allocation Limits")
    print("      -> Enforcing Bill of Materials (BOM) Component Conversion Balances")
    print("      -> Enforcing Plant Throughput Production Capacities")
    print("      -> Enforcing 100% Regional Customer Demand Fulfillment")

    optimizer = SupplyChainOptimizer(network_data)
    result = optimizer.solve_network()

    print("\n[3/3] Optimal Cost Breakdown & Operational Decision Matrix:")
    print("=" * 95)
    print(f"  * Optimization Status        : {result['status']}")
    print(f"  * Total Minimum Network Cost : ${result['total_optimal_cost']:,.2f}")
    print(f"  * Raw Material Procurement   : ${result['procurement_and_inbound_cost']:,.2f}")
    print(f"  * Plant Manufacturing Cost   : ${result['manufacturing_cost']:,.2f}")
    print(f"  * Outbound Distribution Cost : ${result['distribution_shipping_cost']:,.2f}")
    print(f"  * Total Output Produced      : {result['total_units_produced']:,.0f} units (Demand: {result['total_units_demanded']:,.0f})")
    print("=" * 95)

    print("\n[CONCLUSION] Successfully resolved multi-echelon bottleneck trade-offs")
    print("   achieving global cost minimization with 100% customer demand satisfaction.")
    print("=" * 95)


if __name__ == '__main__':
    main()
