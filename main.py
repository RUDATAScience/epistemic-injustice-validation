import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shutil
import os
from scipy.stats import ttest_ind_from_stats

# ==========================================
# [Setup] Create output directory
# ==========================================
output_dir = "harsh_stress_test_results"
if os.path.exists(output_dir): shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

# --- 1. Core Model with Asymmetric Parameters ---
def u_base(i, peak): return 1.0 - 0.25 * np.abs(i - peak)
def softmax(u, beta):
    ex = np.exp(beta * u)
    return ex / np.sum(ex)

def calculate_dist_stress(v2, beta_minority, beta_majority, min_peak=1):
    options = np.array([1, 2, 3, 4, 5])
    u_true1 = u_base(options, min_peak) # Minority Peak (Can be 1 or 2)
    u_true2 = u_base(options, 3)        # Majority Peak
    u_sontaku = u_base(options, 4)      # Target
    
    p1 = softmax((1 - v2) * u_true1 + v2 * u_sontaku, beta_minority)
    p2 = softmax((1 - v2) * u_true2 + v2 * u_sontaku, beta_majority)
    return 0.10 * p1 + 0.90 * p2

# --- 2. Validation G: Proximity Stress Test (Min Peak = 2) ---
print("Running Validation G: Subtle Signal (Peak=2)...")
v2_range = np.linspace(0, 1, 100)
prob_at_1 = [calculate_dist_stress(v, 5.0, 5.0, min_peak=1)[0] for v in v2_range]
prob_at_2 = [calculate_dist_stress(v, 5.0, 5.0, min_peak=2)[1] for v in v2_range] # Index 1 is Rating 2

plt.figure(figsize=(8, 6))
plt.plot(v2_range, prob_at_1, label='Severe Problem (Peak=1)', linewidth=2)
plt.plot(v2_range, prob_at_2, label='Subtle Problem (Peak=2)', color='orange', linewidth=2)
plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.5)
plt.title("Fig G: How Subtle Signals Disappear Faster", fontsize=14)
plt.xlabel("Sontaku Weight (v2)")
plt.ylabel("Probability of Problem Observation")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(output_dir, 'fig_G_proximity_test.png'), dpi=300)
plt.close()

# --- 3. Validation H: Asymmetric Certainty (Expert Minority vs Crowd) ---
print("Running Validation H: Expert Minority vs Hesitant Majority...")
v2_range = np.linspace(0, 1, 100)
# Minority is certain (beta=10), Majority is uncertain (beta=2)
prob_expert = [calculate_dist_stress(v, 10.0, 2.0, min_peak=1)[0] for v in v2_range]

plt.figure(figsize=(8, 6))
plt.plot(v2_range, prob_expert, color='purple', linewidth=3)
plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.5)
plt.title("Fig H: Certainty (Beta=10) cannot prevent Signal Collapse", fontsize=14)
plt.xlabel("Sontaku Weight (v2)")
plt.ylabel("Prob(Rating 1)")
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(output_dir, 'fig_H_asymmetric_beta.png'), dpi=300)
plt.close()

# --- 4. Validation I: The P-Value Delusion Map (N vs v2) ---
print("Running Validation I: P-Value Heatmap...")
v2_space = np.linspace(0, 0.8, 30)
n_space = np.logspace(2, 6, 30) # N=100 to N=1,000,000
p_map = np.zeros((len(n_space), len(v2_space)))

# Baseline (v2=0, beta=5)
dist_base = calculate_dist_stress(0.0, 5.0, 5.0)
mean_base = np.sum(np.arange(1,6) * dist_base)
std_base = np.sqrt(np.sum((np.arange(1,6) - mean_base)**2 * dist_base))

for i, n in enumerate(n_space):
    for j, v in enumerate(v2_space):
        dist = calculate_dist_stress(v, 5.0, 5.0)
        mean_v = np.sum(np.arange(1,6) * dist)
        std_v = np.sqrt(np.sum((np.arange(1,6) - mean_v)**2 * dist))
        
        # Calculate p-value (approx)
        t_stat = (mean_v - mean_base) / np.sqrt((std_base**2/n) + (std_v**2/n))
        # We focus on the log of p-value to see the scale
        p_map[i, j] = np.log10(1 - ttest_ind_from_stats(mean_base, std_base, int(n), 
                                                        mean_v, std_v, int(n))[1] + 1e-100)

plt.figure(figsize=(10, 8))
sns.heatmap(p_map, xticklabels=np.round(v2_space, 2), yticklabels=np.round(np.log10(n_space), 1),
            cmap="viridis", cbar_kws={'label': 'Significance Confidence (Log Scale)'})
plt.title("Fig I: The Zone of Statistical Delusion (N vs v2)", fontsize=14)
plt.xlabel("Sontaku Weight (v2)")
plt.ylabel("Sample Size N (Log10)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fig_I_p_value_heatmap.png'), dpi=300)
plt.close()

# --- 5. Zip and Download ---
df_i = pd.DataFrame(p_map, columns=np.round(v2_space, 2), index=np.round(n_space, 0))
df_i.to_csv(os.path.join(output_dir, 'data_I_p_heatmap.csv'))

shutil.make_archive("harsh_stress_test_archive", 'zip', output_dir)
print("✅ Done. 'harsh_stress_test_archive.zip' is ready.")

# Download if in Colab:
# from google.colab import files
# files.download("harsh_stress_test_archive.zip")
