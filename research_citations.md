# Complete Citation List for Scotland AI Split-Zones Framework

> **Last updated:** July 2026  
> **Coverage:** Stages 1–5 (Constraint Direction → Empirical Validation → Battery Sizing → Merchant Stacking → Behind-the-Meter)

---

## 1. UK & Scottish Government Policy Documents

### AI Growth Zones Programme

- UK Government. (2026). *AI Growth Zones open for applications.* https://www.gov.uk/government/publications/ai-growth-zones/ai-growth-zones-open-for-applications
- UK Government. (2026). *Delivering AI Growth Zones.* https://www.gov.uk/government/publications/delivering-ai-growth-zones/delivering-ai-growth-zones
- UK Parliament. (2026). *Written Statement HCWS1289 — Lanarkshire AI Growth Zone.* https://questions-statements.parliament.uk/written-statements/detail/2026-01-29/hcws1289

### Scottish AI Strategy

- Scottish Government. (2026). *Scotland's Artificial Intelligence Strategy 2026-2031.* https://www.gov.scot/publications/scotlands-ai-strategy-2026-2031/
- Scottish Government. (2026). *AI Strategy Actions.* https://www.gov.scot/publications/scotlands-ai-strategy-2026-2031/pages/6/

### Lanarkshire AI Growth Zone

- DataVita. (2026). *Lanarkshire AI Growth Zone FAQs.* https://www.datavita.co.uk/lanarkshire-ai-growth-zone/faqs

---

## 2. NESO Data Sources (with Exact Resource IDs)

### Constraint Breakdown Data

- NESO. (2024). *Constraint Breakdown 2023-2024.* Resource ID: `24d067d8-1328-452a-9720-21cb691e491e`. Package ID: `fb56b46e-cef3-4eb8-9294-0ca19769b7eb`. https://www.neso.energy/data-portal

### Thermal Constraint Costs (Boundary-Specific)

- NESO. (2024). *Thermal Constraint Costs Data 23-24.* Resource ID: `75c9c564-af38-4421-a461-a612a6921212`. Package ID: `f0055054-c55c-4068-a01c-61da4334e58f`.
  - Schema: `_id`, `Settlement Date`, `Constraint Group`, `Daily Cost (GBP)`
  - Constraint Groups: ESTEX, SCOTEX, SEIMP, SSE-SP, SSHARN, SWALEX

### Day Ahead Constraint Flows and Limits

- NESO. (2024). *Day Ahead Constraint Flows and Limits.* Resource ID: `38a18ec1-9e40-465d-93fb-301e80fd1352`. Package ID: `cf3cbc92-2d5d-4c2b-bd29-e11a21070b26`.
  - Schema: `_id`, `Constraint Group`, `Date (GMT/BST)`, `Limit (MW)`, `Flow (MW)`
  - Constraint Groups: ESTEX, FLOWSTH, GALLEX, SCOTEX, SEIMP, SHARN, SSE-SP, SSEN-S, SWALEX
  - Filter Rule: Strict `year.is_in([2023, 2024])` filter required to eliminate synthetic forward-forecast artifacts.

### Transmission System Boundaries & Services

- NESO. (2024). *ETYS 2024 GB Transmission System Boundaries.* Resource ID: `e914fcec-1dc9-4f1f-97e7-59c0d9521bea`. Package ID: `997f4820-1ad4-499b-b1fe-4b8d3d7fbc72`.
- NESO. *Local Constraint Market.* https://www.neso.energy/industry-information/balancing-services/local-constraint-market
- NESO. *Connections Reform Results.* https://www.neso.energy/industry-information/connections-reform/connections-reform-results
- Ofgem. *Demand Connections Reform.* https://www.ofgem.gov.uk/call-for-input/demand-connections-reform

---

## 3. Battery Energy Storage Market Data (Stage 4)

### Modo Energy GB BESS Revenue Benchmarks

- Modo Energy. (2026, March). *ME BESS GB Monthly Revenue Release — February 2026.* (£41,000/MW/year annualised run-rate).
- Modo Energy. (2026, May). *"How does a BESS make money?"* (12-month rolling average for 2-hour duration systems: £73,145/MW/year).

### Battery Revenue Cannibalisation Evidence

- Modo Energy. (2026, February 3). *Why were ERCOT battery revenues so low in 2025? Weather, energy arbitrage, and buildout.* Modo Energy Research. https://modoenergy.com/research/why-were-ercot-battery-revenues-so-low-in-2025-weather-energy-arbitrage-builodout
- ERCOT Queue. (2026, February). *ERCOT battery revenue, by product: Fleet-average merchant battery earnings (2022–2025).* ERCOTQueue Chartbook & Analytics. https://www.ercotqueue.com/charts/battery-revenue-stack
- Castagneto Gissey, G., et al. (UCL Bartlett School of Sustainable Construction / UCL Energy Institute). *Energy Storage Market Saturation and Revenue Stacking Dynamics in Great Britain's Frequency Response Markets.* Working Paper, University College London.

---

## 4. Network Charge Tariffs & Regulatory Framework (Stage 5)

- SSEN. (2027). *Scottish Hydro Electric Power Distribution — Schedule of Charges and Other Tables — April 2027 v1.0.* https://www.ssen.co.uk/globalassets/library/charging-statements-shepd/202728/shepd---schedule-of-charges-and-other-tables---april-2027-v1.0.xlsx
- Ofgem. (2023). *Targeted Charging Review — Implementation.* https://www.ofgem.gov.uk/environmental-and-social-schemes/targeted-charging-review
- Ofgem. (2024-2026). *Access and Forward-Looking Charges Reform.* https://www.ofgem.gov.uk/electricity/networks-and-connections/access-and-forward-looking-charges-reform
- NESO. (2024-2026). *Demand Flexibility Service.* https://www.neso.energy/industry-information/balancing-services/demand-flexibility-service

---

## 5. Academic Papers on AI/ML Checkpointing & Distributed Training

### Checkpointing Systems

- Xu, W., Huang, X., Meng, S., Zhang, W., Guo, L., & Sato, K. (2024). An efficient checkpointing system for large machine learning model training. In *Proceedings of the SC24 Workshops of the International Conference for High Performance Computing, Networking, Storage and Analysis*.
- Sun, M., et al. (2026). *LLMTailor: A layer-wise tailoring tool for efficient checkpointing of large language models*. arXiv preprint arXiv:2602.22158.

### Distributed Training & LLM Infrastructure

- Dubey, A., Jauhri, A., Pandey, A., et al. (2024). *The LLaMA 3 Herd of Models*. arXiv preprint arXiv:2407.21783.
- Chowdhery, A., et al. (2022). *PaLM: Scaling Language Modeling with Pathways*. arXiv:2204.02311.
- Dean, J., et al. (2023). Pathways: Asynchronous Distributed Dataflow for ML. *Proceedings of MLSys 2023*.
- Rajbhandari, S., et al. (2020). ZeRO: Memory Optimizations Toward Training Trillion Parameter Models. *In Proceedings of SC20: International Conference for High Performance Computing*.

---

## 6. Industry & Hyperscaler Documentation

- Microsoft. (2024). *Checkpoint and resume training jobs in Azure Machine Learning.* Azure Documentation. https://learn.microsoft.com/en-us/azure/machine-learning/
- Google Cloud. (2024). *Checkpointing best practices for TPU VMs.* TPU Documentation. https://cloud.google.com/tpu/docs/
- Amazon Web Services. (2024). *Checkpoint and resume SageMaker training jobs.* SageMaker Documentation. https://docs.aws.amazon.com/sagemaker/