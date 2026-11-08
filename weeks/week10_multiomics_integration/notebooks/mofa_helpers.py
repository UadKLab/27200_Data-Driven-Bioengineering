# =============================================================================
#  27200 Data-driven Bioengineering · Multi-omics integration with MOFA
#  Helper functions shared by Exercise A and Exercise B
# -----------------------------------------------------------------------------
#  Python port of Carsten's 27200_mofa_functions.R. MOFA2 in R trains its
#  models with the Python package mofapy2; here we call mofapy2 directly.
#
#  You do not need to edit this file, but READ build_views(): every parameter
#  you set in the notebook is applied there, and every preprocessing choice is
#  a modelling assumption.
#
#  Data: MetaCardis extract (n = 960; France, Germany, Denmark)
#    Vieira-Silva et al. 2020 Nature        doi:10.1038/s41586-020-2269-x
#    Forslund et al. 2021 Nature            doi:10.1038/s41586-021-04177-9
#    Fromentin et al. 2022 Nature Medicine  doi:10.1038/s41591-022-01688-4
# =============================================================================

import contextlib, copy, hashlib, io, os, pickle, re

import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Ellipse
from scipy import stats

# ---- 0. Default parameters ---------------------------------------------------
# Every option used below has a default here. The notebooks override these with
# their own `settings` dict (merged with merge_settings), so a notebook only has
# to list the options it changes. Stress-test switches (Exercise B) are OFF by default.
DEFAULT_SETTINGS = dict(
    views=["clinical", "microbiome", "drugs", "metabolome"],
    # clinical view
    clinical_vars=["BMI", "Waist.circum", "triglycerides", "adiponectin",
                   "hsCRP", "HbA1c", "SystoBP", "DiastBP"],
    clinical_log=["triglycerides", "adiponectin", "hsCRP", "HbA1c"],
    clinical_scale=True,
    # microbiome view
    mb_min_prevalence=0.10,
    mb_transform="clr",
    mb_pseudocount=1e-6,
    # drug view
    drug_min_prevalence=0.02,
    drug_drop_unions=True,
    drug_likelihood="bernoulli",
    # metabolome view
    met_n_features=300,
    met_drop_xenobiotics=True,
    met_scale=True,
    # MOFA model and training
    num_factors=10,
    scale_views=True,
    group_by=None,
    convergence_mode="fast",
    maxiter=1000,
    seed=501,               # Teacher's birthday!
    # stress tests (Exercise B)
    scramble_view=None,     # name of the view whose sample labels get shuffled
    scramble_fraction=0,    # fraction of samples shuffled in that view
    batch_effect=0,         # size of a simulated plate effect on the metabolome (SD units)
    batch_phenotype="CAD",  # phenotype that is over-represented on plate 2
    batch_confounding=0.5,  # P(plate 2 | batch_phenotype); 0.5 = plate unrelated to phenotype
    batch_correct=False,    # remove plate means from each metabolite before MOFA
)


def merge_settings(*dicts):
    """Defaults, then each dict in turn (like R's modifyList)."""
    out = copy.deepcopy(DEFAULT_SETTINGS)
    for d in dicts:
        out.update(copy.deepcopy(d or {}))
    return out


# Serum features that are the medication itself or its metabolites
# (metformin, atorvastatin, metoprolol, salicylate from aspirin, PPIs, ...).
# Lifestyle xenobiotics (caffeine, cotinine, sweeteners) are deliberately kept.
DRUG_REGEX = "|".join(["metformin", "statin", "olol", "pril", "sartan", "salicyl",
                       "prazole", "warfarin", "furosemide", "thiazide", "gliptin",
                       "ezetim", "acetaminophen", "acetamidophen", "ibuprofen"])

# Drug classes that combine sub-classes listed in the same table
# (e.g. Antidiabetics = Metformin OR Insulin OR DPP-IV inhibitors OR GLP-1 agonists;
# this matches for 99 % of participants, the rest take antidiabetics not listed separately).
DRUG_UNIONS = ["Antidiabetics", "Lipid.lowering.drugs", "Anti.hypertensive.drugs"]

VIEW_ORDER = ["clinical", "microbiome", "drugs", "metabolome"]


# ---- 1. Load data ------------------------------------------------------------
# The data are not in the public repository. Download 27200_mofa_data.zip from DTU Learn
# (Week 10); the notebook asks you to upload it (Colab) or finds it next to the notebook.
DATA_ZIP = "27200_mofa_data.zip"
TABLES = ["cohort_metadata", "drugs", "gut_microbiota", "serum_metabolomics", "taxonomy"]
FILES = [f"27200_multi_omics_{t}.txt" for t in TABLES]


def _extract(zip_path, data_dir):
    """Copy the five data files out of a zip (by file name only; other entries are ignored)."""
    import zipfile
    with zipfile.ZipFile(zip_path) as z:
        for member in z.namelist():
            name = os.path.basename(member)
            if name in FILES and "__MACOSX" not in member:
                with z.open(member) as src, open(os.path.join(data_dir, name), "wb") as dst:
                    dst.write(src.read())


