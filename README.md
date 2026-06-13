# Informational Health Stress Tests: Signal Disappearance Under Extreme Conditions and the P-value Delusion

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository is a Python simulation that executes "stress tests" by setting boundary conditions for extreme scenarios to demonstrate the destruction of information caused by "social desirability bias" (peer pressure and conformity) in surveys and large-scale data collection.

It mathematically and comprehensively refutes the wishful thinking often found in data science: "If the dissatisfaction is minor, shouldn't it be detectable?", "If someone has strong conviction like an expert, shouldn't they overcome peer pressure?", or "If the sample size is large enough, shouldn't a statistically significant difference be visible?"

---

## 📌 Background

In conventional data analysis, minority voices and outliers are often treated as "statistical noise," or it is widely believed that "increasing the sample size ($N$) to achieve a statistical significance ($p$-value) will solve the problem." However, when the data generation process itself is distorted by social conformity (peer pressure), this common sense leads to fatal errors.

This simulation quantitatively proves the following three bleak realities (stress test results):

1. **Early Disappearance of Proximate Signals (Validation G)**: "Subtle problems" closer to the majority, such as mild dissatisfaction (Rating 2), are rendered invisible by the gravitational pull of conformity much faster than the worst evaluations (Rating 1).
2. **Invalidation of the Expert's Cry (Validation H)**: Even if the minority possesses extremely high confidence (experts) and the majority merely follows the crowd (low confidence), their voices are statistically silenced entirely once the social gravity exceeds a certain threshold.
3. **The Map of P-value Delusion (Validation I)**: As the sample size ($N$) grows enormous, existing statistical tests (like the t-test) will falsely detect even the most minute distortions caused by conformity as "highly significant successes ($p < 0.001$)".

---

## 🧮 Mathematical Model

An individual's final utility ($U_{\text{total}}$) is defined as a linear combination of their intrinsic "true intention" ($U_{\text{true}}$) and extrinsic "conformity" ($U_{\text{sontaku}}$). The selection probability is then calculated via a Softmax function.

$$U_{\text{total}} = (1 - v_2) U_{\text{true}} + v_2 U_{\text{sontaku}}$$

* **$v_2$**: The weight of social desirability (conformity). 0 represents complete honesty, while 1 represents complete conformity.
* **$\beta$**: The respondent's confidence level, which controls the sensitivity of the Softmax function. In Validation H, asymmetric confidence levels ($\beta = 10$ vs $\beta = 2$) are applied to the minority and the majority.

---

## 📊 Outputs

Executing the script creates a `harsh_stress_test_results` directory, generating the following high-resolution graphs (PNG) and raw data (CSV).

* **Fig G: How Subtle Signals Disappear Faster**: A comparison of the disappearance rates between Rating 1 (serious problem) and Rating 2 (subtle problem). This visualizes the process where subtler signals are absorbed by the majority much earlier.
* **Fig H: Certainty ($\beta = 10$) Cannot Prevent Signal Collapse**: A proof of the paradox where even an expert group ($\beta = 10$) experiences signal collapse the moment social pressure ($v_2 = 0.5$) is exceeded.
* **Fig I: The Zone of Statistical Delusion ($N$ vs $v_2$ Heatmap)**: A "map of p-value delusion" in the two-dimensional space of sample size $N$ and conformity $v_2$. This heatmap demonstrates the statistical flaw where an increasing $N$ causes even minuscule biases to be perceived as "significant improvements."

---

## 🚀 Usage

This code can be executed in **Google Colaboratory** or a local Python environment.

1. Run `stress_test_sim.py` (or the Jupyter Notebook format).
2. Upon completion, a `harsh_stress_test_archive.zip` containing the graphs and CSVs will be generated.

### Note on Local Environment Execution
When running in a local Python environment (VSCode, JupyterLab, etc.), do not use the `from google.colab import files` import or the commented-out `files.download(...)` command at the end of the script. Simply execute the script as is, and the ZIP file will be generated in your current working directory.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script
python stress_test_sim.py
