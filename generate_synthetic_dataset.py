#!/usr/bin/env python3
"""
generate_synthetic_dataset.py
--------------------------------
Create a new dataset that is statistically similar to dataset.csv
without re-using the exact sampling parameters.

• Input : dataset.csv
• Output: dataset_synthetic.csv
"""

import pathlib
import numpy as np
import pandas as pd
from scipy import stats


# --------------------------------------------------------------------
# 0. CONFIG
# --------------------------------------------------------------------
ORIG_PATH = pathlib.Path("dataset.csv")
OUT_PATH  = pathlib.Path("dataset_synthetic.csv")
N_NEW     = 2_000          # larger sample size than original
RNG       = np.random.default_rng(seed=17)

# Perturbation factors for mean / std so we do not clone the originals
MEAN_JITTER = 0.05   # ±5 %
STD_JITTER  = 0.10   # ±10 %
DIRICHLET_ALPHA = 1  # prior strength for category smoothing
CHI2_ALPHA      = 0.05
KS_ALPHA        = 0.05


# --------------------------------------------------------------------
# 1. LOAD ORIGINAL DATA
# --------------------------------------------------------------------
df_orig = pd.read_csv(ORIG_PATH, sep=";")
cat_col = "Category1"
num_cols = ["Value1", "Value2"]


# --------------------------------------------------------------------
# 2. FIT SIMPLE EMPIRICAL DISTRIBUTIONS
# --------------------------------------------------------------------
# 2a. Categorical probabilities (with Dirichlet smoothing)
counts = df_orig[cat_col].value_counts().sort_index()
alpha  = counts.values + DIRICHLET_ALPHA
p_hat  = RNG.dirichlet(alpha)           # draws new but close probs
categories = counts.index.tolist()

# 2b. Mean / std for continuous vars (with small jitter)
mu = df_orig[num_cols].mean()
sd = df_orig[num_cols].std(ddof=0)
mu_new = mu * (1 + RNG.uniform(-MEAN_JITTER, MEAN_JITTER, size=len(num_cols)))
sd_new = sd * (1 + RNG.uniform(-STD_JITTER,  STD_JITTER,  size=len(num_cols)))


# --------------------------------------------------------------------
# 3. SYNTHESISE NEW SAMPLES
# --------------------------------------------------------------------
df_new = pd.DataFrame(
    {
        cat_col: RNG.choice(categories, size=N_NEW, p=p_hat),
        num_cols[0]: RNG.normal(mu_new[0], sd_new[0], size=N_NEW),
        num_cols[1]: RNG.normal(mu_new[1], sd_new[1], size=N_NEW),
    }
)

df_new.to_csv(OUT_PATH, sep=";", index=False)
print(f"✔  Saved {N_NEW} synthetic rows to {OUT_PATH}")


# --------------------------------------------------------------------
# 4. QUICK VERIFICATION
# --------------------------------------------------------------------
def check_categorical(original, synthetic):
    # Chi-square goodness of fit
    orig_counts = original.value_counts().sort_index()
    synth_counts = synthetic.value_counts().reindex(orig_counts.index, fill_value=0)
    chi2, p = stats.chisquare(f_obs=synth_counts, f_exp=orig_counts * (len(synthetic) / len(original)))
    return chi2, p

def check_continuous(original, synthetic):
    # Kolmogorov–Smirnov 2-sample test
    return stats.ks_2samp(original, synthetic)


chi2, p_cat = check_categorical(df_orig[cat_col], df_new[cat_col])
print(f"\nCategorical column '{cat_col}': chi²={chi2:.2f}, p={p_cat:.3f}"
      f" -> {'match' if p_cat>CHI2_ALPHA else 'different'}")

for col in num_cols:
    ks_stat, p_val = check_continuous(df_orig[col], df_new[col])
    print(f"Continuous '{col}': KS={ks_stat:.3f}, p={p_val:.3f}"
          f" -> {'match' if p_val>KS_ALPHA else 'different'}")

print("\nDone.")