def get_data(data_dir="data"):
    import glob, shutil
    os.makedirs(data_dir, exist_ok=True)
    missing = lambda: [f for f in FILES if not os.path.exists(os.path.join(data_dir, f))]
    for f in missing():                                   # loose files next to the notebook
        if os.path.exists(f):
            shutil.copy(f, data_dir)
    for z in glob.glob("*.zip") + glob.glob(os.path.join(data_dir, "*.zip")):
        if missing():
            _extract(z, data_dir)
    if missing():
        try:
            from google.colab import files
        except ImportError:
            raise FileNotFoundError(f"Put {DATA_ZIP} (from DTU Learn, Week 10) in the folder of this notebook, "
                                    f"or the five data files in '{data_dir}/'. Missing: {missing()}")
        print(f"Upload {DATA_ZIP} from DTU Learn (Week 10), or the five .txt files:")
        for name in files.upload():
            if name.endswith(".zip"):
                _extract(name, data_dir)
            elif name in FILES:
                shutil.move(name, os.path.join(data_dir, name))
    if missing():
        raise FileNotFoundError(f"Still missing: {missing()}. Run the cell again and upload {DATA_ZIP}.")


def load_metacardis(data_dir="data"):
    """Returns one dict holding all five tables (rows = samples, except taxonomy)."""
    get_data(data_dir)
    read = lambda t: pd.read_csv(os.path.join(data_dir, f"27200_multi_omics_{t}.txt"), sep="\t", index_col=0)
    md = read("cohort_metadata")
    # 'group' is renamed 'phenotype': MOFA reserves the word 'group' for its own
    # multi-group option. 'metabolic_syndrome' is shortened to 'MetS' for readable plots.
    md["Nationality"] = md["Nationality"].replace("Danemark", "Denmark")
    md["group"] = md["group"].replace("metabolic_syndrome", "MetS")
    md = md.rename(columns={"group": "phenotype"})
    return dict(metadata=md, drugs=read("drugs"), microbiome=read("gut_microbiota"),
                serum=read("serum_metabolomics"), taxonomy=read("taxonomy"))


# ---- 2. Build the MOFA input views ------------------------------------------
def _zscore(df):
    return (df - df.mean()) / df.std()


def xenobiotic_features(serum):
    """Serum features removed when met_drop_xenobiotics = True."""
    return [c for c in serum.columns if re.search(DRUG_REGEX, c, flags=re.I)]


class Views(dict):
    """dict of DataFrames (rows = samples, columns = features), one per view.
    Sample covariates (metadata + drug use + simulated plate) travel along as .covariates."""
    covariates = None


def build_views(mc, settings=None):
    s = merge_settings(settings)
    rng = np.random.default_rng(s["seed"])   # simulated plate and scrambling are reproducible
    md = mc["metadata"]
    n = len(md)

    # Simulated technical batch ("plate"). It only touches the data if batch_effect > 0.
    p2 = np.where(md["phenotype"] == s["batch_phenotype"], s["batch_confounding"], 1 - s["batch_confounding"])
    plate = rng.binomial(1, p2)

    views = {}

    # Clinical markers: different units (mmHg, mmol/L, %, kg/m2), several right-skewed
    cl = md[s["clinical_vars"]].astype(float).copy()
    for c in [c for c in s["clinical_log"] if c in cl]:
        cl[c] = np.log(cl[c])                    # all strictly positive here
    # z-score: otherwise blood pressure (SD ~ 17 mmHg) outweighs triglycerides (SD ~ 0.8 mmol/L)
    views["clinical"] = _zscore(cl) if s["clinical_scale"] else cl

    # Gut microbiome: relative abundances (rows sum to 1), ~88 % zeros
    mb = mc["microbiome"]
    # prevalence filter: keep taxa detected in >= mb_min_prevalence of samples
    mb = mb.loc[:, (mb > 0).mean() >= s["mb_min_prevalence"]]
    # transformation. CLR = log(x) minus the sample's mean log abundance; the
    # reference (geometric mean) is taken over the taxa kept by the filter above.
    if s["mb_transform"] == "clr":
        lx = np.log(mb + s["mb_pseudocount"])
        mb = lx.sub(lx.mean(axis=1), axis=0)
    elif s["mb_transform"] == "log10":
        mb = np.log10(mb + s["mb_pseudocount"])
    elif s["mb_transform"] != "none":
        raise ValueError("mb_transform must be 'clr', 'log10' or 'none'")
    # readable feature names: bac_1 -> Bacteroides_uniformis
    names = mc["taxonomy"].loc[mb.columns, "Species"].str.replace(r"^s__", "", regex=True)
    seen = {}
    unique = []
    for nm in names:                              # like R's make.unique: x, x.1, x.2
        unique.append(nm if nm not in seen else f"{nm}.{seen[nm]}")
        seen[nm] = seen.get(nm, 0) + 1
    views["microbiome"] = mb.set_axis(unique, axis=1)

    # Medication: Yes/No -> 1/0 (MOFA's Bernoulli likelihood needs 0/1)
    dr = (mc["drugs"] == "Yes").astype(float)
    keep = (dr.mean() >= s["drug_min_prevalence"]) & ~(s["drug_drop_unions"] & dr.columns.isin(DRUG_UNIONS))
    views["drugs"] = dr.loc[:, keep]

    # Serum metabolome: already log-transformed; 17 samples have no serum data at all
    met = mc["serum"]
    # optionally remove the measured drugs/drug metabolites from the serum panel
    if s["met_drop_xenobiotics"]:
        met = met.drop(columns=xenobiotic_features(met))
    # keep the met_n_features most variable metabolites (variance on the log scale)
    met = met[met.var().sort_values(ascending=False, kind="stable").index[:s["met_n_features"]]]
    # optionally z-score each metabolite
    if s["met_scale"]:
        met = _zscore(met)
    # STRESS TEST: plate 2 samples get a metabolite-specific shift
    met = met + s["batch_effect"] * np.outer(plate, rng.standard_normal(met.shape[1]))
    # STRESS TEST remedy: subtract plate means per metabolite (= regress out plate)
    if s["batch_correct"]:
        met = met - met.groupby(plate).transform("mean")
    views["metabolome"] = met

    views = Views({v: views[v] for v in s["views"]})

    # STRESS TEST: break sample linkage by shuffling rows of one view for a fraction
    # of samples. Row names stay in place, so MOFA still believes rows are matched.
    if s["scramble_view"] and s["scramble_fraction"] > 0:
        v = views[s["scramble_view"]]
        idx = rng.choice(n, round(s["scramble_fraction"] * n), replace=False)
        vals = v.to_numpy().copy()
        vals[idx] = vals[rng.permutation(idx)]
        views[s["scramble_view"]] = pd.DataFrame(vals, index=v.index, columns=v.columns)

    # covariates = metadata + drug use (+ the simulated plate, only if it was used)
    cov = pd.concat([md, mc["drugs"]], axis=1)
    if s["batch_effect"] > 0:
        cov["plate"] = [f"plate{p + 1}" for p in plate]
    views.covariates = cov
    return views


