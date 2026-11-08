# Week 10 — Multiomics Integration

**Date:** 12 November 2026  
**Instructors:** Carsten & Kostas  
**Theme:** Integrating heterogeneous biological data to support systems-level interpretation.

Two exercises with MOFA (multi-omics factor analysis) on the MetaCardis cohort. Both run in Colab;
no installation and no GPU needed. Do them in order: Exercise B starts from the model you build in
Exercise A.

---

## Exercises

### A · A guided MOFA run

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week10_multiomics_integration/notebooks/01_mofa_exercise_A.ipynb)

**[notebooks/01_mofa_exercise_A.ipynb](notebooks/01_mofa_exercise_A.ipynb)** — explore the study
design (which phenotypes, countries and drugs go together), then decide how to preprocess each of
the four views (clinical markers, gut microbiome, medication, serum metabolome) and justify every
choice in a decision log. Train a baseline MOFA model and interpret it: variance explained per view,
sanity checks, which covariates the factors follow, and which features drive a factor.

### B · Break the model, compare models, critique the AI

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week10_multiomics_integration/notebooks/02_mofa_exercise_B.ipynb)

**[notebooks/02_mofa_exercise_B.ipynb](notebooks/02_mofa_exercise_B.ipynb)** — paste your settings
from Exercise A, then:
- stress-test the model with predefined scenarios (no log-ratio, no scaling, a batch effect confounded
  with phenotype, scrambled sample IDs, drugs measured twice, one group per country, ...)
- check whether medication confounds the "disease" factors
- compare MOFA with PCA and sparse PLS-DA, including PLS-DA on permuted labels
- ask an LLM to interpret a factor with a predefined prompt, and check its claims against the data
  and the literature
- write a one-minute paper on what you found

All preprocessing and plotting functions are in
[notebooks/mofa_helpers.py](notebooks/mofa_helpers.py). Read `build_views()`: every setting you
choose is applied there.

---

## Data

The data are not stored in this repository. Download **`27200_mofa_data.zip`** from DTU Learn (Week 10);
the setup cell of each notebook asks you to upload it. Each Colab notebook runs on its own machine, so
you upload it once in Exercise A and once in Exercise B.

| File in the zip | Contents |
|---|---|
| `27200_multi_omics_cohort_metadata.txt` | 960 participants: age, sex, country, phenotype and 8 clinical markers |
| `27200_multi_omics_drugs.txt` | use (Yes/No) of 24 drug classes |
| `27200_multi_omics_gut_microbiota.txt` | relative abundances of 705 gut microbial species (faecal metagenomics) |
| `27200_multi_omics_serum_metabolomics.txt` | 1,446 serum metabolites (log-transformed) |
| `27200_multi_omics_taxonomy.txt` | taxonomy of the 705 species |

The data are an extract from the MetaCardis cohort, published with
Vieira-Silva *et al.*, *Nature* 2020 ([doi:10.1038/s41586-020-2269-x](https://doi.org/10.1038/s41586-020-2269-x)),
Forslund *et al.*, *Nature* 2021 ([doi:10.1038/s41586-021-04177-9](https://doi.org/10.1038/s41586-021-04177-9)) and
Fromentin *et al.*, *Nature Medicine* 2022 ([doi:10.1038/s41591-022-01688-4](https://doi.org/10.1038/s41591-022-01688-4)).

## Acknowledgements

The exercises were designed by Carsten as R Markdown workbooks with MOFA2 and mixOmics. The notebooks
here are a Python version for Colab: MOFA models are trained with
[mofapy2](https://github.com/bioFAM/mofapy2), the same engine MOFA2 uses in R
(Argelaguet *et al.*, *Mol Syst Biol* 2018, [doi:10.15252/msb.20178124](https://doi.org/10.15252/msb.20178124)).
