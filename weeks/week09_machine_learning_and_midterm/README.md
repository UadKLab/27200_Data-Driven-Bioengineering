# Week 9 — Machine Learning & Mid-term Assessment

**Date:** 05 November 2026  
**Instructors:** Valdemaras  
**Theme:** Checkpoint after omics block; transition from biological data modalities to modeling.

Two exercises, both in Colab. No GPU needed. Do them in order: the second builds on the first.

---

## Exercises

### 1 · Tumour types from bulk RNA-seq (TCGA)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week09_machine_learning_and_midterm/notebooks/week09_dimensionality_reduction.ipynb)

**[notebooks/week09_dimensionality_reduction.ipynb](notebooks/week09_dimensionality_reduction.ipynb)** —
801 tumours from five cancer types (BRCA, KIRC, COAD, LUAD, PRAD), each measured on 20,531 genes.
Inspect the data (size, fraction of zeros, class balance) and the distributions of the expression
values. Run PCA on the raw data and see why highly expressed genes dominate the loadings. Check whether
between-sample normalization is needed. Then filter genes, select the highly variable ones and scale,
and interpret the PCA loadings and explained variance. Finally, show the tumour types with UMAP and
explore its parameters. The notebook downloads the data (about 70 MB) itself.

### 2 · Cell types from single-cell RNA-seq (PBMC)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week09_machine_learning_and_midterm/notebooks/week09_cell_type_classification.ipynb)

**[notebooks/week09_cell_type_classification.ipynb](notebooks/week09_cell_type_classification.ipynb)** —
2,638 blood immune cells (PBMCs), each assigned to one of eight cell types. See how unbalanced the
cell types are and compare the cells in PCA and UMAP space. Train a logistic regression with and
without class balancing and test it on held-out cells. Then compare LDA, SVM and random forest, with
gene selection inside the pipeline so that no information leaks from the test cells. Finally, look at
what the models have learned: logistic regression coefficients and random forest feature importances,
checked against the known marker genes.

---

## Data

| Dataset | Used in | Contents |
|---|---|---|
| TCGA pan-cancer RNA-seq | 1 | gene expression of 801 tumours from five cancer types, 20,531 genes |
| PBMC 3k (processed) | 2 | 2,638 cells, cleaned and scaled, with cell-type labels |

Both datasets are downloaded by the notebooks. The TCGA extract is hosted by the
[UCI Machine Learning Repository](https://doi.org/10.24432/C5R88H) (Fiorini, 2016, CC BY 4.0). The
PBMC data are from 10x Genomics and are loaded with Scanpy (`sc.datasets.pbmc3k_processed()`), as
prepared in its *Preprocessing and clustering 3k PBMCs* tutorial.