# ---- 3. Train MOFA (with caching) -------------------------------------------
class MofaModel:
    """The parts of a trained MOFA model the notebooks use.
    Z: samples x factors; W: dict view -> features x factors;
    r2: long table (group, view, factor, value in %); metadata: sample covariates."""

    def __init__(self, path, views, settings, messages=""):
        self.path, self.views, self.settings, self.messages = path, views, settings, messages
        dec = lambda a: [x.decode() if isinstance(x, bytes) else str(x) for x in a]
        with h5py.File(path, "r") as f:
            self.groups = dec(f["groups/groups"][()])
            view_names = dec(f["views/views"][()])
            samples = {g: dec(f[f"samples/{g}"][()]) for g in self.groups}
            Z = pd.concat([pd.DataFrame(f[f"expectations/Z/{g}"][()].T, index=samples[g]) for g in self.groups])
            W = {m: pd.DataFrame(f[f"expectations/W/{m}"][()].T, index=dec(f[f"features/{m}"][()]))
                 for m in view_names}
            r2 = {g: np.atleast_2d(f[f"variance_explained/r2_per_factor/{g}"][()]) for g in self.groups}
        k = Z.shape[1]
        # Like MOFA2's load_model(): remove factors that explain no variance at all
        total = sum(r2[g].sum(axis=0) for g in self.groups)
        active = np.where(total >= 1e-4)[0] if (total >= 1e-4).any() else np.arange(k)
        fn = [f"Factor{i + 1}" for i in range(len(active))]
        self.Z = Z.iloc[:, active].set_axis(fn, axis=1)
        self.W = {m: w.iloc[:, active].set_axis(fn, axis=1) for m, w in W.items()}
        rows = []
        for g in self.groups:
            for vi, m in enumerate(view_names):
                for j, a in enumerate(active):
                    rows.append((g, m, fn[j], r2[g][vi, a]))   # mofapy2 stores R² in %
        self.r2 = pd.DataFrame(rows, columns=["group", "view", "factor", "value"])
        self.view_names = view_names
        md = views.covariates.loc[self.Z.index].copy()
        md.insert(0, "group", pd.concat([pd.Series(g, index=samples[g]) for g in self.groups]))
        self.metadata = md

    @property
    def factors(self):
        return list(self.Z.columns)


def _quality_checks(model):
    """Warnings like the ones MOFA2 prints in R after training."""
    out = []
    c = model.Z.corr().to_numpy().copy()
    np.fill_diagonal(c, 0)
    if np.nanmax(np.abs(c)) > 0.5:
        out.append("The model contains highly correlated factors (see plot_factor_cor(model)). "
                   "Consider fewer factors or longer training.")
    for m, X in model.views.items():
        n_expr = (X > 0).sum(axis=1).loc[model.Z.index]
        r = model.Z.apply(lambda z: np.corrcoef(z, n_expr)[0, 1])
        hit = [f for f, v in r.items() if abs(v) > 0.75]
        if hit:
            out.append(f"{', '.join(hit)} strongly correlated (|r| > 0.75) with the number of values above "
                       f"zero per sample in view '{m}', i.e. with a global level of that view.")
    return out


