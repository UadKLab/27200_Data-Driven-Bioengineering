# Week 4 — Experimental Design and Statistical Inference

**Date:** 24 September 2026
**Instructors:** Mikael & Ajuna
**Theme:** Inference is bounded by design, variability, and assumptions.

Three exercise notebooks and two notebooks for the group assignment. All run in Colab.

> **The exercise notebooks are in R.** Colab opens them with an R runtime automatically. The first
> cell installs the `beeswarm` package, which takes about a minute.

---

## Exercises

### 1 · t-tests and p-values

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/notebooks/T_test_R.ipynb)

**[notebooks/T_test_R.ipynb](notebooks/T_test_R.ipynb)** — simulate two groups, plot them and run a
t-test. Change the means, the spread and the sample size and see how the p-value responds. The second
part runs 100 tests at once and applies Bonferroni and Benjamini–Hochberg corrections.

### 2 · ANOVA and linear regression

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/notebooks/ANOVA_R.ipynb)

**[notebooks/ANOVA_R.ipynb](notebooks/ANOVA_R.ipynb)** — compare three groups with an ANOVA and
Tukey's post-hoc test, then fit a linear regression with `lm()` and interpret the slope, intercept
and R².

### 3 · Non-normality and transformations

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/notebooks/Nonnormal_R.ipynb)

**[notebooks/Nonnormal_R.ipynb](notebooks/Nonnormal_R.ipynb)** — skewed data: a log transform with
a normality check, and the Wilcoxon test as a non-parametric alternative.

---

## Group assignment — power and sample size

The assignment brief and case allocation are on DTU Learn. These notebooks contain the calculations
you need. They have the same content in Python and in R; use either.

| | |
|---|---|
| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/power/27200_W4_power_python.ipynb) | **[power/27200_W4_power_python.ipynb](power/27200_W4_power_python.ipynb)** — Python (`statsmodels`) |
| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/power/27200_W4_power_R.ipynb) | **[power/27200_W4_power_R.ipynb](power/27200_W4_power_R.ipynb)** — R (base R and `pwr`) |

| Section | Content |
|---|---|
| 1 | Two groups: sample size, detectable difference, dropout, power curves |
| 2 | Repeated measurements of the same unit |
| 3 | Two proportions, including unequal group sizes |
| 4 | Many tests at once: Bonferroni and FDR |
| 5 | Paired designs |
| 6 | More than two groups, normality checks, non-parametric tests |
| 7 | Power by simulation, for designs without a formula |

---

## Reading

Vaux, D. *Know when your numbers are significant.* Nature **492**, 180–181 (2012).

Krzywinski & Altman, *Points of Significance* series, Nature Methods.
