# bth-work-task – Coding Task (PhD application, BTH)

This repo contains the Python solution for **Work Task 2 (coding)**.  
It lets you

1. **Create** the original 500-row `dataset.csv`
2. **Generate** a larger, statistically similar `dataset_synthetic.csv`
3. **Check** that the synthetic data match the original distribution

```
bth-work-task/
├── generate_data.py              <- step 1 – original dataset
├── generate_synthetic_dataset.py <- step 2 – new dataset + similarity tests
├── dataset.csv                   <- sample output of step 1
├── dataset_synthetic.csv         <- sample output of step 2
└── README.md
```

---

## Quick start

```bash
# clone repo
git clone https://github.com/<user>/bth-work-task.git
cd bth-work-task

# (optional) create virtual env
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate

# install dependencies
pip install numpy pandas scipy
```

### 3-line demo

```bash
python generate_data.py              # → dataset.csv   (500 rows)
python generate_synthetic_dataset.py # → dataset_synthetic.csv (2 000 rows)
```

`generate_synthetic_dataset.py` finishes by printing chi-square & KS p-values;  
*p* \> 0.05 indicates the synthetic distribution is statistically close to the original.

---

## Script overview

| Script | Purpose | Key steps |
|--------|---------|-----------|
| **generate_data.py** | Reproduce the task’s original dataset. | Fixed seed = 42, 500 rows. Category probs `[0.2, 0.4, 0.2, 0.1, 0.1]`; two normals (μ 10 σ 2, μ 20 σ 6). |
| **generate_synthetic_dataset.py** | Create a larger dataset *without copying* the exact parameters. | Category probs redrawn with Dirichlet smoothing; means jittered ±5 %, std ±10 %. Exports 2 000 rows and runs chi-square + KS tests. |

Feel free to tweak `N_NEW`, jitter factors, or add plots for deeper validation.

---

## License & contact

MIT License • © 2025 Xiaoran Zhang  