def fit_mofa(views, settings=None, cache_dir="models", show_warnings=True):
    """Identical input data + settings -> identical model file in cache_dir, so
    re-running a cell re-uses a model that is already trained."""
    from mofapy2.run.entry_point import entry_point
    s = merge_settings(settings)
    os.makedirs(cache_dir, exist_ok=True)
    key = hashlib.md5(pickle.dumps(({k: v.to_numpy().tobytes() for k, v in views.items()},
                                    {k: list(v.columns) for k, v in views.items()},
                                    sorted(s.items(), key=str)))).hexdigest()[:12]
    outfile = os.path.join(cache_dir, f"mofa_{key}.hdf5")
    logfile = outfile.replace(".hdf5", ".log")
    if os.path.exists(outfile):
        print("Loading cached model:", outfile)
        log = open(logfile).read() if os.path.exists(logfile) else ""
    else:
        cov = views.covariates
        samples = list(next(iter(views.values())).index)
        if s["group_by"]:
            labels = cov.loc[samples, s["group_by"]].astype(str)
            groups = sorted(labels.unique())
            gsamples = [list(labels.index[labels == g]) for g in groups]
        else:
            groups, gsamples = ["group1"], [samples]
        names = list(views)
        data = [[views[m].loc[gs].to_numpy(dtype=float) for gs in gsamples] for m in names]
        lik = [s["drug_likelihood"] if m == "drugs" else "gaussian" for m in names]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ent = entry_point()
            ent.set_data_options(scale_views=s["scale_views"])
            ent.set_data_matrix(data, likelihoods=lik, views_names=names, groups_names=groups,
                                samples_names=gsamples, features_names=[list(views[m].columns) for m in names])
            ent.set_model_options(factors=s["num_factors"], ard_factors=len(groups) > 1)
            ent.set_train_options(iter=s["maxiter"], convergence_mode=s["convergence_mode"], seed=s["seed"],
                                  startELBO=1, freqELBO=5, verbose=False)
            ent.build()
            ent.run()
            ent.save(outfile, save_data=False)
        log = buf.getvalue()
        with open(logfile, "w") as fh:
            fh.write(log)
    model = MofaModel(outfile, views, s, log)
    if show_warnings:
        warn = [ln.strip() for ln in log.splitlines() if "warning" in ln.lower()] + _quality_checks(model)
        for w in dict.fromkeys(warn):
            print("WARNING:", w)
    return model


# ---- 4. Downstream helpers ---------------------------------------------------
def get_Z(model):
    return model.Z


