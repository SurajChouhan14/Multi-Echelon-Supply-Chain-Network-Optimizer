# Multi-Echelon Supply Chain Network Optimization Engine

An exact Operations Research engine implementing **Mixed-Integer Linear Programming (MILP)** to minimize total procurement, multi-tier inbound transportation, manufacturing conversion (with multi-material Bill of Materials BOM constraints), and outbound distribution costs across **5 Suppliers, 3 Assembly Plants, and 4 Regional Customer Markets**.

---

## 1. System Architecture

```
                                 +-------------------------------------+
                                 | 5 Raw Material Suppliers            |
                                 | (Materials A, B, C, D)              |
                                 +------------------+------------------+
                                                    | Inbound Freight (c_sm)
                                                    v
                                 +-------------------------------------+
                                 | 3 Manufacturing Plants              |
                                 | (BOM Conversion & Prod Capacities)  |
                                 +------------------+------------------+
                                                    | Outbound Freight (c_fc)
                                                    v
                                 +-------------------------------------+
                                 | 4 Regional Customer Markets         |
                                 | (100% Demand Satisfaction)          |
                                 +-------------------------------------+
```

---

## 2. Mathematical Formulation

### **Objective Function (Total Network Cost Minimization)**:
$$\min \sum_{f} \sum_{m} \sum_{s} \text{orders}_{fms} \cdot (\text{MatCost}_{sm} + \text{InboundRate}_{sf}) + \sum_{f} \sum_{p} \text{vol}_{fp} \cdot \text{ProdCost}_{fp} + \sum_{f} \sum_{c} \sum_{p} \text{delivery}_{fcp} \cdot \text{OutboundRate}_{fc}$$

### **Operational Constraints**:
1. **Supplier Availability Limits**: $\sum_{f} \text{orders}_{fms} \le \text{SupplierStock}_{sm} \quad \forall s, m$
2. **Plant Capacity Bounds**: $\sum_{p} \text{vol}_{fp} \le \text{PlantCapacity}_{f} \quad \forall f$
3. **Bill of Materials (BOM) Balance**: $\sum_{s} \text{orders}_{fms} \ge \sum_{p} \text{vol}_{fp} \cdot \text{BOM}_{pm} \quad \forall f, m$
4. **Plant Flow Conservation**: $\text{vol}_{fp} \ge \sum_{c} \text{delivery}_{fcp} \quad \forall f, p$
5. **Customer Demand Satisfaction**: $\sum_{f} \text{delivery}_{fcp} \ge \text{Demand}_{pc} \quad \forall c, p$

---

## 3. Exact Computed Benchmark Results (7,500 Units Total Demand)

```
===============================================================================================
MULTI-ECHELON SUPPLY CHAIN NETWORK OPTIMIZATION ENGINE
===============================================================================================
  * Optimization Status        : Optimal
  * Total Minimum Network Cost : $986,882.96
  * Raw Material Procurement   : $839,235.23  (85.0% of total expenditure)
  * Plant Manufacturing Cost   : $121,486.36  (12.3% of total expenditure)
  * Outbound Distribution Cost : $26,161.36   ( 2.7% of total expenditure)
  * Total Production Volume    : 7,500 units (100.0% Customer Demand Satisfaction)
===============================================================================================
```

---

## 4. Quick Start & Execution

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run exact MILP optimization pipeline
python run_pipeline.py

# 3. Run automated unit tests
python test_supply_chain.py
```

---

## 5. Master Placement Resume Description

> **Multi-Echelon Supply Chain Network Optimizer (MILP)**
> * Formulated an end-to-end Mixed-Integer Linear Program (MILP) in Python/PuLP optimizing a multi-tier manufacturing network spanning 5 suppliers, 3 plants, and 4 regional customer markets.
> * Implemented Bill of Materials (BOM) multi-material conversion balances, supplier capacity limits, and multi-modal transportation tariffs.
> * Achieved \$986,882 global cost minimization with 100% customer order fulfillment across 7,500 units of weekly demand.

---

## License
MIT License. Open for academic research and portfolio demonstration.
