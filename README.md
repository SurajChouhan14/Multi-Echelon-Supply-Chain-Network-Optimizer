# Multi-Echelon Supply Chain Network Flow Optimizer
> **Exact 3-Echelon Multi-Commodity Linear Program (LP) for Procurement, Plant Manufacturing, and Outbound Customer Distribution via PuLP with CBC solver**  
> *Operations Research · Supply Chain Optimization · Linear Programming · Multi-Commodity Network Flow · PuLP / CBC · Cost Minimization*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/SurajChouhan14/Multi-Echelon-Supply-Chain-Network-Optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/SurajChouhan14/Multi-Echelon-Supply-Chain-Network-Optimizer/actions)
[![Benchmark](https://img.shields.io/badge/benchmark-7%2C500%20Units%20Demanded-blue.svg)]()
[![Tests](https://img.shields.io/badge/tests-5%20passed-brightgreen.svg)]()

---

## 🎯 Executive Overview & Architecture
Global manufacturing enterprises face complex multi-echelon cost trade-offs across raw material procurement tariffs, plant-level manufacturing conversion costs, and outbound distribution logistics to customer demand markets.

This repository implements a **Pure Linear Program (LP)** solving the 3-echelon multi-commodity supply chain network flow problem to **proven global optimality**:
1. **Tier 1 (Procurement & Inbound Freight):** Optimizes raw material purchasing allocations across 5 global suppliers subject to individual material stock bounds.
2. **Tier 2 (Manufacturing & BOM Balance):** Enforces plant throughput production capacities and multi-material Bill-of-Materials (BOM) component conversion equations.
3. **Tier 3 (Outbound Customer Distribution):** Optimizes multi-commodity transportation flows across 4 regional customer demand markets to guarantee 100% on-time fulfillment at minimum total cost.

```
  ┌────────────────────────────────────────────────────────┐
  │ 5 Raw Material Suppliers (Materials A, B, C, D)        │
  └───────────────────────────┬────────────────────────────┘
                              │ Inbound Freight ($/unit)
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3 Assembly Manufacturing Plants (Capacities A, B, C)   │
  │ • Bill of Materials (BOM) Component Balance Equations  │
  │ • Plant Throughput Limits (Capacity <= 9,300 units)    │
  └───────────────────────────┬────────────────────────────┘
                              │ Outbound Freight ($/unit)
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 4 Regional Customer Markets (Demands: 7,500 Units)     │
  │ • 100% Exact Demand Fulfillment Guaranteed             │
  │ • Global Network Cost Minimized: $986,883.00           │
  └────────────────────────────────────────────────────────┘
```

---

## 📊 Benchmark Execution & Validation Report

### Deterministic 3-Echelon Benchmark Instance (7,500 Units Demanded)

| Metric | Measured Value | Verification Method | Operational Definition |
|---|:---:|:---:|---|
| **Instance Provenance** | **$7,500	ext{ Units Demanded}$** | Synthetic 3-Echelon Topology | 5 suppliers, 3 assembly plants, 4 regional markets, 4 finished products, 4 raw materials |
| **Formulation Class** | **Pure Linear Program (LP)** | $100\%$ Continuous Variables | $0.0\%$ integrality gap; solved to proven global optimality |
| **Solver Engine** | **PuLP with CBC solver** | Primal-Dual Simplex | Verified global convergence in under 0.05 seconds |
| **Global Minimized Cost** | **$\$986,882.96	ext{ (~}\$986,883	ext{)}$** | Exact LP Objective | Total minimum expenditure across procurement, manufacturing, and distribution |
| **Procurement & Inbound** | **$\$839,235.23	ext{ (}85.04\%	ext{)}$** | Purchasing + Shipping | Sourcing costs for all raw materials across 5 suppliers |
| **Plant Manufacturing** | **$\$121,486.36	ext{ (}12.31\%	ext{)}$** | Conversion Cost Matrix | Assembly and production conversion costs across 3 manufacturing plants |
| **Outbound Distribution** | **$\$26,161.36	ext{ (}2.65\%	ext{)}$** | Outbound Freight Tariffs | Logistics shipping costs delivering finished products to 4 customer markets |
| **Demand Fulfillment** | **$100.0\%	ext{ (}7,500 / 7,500	ext{)}$** | Flow Conservation Balance | 7,500 units produced and delivered with zero unmet demand |

---

## 📁 Repository Structure

```text
Multi-Echelon-Supply-Chain-Network-Optimizer/
├── .github/
│   └── workflows/
│       └── ci.yml                      # Automated CI test & benchmark workflow
├── results/
│   └── final_benchmark.txt             # Frozen solver execution report
├── src/
│   ├── data_loader.py                  # Network topology & parameter ingestion
│   └── supply_chain_optimizer.py       # PuLP LP formulation & CBC solver engine
├── requirements.txt                    # Dependencies (pulp, pandas, numpy)
├── run_pipeline.py                     # Pipeline execution & cost breakdown logger
└── test_supply_chain.py                # 5 unit, sensitivity & infeasibility tests
```

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/SurajChouhan14/Multi-Echelon-Supply-Chain-Network-Optimizer.git
cd Multi-Echelon-Supply-Chain-Network-Optimizer
pip install -r requirements.txt
```

### 2. Run Optimization Pipeline
```bash
python run_pipeline.py
```

### 3. Run Test Suite
```bash
python test_supply_chain.py
```
