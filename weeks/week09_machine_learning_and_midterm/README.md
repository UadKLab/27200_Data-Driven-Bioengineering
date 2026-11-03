# Week 9 — Machine Learning & Mid-term Assessment

**Date:** 05 November 2026  
**Instructors:** Mikael & Valdemaras  
**Theme:** Checkpoint after omics block; transition from biological data modalities to modeling.

# Week 9 – Exploring and classifying omics data

Exercise notebooks for **27200 Data-driven Bioengineering**. They cover two standard tasks on high-dimensional biological data: dimensionality reduction and supervised classification.

## Notebooks

### `week09_dimensionality_reduction.ipynb` – Tumour types from bulk RNA-seq (TCGA)

Dataset: 801 tumours from five cancer types (BRCA, KIRC, COAD, LUAD, PRAD), each measured on 20,531 genes. The data is the TCGA extract hosted by the UCI Machine Learning Repository, and the notebook downloads it automatically.

You will:
- inspect the data: its size, the fraction of zeros and the class balance
- look at the distributions of gene expression values and what they say about NGS data
- run PCA on the raw data and see why highly expressed genes dominate the loadings
- check whether between-sample normalization is needed
- preprocess the data (filter genes, select highly variable genes, scale) and interpret the PCA loadings and explained variance
- visualize the tumour types non-linearly with UMAP and explore its parameters

### `week09_cell_type_classification.ipynb` – Cell types from single-cell RNA-seq (PBMC)

Dataset: 2,638 peripheral blood mononuclear cells (10x Genomics, loaded through Scanpy), each assigned to one of eight immune cell types.

You will:
- inspect the cell type composition and see how unbalanced it is
- compare the cells in PCA and UMAP space
- train a logistic regression with and without class balancing, and evaluate it on held-out cells
- compare logistic regression, SVM and random forest, using feature selection inside the pipeline to avoid leaking information from the test set
- inspect what the models have learned, using logistic regression coefficients an

