# 📦 Multi-Echelon Supply Chain Network Flow Optimizer
### 3-Echelon Mixed-Integer Linear Program (MILP) | Multi-Material BOM Balance | Multi-Commodity Flow | SciPy HiGHS

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Optimization](https://img.shields.io/badge/Solver-HiGHS%20%2F%20MILP-success.svg)](https://highs.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A multi-echelon supply chain network design and commodity flow optimization platform formulating large-scale Mixed-Integer Linear Programs (MILP). Simultaneously optimizes supplier procurement, assembly plant manufacturing, Bill-of-Materials (BOM) conversions, and regional distribution center freight routing.

---

## 📌 Problem Formulation & Conservation Constraints

```
 5 Raw Material Suppliers ──(Inbound Freight)──> 3 Manufacturing Assembly Plants
                                                          │
                                                (Multi-Material BOM Conversion)
                                                          │
                                                          ▼
 4 Regional Customer Markets <──(Outbound Freight)── 3 Assembly Plants
```

### Flow Conservation & Bill-of-Materials (BOM) Balance:
$$\sum_{s \in S} x_{smk} = \sum_{p \in P} B_{kp} \cdot y_{mp}, \quad \forall m \in M, \; k \in K$$
$$\sum_{m \in M} z_{mpc} = D_{pc}, \quad \forall p \in P, \; c \in C$$

---

## 📊 Industrial Case Study & Benchmark Performance
* **Network Topology:** 5 Tier-1 Suppliers $\to$ 3 Assembly Plants $\to$ 4 Regional Customer Markets.
* **Commodities:** 4 Raw Material types converted into 4 Finished Goods product lines.
* **Weekly Demand:** **7,500 finished goods units**.
* **Global Network Minimum Cost:** **\$986,883** ($100\%$ customer demand satisfied).
  * Inbound Raw Material Procurement & Freight: **\$839,235.23 (85.0%)**
  * Plant Manufacturing Conversion Cost: **\$121,486.36 (12.3%)**
  * Outbound Customer Distribution Freight: **\$26,161.36 (2.7%)**
* **Solver Convergence:** Solved in $< 0.10\text{s}$ using SciPy HiGHS.

---

## 📂 Repository Structure
```
Multi-Echelon-Supply-Chain-Network-Optimizer/
├── src/
│   ├── supply_chain_solver.py      # MILP network flow formulation & solver
│   └── data_loader.py              # Network topology, BOM matrix & cost tables
├── Multi_Echelon_Supply_Chain.ipynb # Interactive execution notebook
├── run_pipeline.py                 # Pipeline execution script
├── test_supply_chain.py            # Unit testing suite (4/4 passing)
└── requirements.txt                # Production dependencies
```

---

## 🚀 Quickstart & Reproducibility
```bash
git clone https://github.com/SurajChouhan14/Multi-Echelon-Supply-Chain-Network-Optimizer.git
cd Multi-Echelon-Supply-Chain-Network-Optimizer
pip install -r requirements.txt
python run_pipeline.py
python -m unittest test_supply_chain.py
```
