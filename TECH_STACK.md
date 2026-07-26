# Technology Stack: Scotland AI Split-Zones

This project is built on a modern, high-performance, and strictly auditable Python data stack. The technology choices are driven by three core principles:
1. **Auditability & Reproducibility**: Every assumption must be traceable, and the pipeline must run identically on any machine.
2. **Performance**: Processing sensitivity matrices and grid scenarios requires fast, memory-efficient tabular operations.
3. **Strict Typing & Validation**: "Configuration, not magic numbers." All inputs are validated against strict schemas before any computation occurs.

---

## 1. Core Runtime & Environment
- **Python 3.11+**: The core language, chosen for its mature data science ecosystem, strong typing capabilities, and performance improvements in recent versions.
- **`uv` (by Astral)**: The ultra-fast Python package and project manager. It replaces `pip`, `pip-tools`, and `virtualenv`, providing deterministic, lockfile-based environment resolution in milliseconds. 
  - *Why:* Guarantees that the environment used to generate the Adversarial Review Kit is bit-for-bit reproducible by any reviewer.

## 2. Data Processing & Computation
- **Polars**: The primary DataFrame library for all tabular data manipulation.
  - *Why:* Blazingly fast, memory-efficient, and features a powerful expression API that prevents silent failures. Its lazy evaluation and strict schema enforcement align perfectly with the project's "Fail Loudly" manifesto rule.
2. **DuckDB**: Embedded analytical SQL database.
  - *Why:* Used for complex, multi-table joins or aggregations that are more naturally expressed in SQL, running directly on Parquet files without loading everything into memory.
- **NumPy & SciPy**: Used sparingly for specific vectorised mathematical operations and sensitivity distribution modelling where Polars' native functions are insufficient.

## 3. Configuration & Validation
- **PyYAML**: For human-readable configuration files (e.g., `workload_flexibility_assumptions.yml`).
- **Pydantic**: For strict data validation.
  - *Why:* Ensures that every YAML configuration file is validated against a strict Python schema *before* the model runs. If a notice period is missing or a fraction is > 1.0, the model fails immediately with a clear error, preventing "garbage in, garbage out."

## 4. Data Storage & Handoffs
- **Apache Parquet**: The exclusive format for intermediate and processed data (e.g., `data/intermediate/*.parquet`).
  - *Why:* Columnar, highly compressed, and preserves strict data types (unlike CSV). It enforces the **Parquet Handoff Rule**: notebooks communicate via typed, versioned data files, not hidden in-memory variables.

## 5. Visualization & Reporting
- **Matplotlib**: The primary library for generating static, publication-ready figures.
  - *Why:* Provides granular, programmatic control over every pixel, allowing us to enforce Tufte-compliant design principles (e.g., explicit annotations, removed chart junk, precise color coding for grid burden vs. absorption).

## 6. Development & Quality Assurance
- **JupyterLab**: The interactive interface for exploratory data analysis and narrative-driven notebook execution.
- **Ruff**: The ultra-fast Python linter and code formatter.
  - *Why:* Enforces PEP 8 compliance and catches potential bugs (like unused variables or undefined names) instantly, keeping the codebase clean and professional.
- **Pytest**: For unit testing core logic extracted into the `src/ai_split_zones/` module.

---

## Architecture Diagram (Logical Flow)

```text
[ configs/*.yml ]  --> (Pydantic Validation) --> [ Strict Python Objects ]
       |                                               |
       v                                               v
[ data/raw/*.csv ] --> (Polars Ingestion) ---> [ data/intermediate/*.parquet ]
                                                       |
                                                       v
[ notebooks/01-05 ] --> (Polars/DuckDB Compute) -> [ data/processed/*.parquet ]
                                                       |
                                                       v
                                                [ figures/*.png ]
                                                [ adversarial_review_kit/ ]

## Getting Started
To replicate this exact stack:

# 1. Clone the repository
git clone <repository-url>
cd scotland-ai-split-zones

# 2. Install dependencies and create the virtual environment (via uv)
uv sync

# 3. Launch the interactive environment
uv run jupyter lab

# 4. Run quality checks
uv run ruff check .
uv run pytest

Note: This stack is deliberately lightweight and avoids heavy, opaque machine learning frameworks (like TensorFlow or PyTorch). This is a deterministic, physics-based constraint model, not a predictive AI black box.