def _bh(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    q = p[o] * len(p) / np.arange(1, len(p) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty_like(q)
    out[o] = np.minimum(q, 1)
    return out


def _lm_r2(z, x):
    """R² and F-test p of a linear model z ~ x (categorical x as dummies, like R's lm)."""
    d = pd.DataFrame({"z": z, "x": x}).dropna()
    if pd.api.types.is_numeric_dtype(d["x"]) and not pd.api.types.is_bool_dtype(d["x"]):
        X = np.column_stack([np.ones(len(d)), d["x"].astype(float)])
    else:
        X = np.column_stack([np.ones(len(d)), pd.get_dummies(d["x"].astype(str), drop_first=True).to_numpy(float)])
    if X.shape[1] < 2 or len(d) <= X.shape[1]:
        return np.nan, np.nan
    beta, *_ = np.linalg.lstsq(X, d["z"].to_numpy(), rcond=None)
    rss = ((d["z"] - X @ beta) ** 2).sum()
    tss = ((d["z"] - d["z"].mean()) ** 2).sum()
    r2 = 1 - rss / tss
    df1, df2 = X.shape[1] - 1, len(d) - X.shape[1]
    F = (r2 / df1) / ((1 - r2) / df2) if r2 < 1 else np.inf
    return r2, stats.f.sf(F, df1, df2)


def covariate_r2(Z, md, covariates):
    """How much of each factor's variance is explained by each covariate?
    One linear model per factor x covariate, so R² is comparable across continuous and
    categorical covariates. Works for any samples x components matrix (MOFA factors, PCs, ...)."""
    Z = pd.DataFrame(Z)
    md = md.loc[Z.index]
    rows = [(f, v, *_lm_r2(Z[f], md[v])) for v in covariates for f in Z.columns]
    res = pd.DataFrame(rows, columns=["factor", "covariate", "r2", "p"])
    res["p_adj"] = _bh(res["p"].fillna(1))
    return res


def factor_covariates(model, covariates):
    return covariate_r2(model.Z, model.metadata, covariates)


def factor_covariates_within(model, covariates, subset_var, subset_level):
    """Same, but only within one subset of samples, e.g. Metformin within T2D patients:
    factor_covariates_within(model, ["Metformin"], "phenotype", "T2D")"""
    covariates = [covariates] if isinstance(covariates, str) else covariates
    keep = model.metadata[subset_var].isin([subset_level] if isinstance(subset_level, str) else subset_level)
    return covariate_r2(model.Z[keep.to_numpy()], model.metadata[keep], covariates)


def _heatmap(ax, M, row_labels, col_labels, cmap, vmax, labels, title=None, cbar_label=None):
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(col_labels)), col_labels, rotation=45, ha="right")
    ax.set_yticks(range(len(row_labels)), row_labels)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if labels[i][j]:
                ax.text(j, i, labels[i][j], ha="center", va="center", fontsize=8,
                        color="white" if vmax and M[i, j] > 0.6 * vmax else "black")
    ax.set_xticks(np.arange(-.5, M.shape[1]), minor=True)
    ax.set_yticks(np.arange(-.5, M.shape[0]), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    ax.tick_params(which="minor", length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    if title:
        ax.set_title(title, loc="left", fontsize=11)
    plt.colorbar(im, ax=ax, shrink=0.8, label=cbar_label)


def _factor_sort(fs):
    return sorted(fs, key=lambda f: int(re.sub(r"\D", "", str(f)) or 0))


def plot_covariate_r2(res, title=None, ax=None):
    fs = _factor_sort(res["factor"].unique())
    cs = list(dict.fromkeys(res["covariate"]))
    M = res.pivot(index="factor", columns="covariate", values="r2").loc[fs, cs]
    P = res.pivot(index="factor", columns="covariate", values="p_adj").loc[fs, cs]
    lab = [[f"{M.iloc[i, j]:.2f}" if P.iloc[i, j] < 0.05 else "" for j in range(len(cs))] for i in range(len(fs))]
    if ax is None:
        _, ax = plt.subplots(figsize=(1.0 + 0.75 * len(cs), 0.9 + 0.35 * len(fs)))
    _heatmap(ax, M.to_numpy(float), fs, cs, "Reds", max(np.nanmax(M.to_numpy(float)), 1e-9), lab, title, "R²")
    ax.set_xlabel("R² of factor ~ covariate; values printed where BH-adjusted p < 0.05", fontsize=8)
    return ax


def plot_variance_explained(model, total=False, group=None):
    """total=True: R² per view over all factors. Otherwise R² per factor and view (%)."""
    r2 = model.r2 if group is None else model.r2[model.r2.group == group]
    groups = list(dict.fromkeys(r2.group))
    if total:
        tot = r2.groupby(["group", "view"], sort=False)["value"].sum().reset_index()
        fig, axes = plt.subplots(1, len(groups), figsize=(4.5 * len(groups), 3), squeeze=False)
        for ax, g in zip(axes[0], groups):
            d = tot[tot.group == g]
            ax.bar(d["view"], d["value"], color="#2e6f95")
            ax.set(ylabel="variance explained (%)", title=g if len(groups) > 1 else "Total variance explained per view")
            ax.tick_params(axis="x", rotation=30)
        plt.tight_layout(); plt.show(); return
    fig, axes = plt.subplots(1, len(groups), figsize=(4.8 * len(groups), 4.6), squeeze=False)
    for ax, g in zip(axes[0], groups):
        d = r2[r2.group == g]
        fs = _factor_sort(d["factor"].unique()); vs = list(dict.fromkeys(d["view"]))
        M = d.pivot(index="factor", columns="view", values="value").loc[fs, vs].clip(lower=0)
        lab = [[f"{v:.1f}" if v >= 0.1 else "" for v in row] for row in M.to_numpy()]
        _heatmap(ax, M.to_numpy(), fs, vs, "Greens", max(M.to_numpy().max(), 1e-9), lab,
                 g if len(groups) > 1 else "Variance explained (%) per factor and view", "R² (%)")
    plt.tight_layout(); plt.show()


def plot_data_overview(views):
    """Which samples have which views? (grey = missing)"""
    names = list(views)
    samples = next(iter(views.values())).index
    P = np.array([~views[m].loc[samples].isna().all(axis=1).to_numpy() for m in names])
    order = np.lexsort(P[::-1])
    fig, ax = plt.subplots(figsize=(9, 0.5 + 0.45 * len(names)))
    ax.imshow(P[:, order], aspect="auto", cmap=plt.matplotlib.colors.ListedColormap(["#cccccc", "#2e6f95"]),
              interpolation="nearest")
    ax.set_yticks(range(len(names)), [f"{m}  (D = {views[m].shape[1]}, N = {P[i].sum()})" for i, m in enumerate(names)])
    ax.set_xticks([]); ax.set_xlabel(f"{len(samples)} samples (blue = data, grey = missing)")
    for sp in ax.spines.values():
        sp.set_visible(False)
    plt.tight_layout(); plt.show()


def plot_factor_cor(model):
    C = model.Z.corr().to_numpy()
    fs = model.factors
    fig, ax = plt.subplots(figsize=(0.6 * len(fs) + 1.5, 0.55 * len(fs) + 1))
    im = ax.imshow(C, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(fs)), fs, rotation=45, ha="right"); ax.set_yticks(range(len(fs)), fs)
    for i in range(len(fs)):
        for j in range(len(fs)):
            ax.text(j, i, f"{C[i, j]:.2f}", ha="center", va="center", fontsize=7)
    plt.colorbar(im, ax=ax, shrink=0.8, label="Pearson r")
    ax.set_title("Correlation between factors", loc="left", fontsize=11)
    plt.tight_layout(); plt.show()


def _cats(x):
    return [c for c in pd.unique(x.dropna()) if c is not None] if x.dtype == object else sorted(x.dropna().unique())


def plot_factor(model, factors=(1,), color_by="phenotype", group_by=None, dot_size=6, add_violin=True):
    """Factor values per sample. x axis: categories of group_by (default: color_by);
    dots coloured by color_by, side by side (dodged) when group_by differs from color_by."""
    group_by = group_by or color_by
    md = model.metadata
    fs = [f"Factor{f}" if isinstance(f, (int, np.integer)) else f for f in factors]
    xs, cs = _cats(md[group_by]), _cats(md[color_by])
    pal = dict(zip(cs, plt.cm.tab10.colors))
    fig, axes = plt.subplots(1, len(fs), figsize=(max(4.5, 0.9 * len(xs) * (len(cs) if group_by != color_by else 1)) * len(fs) / 1.4, 3.8),
                             squeeze=False)
    rng = np.random.default_rng(0)
    for ax, f in zip(axes[0], fs):
        for i, xv in enumerate(xs):
            sub = md[md[group_by] == xv]
            levels = [xv] if group_by == color_by else cs
            for j, cv in enumerate(levels):
                pts = sub if group_by == color_by else sub[sub[color_by] == cv]
                z = model.Z.loc[pts.index, f].dropna()
                if len(z) == 0:
                    continue
                w = 0.8 / len(levels)
                x0 = i - 0.4 + w * (j + 0.5)
                col = pal.get(cv if group_by != color_by else xv, "grey")
                if add_violin and len(z) > 2:
                    v = ax.violinplot(z, positions=[x0], widths=w * 0.95, showextrema=False)
                    for b in v["bodies"]:
                        b.set_facecolor(col); b.set_alpha(0.25); b.set_edgecolor("none")
                ax.scatter(x0 + rng.uniform(-w * 0.3, w * 0.3, len(z)), z, s=dot_size, color=col, alpha=0.7, linewidths=0)
        ax.axhline(0, color="#999999", lw=0.8, zorder=0)
        ax.set_xticks(range(len(xs)), xs, rotation=30, ha="right")
        ax.set(title=f, ylabel="factor value")
    if group_by != color_by:
        handles = [plt.Line2D([], [], marker="o", ls="", color=pal[c], label=str(c)) for c in cs]
        axes[0][-1].legend(handles=handles, title=color_by, frameon=False, bbox_to_anchor=(1, 1), loc="upper left")
    plt.tight_layout(); plt.show()


def plot_factors(model, factors=(1, 2), color_by="phenotype", dot_size=8):
    md = model.metadata
    fx, fy = [f"Factor{f}" if isinstance(f, (int, np.integer)) else f for f in factors]
    fig, ax = plt.subplots(figsize=(6, 4.8))
    for c, col in zip(_cats(md[color_by]), plt.cm.tab10.colors):
        idx = md.index[md[color_by] == c]
        ax.scatter(model.Z.loc[idx, fx], model.Z.loc[idx, fy], s=dot_size, color=col, alpha=0.7, label=str(c), linewidths=0)
    ax.set(xlabel=fx, ylabel=fy)
    ax.legend(title=color_by, frameon=False, bbox_to_anchor=(1, 1), loc="upper left")
    plt.tight_layout(); plt.show()


def scaled_weights(model, view, factor):
    """Weights of one view and factor, scaled to -1..1 (divided by the largest |weight|)."""
    f = f"Factor{factor}" if isinstance(factor, (int, np.integer)) else factor
    w = model.W[view][f]
    return w / w.abs().max()


def plot_top_weights(model, view, factor=1, nfeatures=10, ax=None):
    w = scaled_weights(model, view, factor)
    top = w.reindex(w.abs().sort_values(ascending=False).index[:nfeatures])[::-1]
    show = ax is None
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 0.3 * nfeatures + 1))
    ax.barh(range(len(top)), top.to_numpy(), color=np.where(top.to_numpy() > 0, "#c0392b", "#2e6f95"))
    ax.set_yticks(range(len(top)), top.index)
    ax.axvline(0, color="#666666", lw=0.8)
    ax.set(xlim=(-1.05, 1.05), xlabel="scaled weight (-1..1)", title=f"{view}: top weights, Factor{factor}" if isinstance(factor, (int, np.integer)) else f"{view}: {factor}")
    if show:
        plt.tight_layout(); plt.show()
    return ax


