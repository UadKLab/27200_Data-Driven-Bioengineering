# Week 4 — Experimental Design and Statistical Inference

**Date:** 24 September 2026
**Instructors:** Mikael & Ajuna
**Theme:** Inference is bounded by design, variability, and assumptions.

Three short exercise notebooks, then a set of tools for the group assignment. Everything runs in
Colab — nothing to install.

> **These notebooks are written in R, not Python.** Colab starts an R runtime for them
> automatically; you do not need to change anything. The first cell of each installs the `beeswarm`
> plotting package, which takes about a minute. Let it finish before running the rest.

---

## Exercises

### 1 · t-tests and p-values

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/notebooks/T_test_R.ipynb)

**[notebooks/T_test_R.ipynb](notebooks/T_test_R.ipynb)** — simulate two groups of measurements, look
at them, and then run a t-test. The point is to connect what a p-value says with what the data looks
like: you set the means, the spread and the number of points yourself, so you can watch which of
those the test responds to. The second half runs 100 tests at once and shows why that changes
everything — Bonferroni and Benjamini–Hochberg corrections, with the true answer known so you can
count your own mistakes.

### 2 · ANOVA and linear regression

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/notebooks/ANOVA_R.ipynb)

**[notebooks/ANOVA_R.ipynb](notebooks/ANOVA_R.ipynb)** — three groups instead of two. Why running
three t-tests is not the same as running one ANOVA, how to read an ANOVA table, and what Tukey's
post-hoc test adds once the ANOVA says *something* differs. The second half is linear regression:
the same `y ~ x` model notation, fitted with `lm()`, and what the slope, the intercept and R²
each tell you.

### 3 · Non-normality and transformations

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/notebooks/Nonnormal_R.ipynb)

**[notebooks/Nonnormal_R.ipynb](notebooks/Nonnormal_R.ipynb)** — skewed data, and the two honest
ways to deal with it. A t-test on lognormal data returns a perfectly ordinary-looking p-value and
nothing warns you, which is the danger. Log-transform and check with a Q-Q plot, or switch to a
rank-based test that makes no assumption about shape.

---

## Group assignment — power and sample size

The Week 4 group assignment (the brief, the cases and the allocation are on DTU Learn) asks you to
design an experiment before any data exists. These two notebooks do the calculations it needs.

**They are the same notebook in two languages** — same seven sections, same numbers, same worked
examples. Pick whichever you prefer; you do not need both.

| | |
|---|---|
| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/power/27200_W4_power_python.ipynb) | **[power/27200_W4_power_python.ipynb](power/27200_W4_power_python.ipynb)** — Python, using `statsmodels` |
| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week04_experimental_design_and_statistical_inference/power/27200_W4_power_R.ipynb) | **[power/27200_W4_power_R.ipynb](power/27200_W4_power_R.ipynb)** — R, using base R and `pwr` |

Sections, in both:

| | Use it for |
|---|---|
| 1 | Two groups, one measurement each — sample size, detectable difference, dropout, power curves |
| 2 | Repeated measurements of the same unit — deciding what n actually is |
| 3 | Two proportions, including very unequal group sizes |
| 4 | Thousands of tests at once — Bonferroni, and an FDR simulation |
| 5 | Paired designs, and how much pairing saves you |
| 6 | More than two groups, checking normality, and the cost of going non-parametric |
| 7 | **Simulation** — how to get power for any design, when no formula exists |

Section 7 is the one worth reading even if your case is covered by a formula. Power just means "how
often would this experiment work?", so you can always simulate the experiment a thousand times and
count. That works for designs no formula covers.

---

## Reading

Vaux, D. *Know when your numbers are significant.* Nature **492**, 180–181 (2012).

The *Points of Significance* columns in Nature Methods are short, readable and directly about these
questions — particularly those on power, replication and the error bars people misuse.