def plot_data_scatter(model, view, factor=1, features=4, color_by="phenotype", add_lm=True):
    """Do the data support the weights? Feature values (as entered into MOFA) against factor values."""
    f = f"Factor{factor}" if isinstance(factor, (int, np.integer)) else factor
    if isinstance(features, (int, np.integer)):
        w = model.W[view][f]
        features = list(w.abs().sort_values(ascending=False).index[:features])
    X = model.views[view].loc[model.Z.index]
    missing = [ft for ft in features if ft not in X.columns]
    if missing:
        raise KeyError(f"Not in view '{view}': {missing}. Copy feature names exactly, e.g. from the brief.")
    md = model.metadata
    ncol = min(len(features), 2)
    nrow = int(np.ceil(len(features) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(5.2 * ncol, 3.6 * nrow), squeeze=False)
    cats = _cats(md[color_by])
    for ax, ft in zip(axes.flat, features):
        for c, col in zip(cats, plt.cm.tab10.colors):
            idx = md.index[md[color_by] == c]
            ax.scatter(model.Z.loc[idx, f], X.loc[idx, ft], s=6, alpha=0.6, color=col, label=str(c), linewidths=0)
        d = pd.DataFrame({"z": model.Z[f], "x": X[ft]}).dropna()
        if add_lm and len(d) > 2:
            r, p = stats.pearsonr(d["z"], d["x"])
            b = np.polyfit(d["z"], d["x"], 1)
            xx = np.linspace(d["z"].min(), d["z"].max(), 50)
            ax.plot(xx, np.polyval(b, xx), color="black", lw=1.2)
            ax.set_title(f"{ft}\nr = {r:.2f}, p = {p:.1e}", fontsize=10)
        else:
            ax.set_title(ft, fontsize=10)
        ax.set(xlabel=f, ylabel="value entered into MOFA")
    for ax in axes.flat[len(features):]:
        ax.axis("off")
    axes.flat[0].legend(title=color_by, frameon=False, fontsize=8, markerscale=2)
    plt.tight_layout(); plt.show()


def plot_r2_compare(models):
    """Variance explained per factor and view, side by side for a dict of models.
    Multi-group models get one panel per group. Negative R² (possible for non-Gaussian
    views, where R² is computed on pseudo-data) is shown as 0."""
    panels = []
    for nm, m in models.items():
        for g in m.groups:
            panels.append((nm if len(m.groups) == 1 else f"{nm} | {g}", m.r2[m.r2.group == g]))
    ncol = min(4, len(panels)); nrow = int(np.ceil(len(panels) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.6 * ncol, 4.2 * nrow), squeeze=False)
    vmax = max(p[1]["value"].max() for p in panels)
    for ax, (title, d) in zip(axes.flat, panels):
        fs = _factor_sort(d["factor"].unique()); vs = list(dict.fromkeys(d["view"]))
        M = d.pivot(index="factor", columns="view", values="value").loc[fs, vs].clip(lower=0)
        lab = [[f"{v:.1f}" if v >= 0.1 else "" for v in row] for row in M.to_numpy()]
        _heatmap(ax, M.to_numpy(), fs, vs, "Greens", vmax, lab, title, "R² (%)")
    for ax in axes.flat[len(panels):]:
        ax.axis("off")
    plt.tight_layout(); plt.show()


def plot_factor_match(ref, alt, labels=("baseline", "perturbed"), ax=None):
    """|Pearson r| between two sets of latent components on the shared samples.
    ref / alt may be MOFA models or samples x components tables (e.g. PCA scores)."""
    as_Z = lambda x: x.Z if isinstance(x, MofaModel) else pd.DataFrame(x)
    A, B = as_Z(ref), as_Z(alt)
    s = A.index.intersection(B.index)
    C = np.abs(np.array([[pd.Series(A.loc[s, a]).corr(pd.Series(B.loc[s, b])) for b in B.columns] for a in A.columns]))
    show = ax is None
    if ax is None:
        _, ax = plt.subplots(figsize=(0.55 * B.shape[1] + 2, 0.4 * A.shape[1] + 1.5))
    lab = [[f"{v:.2f}" for v in row] for row in C]
    _heatmap(ax, C, list(A.columns), [str(c) for c in B.columns], "Blues", 1, lab, None, "|r|")
    ax.set(xlabel=labels[1], ylabel=labels[0])
    if show:
        plt.tight_layout(); plt.show()
    return ax


def block_matrix(views):
    """Concatenated, block-scaled matrix for PCA / PLS-DA comparison:
    z-score every feature, set missing values to 0 (= the feature mean; PCA and PLS
    cannot handle NA), divide each view by sqrt(#features) so that every view
    contributes the same total variance."""
    blocks = []
    for nm, v in views.items():
        z = _zscore(v).replace([np.inf, -np.inf], np.nan).fillna(0) / np.sqrt(v.shape[1])
        blocks.append(z.set_axis([f"{nm}:{c}" for c in v.columns], axis=1))
    return pd.concat(blocks, axis=1)


# ---- 5. Supervised comparison: sparse PLS-DA --------------------------------
def splsda_fit(X, y, ncomp=2, keepX=50):
    """Sparse PLS-DA, approximated as: keep the keepX * ncomp features that best separate
    the labels (F-test), then PLS-DA with ncomp components. Returns (pipeline, scores)."""
    from sklearn.cross_decomposition import PLSRegression
    from sklearn.feature_selection import SelectKBest, f_classif
    sel = SelectKBest(f_classif, k=min(keepX * ncomp, X.shape[1])).fit(X, y)
    Xs = sel.transform(X)
    Y = pd.get_dummies(pd.Series(y)).to_numpy(float)
    pls = PLSRegression(n_components=ncomp, scale=True).fit(Xs, Y)
    return (sel, pls, sorted(pd.unique(y))), pd.DataFrame(pls.x_scores_, index=X.index,
                                                           columns=[f"comp{i + 1}" for i in range(ncomp)])


def plot_splsda(scores, y, title):
    fig, ax = plt.subplots(figsize=(5.8, 4.6))
    for c, col in zip(sorted(pd.unique(y)), plt.cm.tab10.colors):
        m = np.asarray(y) == c
        S = scores.to_numpy()[m, :2]
        ax.scatter(S[:, 0], S[:, 1], s=7, alpha=0.6, color=col, label=str(c), linewidths=0)
        cov = np.cov(S.T); vals, vecs = np.linalg.eigh(cov)
        ang = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
        w, h = 2 * np.sqrt(vals[::-1] * stats.chi2.ppf(0.95, 2))
        ax.add_patch(Ellipse(S.mean(0), w, h, angle=ang, fill=False, color=col, lw=1.5))
    ax.set(xlabel="component 1", ylabel="component 2", title=title)
    ax.legend(frameon=False, fontsize=8, bbox_to_anchor=(1, 1), loc="upper left")
    plt.tight_layout(); plt.show()


def splsda_cv_ber(X, y, ncomp=2, keepX=50, folds=5, nrepeat=3, seed=501):
    """Cross-validated balanced error rate. Feature selection is refitted inside every
    training fold, so the test samples never influence which features are used."""
    from sklearn.model_selection import StratifiedKFold
    y = np.asarray(y); errs = []
    for r in range(nrepeat):
        pred = np.empty(len(y), dtype=object)
        for tr, te in StratifiedKFold(folds, shuffle=True, random_state=seed + r).split(X, y):
            (sel, pls, classes), _ = splsda_fit(X.iloc[tr], y[tr], ncomp, keepX)
            pred[te] = np.array(classes)[pls.predict(sel.transform(X.iloc[te])).argmax(1)]
        errs.append(np.mean([np.mean(pred[y == c] != c) for c in np.unique(y)]))
    return float(np.mean(errs))


# ---- 6. Export a factor summary for an LLM -----------------------------------
def llm_brief(model, factor, settings, covariates, n_top=10, file=None):
    """Writes a plain-text/Markdown brief: data context, preprocessing settings,
    variance explained, top weights per view and covariate associations."""
    s = merge_settings(settings)
    f = f"Factor{factor}" if isinstance(factor, (int, np.integer)) else factor
    md = model.metadata
    txt = [f"# MOFA factor brief: {f}", "",
           "## Study and data",
           "MetaCardis cross-sectional extract: n = 960 adults from France, Germany and Denmark.",
           "Phenotype groups: CAD, T2D, metabolic syndrome (MetS), obesity, controls (mutually exclusive).",
           f"Views integrated: {', '.join(model.view_names)}.",
           "Feature names were made syntactically valid; metabolites named 'X.12345' are unannotated",
           "compounds (Metabolon 'X-12345'). Microbiome features are species-level taxa.", "",
           "## Preprocessing and model settings"]
    txt += [f"- {k} = {v!r}" for k, v in s.items()]
    txt += ["", "## Variance explained by this factor (% of each view)"]
    for _, r in model.r2[model.r2.factor == f].iterrows():
        txt.append(f"- {r.view}{'' if r.group == 'group1' else f' [{r.group}]'}: {r.value:.1f}%")
    txt += ["", "## Top features by scaled weight (range -1..1; sign = direction relative to the factor)"]
    for v in model.view_names:
        w = scaled_weights(model, v, f)
        txt.append(f"### {v}")
        txt += [f"- {k}: {x:+.2f}" for k, x in w.reindex(w.abs().sort_values(ascending=False).index[:n_top]).items()]
    txt += ["", "## Association of factor values with covariates (R² of linear model, BH-adjusted p)"]
    res = covariate_r2(model.Z[[f]], md, covariates).sort_values("r2", ascending=False)
    txt += [f"- {r.covariate}: R² = {r.r2:.3f}, p_adj = {r.p_adj:.1e}" for r in res.itertuples()]
    txt += ["", "## Mean factor value by phenotype group (factor values are centred; arbitrary units)"]
    g = model.Z[f].groupby(md["phenotype"])
    txt += [f"- {k}: {m:+.2f} (n = {n})" for (k, m), n in zip(g.mean().items(), g.size())]
    out = "\n".join(txt)
    if file:
        os.makedirs(os.path.dirname(file) or ".", exist_ok=True)
        with open(file, "w") as fh:
            fh.write(out + "\n")
    print(out)
    return out
