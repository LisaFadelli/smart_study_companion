"""
Paired bootstrap significance test for comparing two RAG runs on the same set of QA items.

1. Loads two evaluation logs (JSON for IR metrics, CSV for RAGAS metrics).
2. For each QA item, computes the difference in a metric between run B and run A.
3. Uses a bootstrap procedure to estimate:
     - The average improvement (mean difference)
     - A 95% confidence interval (CI) for that improvement
     - An approximate p-value for the hypothesis "no real difference"
4. Prints a table showing which metrics are significantly better in one run.
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd

# Folder where your eval_*.json and eval_*_ragas.csv files live.
RUN_LOG_DIR = Path("run_logs")

IR_METRICS = {
    "recall_at_k": lambda item: item["recall_at_k"],
    "precision_at_k": lambda item: item["precision_at_k"],
    "reciprocal_rank": lambda item: item["reciprocal_rank"],
    "hit": lambda item: 1.0 if item["hit"] else 0.0,
}

RAGAS_METRICS = ["faithfulness", "context_precision", "answer_relevancy"]


def load_per_item(eval_json_path):
    """Load json and return a dict {qa_id: per_item_record}."""
    with open(eval_json_path) as f:
        log = json.load(f)
    return {item["qa_id"]: item for item in log["per_item"]}


# Paired differences for IR metrics
def paired_diffs_ir(items_a, items_b, metric_fn):
    """
    Align two per-qa_id dicts by qa_id intersection and return the paired
    difference array (b - a) for a given metric.
    """
    ids_a = set(items_a.keys())
    ids_b = set(items_b.keys())

    if ids_a != ids_b:
        missing_a = ids_b - ids_a
        missing_b = ids_a - ids_b
        raise ValueError(
            "qa_id mismatch between runs, not directly comparable. \n"
            f"In B but not in A: {sorted(missing_a)}\n"
            f"In A but not in B: {sorted(missing_b)}"
        )

    diffs = np.array(
        [metric_fn(items_b[qid]) - metric_fn(items_a[qid]) for qid in ids_a]
    )
    return diffs


# Paired bootstrap significance test
def paired_bootstrap_test(diffs, n_boot=10000, ci=0.95, seed=42):
    rng = np.random.default_rng(seed)
    n = len(diffs)
    observed_mean = diffs.mean()

    # Bootstrap: repeatedly resample diffs with replacement and compute means.
    boot_means = np.empty(n_boot)
    for b in range(n_boot):
        sample = rng.choice(diffs, size=n, replace=True)
        boot_means[b] = sample.mean()

    # Percentile confidence interval.
    alpha = 1 - ci
    ci_low, ci_high = np.percentile(boot_means, [100 * alpha / 2, 100 * (1 - alpha / 2)])

    # Two-sided p-value (percentile-consistent).
    if observed_mean > 0:
        tail_prob = np.mean(boot_means <= 0)
    elif observed_mean < 0:
        tail_prob = np.mean(boot_means >= 0)
    else:
        tail_prob = 0.5

    p_value = min(2 * tail_prob, 1.0)

    return {
        "n": n,
        "observed_mean_diff": observed_mean,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "ci_excludes_zero": not (ci_low <= 0 <= ci_high),
        "p_value_approx": p_value,
    }


# Run significance tests for IR metrics
def run_ir_significance(path_a, path_b, label_a="A", label_b="B", n_boot=10000):
    items_a = load_per_item(path_a)
    items_b = load_per_item(path_b)

    print(f"\nIR metrics: {label_b} - {label_a}  (n_boot={n_boot})")
    print(
        f"{'metric':<16}"
        f"{'mean_diff':>12}"
        f"{'95% CI':>24}"
        f"{'p (approx)':>12}   sig?"
    )

    results = {}
    for name, fn in IR_METRICS.items():
        diffs = paired_diffs_ir(items_a, items_b, fn)
        res = paired_bootstrap_test(diffs, n_boot=n_boot)
        results[name] = res

        ci_str = f"[{res['ci_low']:+.4f}, {res['ci_high']:+.4f}]"
        sig = "YES" if res["ci_excludes_zero"] else "no"

        print(
            f"{name:<16}"
            f"{res['observed_mean_diff']:>+12.4f}"
            f"{ci_str:>24}"
            f"{res['p_value_approx']:>12.4f}   {sig}"
        )

    return results


# Run significance tests for RAGAS metrics (CSV files)
def run_ragas_significance(csv_a, csv_b, label_a="A", label_b="B", n_boot=10000):
    df_a = pd.read_csv(csv_a)
    df_b = pd.read_csv(csv_b)

    # Try to align by qa_id if present.
    if "qa_id" in df_a.columns and "qa_id" in df_b.columns:
        df_a = df_a.set_index("qa_id")
        df_b = df_b.set_index("qa_id").loc[df_a.index]
    else:
        # No qa_id: fall back to row order, but verify questions match.
        if not df_a["user_input"].equals(df_b["user_input"]):
            raise ValueError(
                "RAGAS CSVs are not in the same question order and have no qa_id "
                "column to align on -- pairing would silently be wrong. Add a "
                "qa_id column to build_ragas_dataset's output before proceeding."
            )
        print("  (paired by row order -- user_input sequence verified identical)")

    print(f"\nRAGAS metrics: {label_b} - {label_a}  (n_boot={n_boot})")
    print(
        f"{'metric':<20}"
        f"{'mean_diff':>12}"
        f"{'95% CI':>24}"
        f"{'p (approx)':>12}   sig?"
    )

    results = {}
    for metric in RAGAS_METRICS:
        diffs = (df_b[metric] - df_a[metric]).to_numpy()
        res = paired_bootstrap_test(diffs, n_boot=n_boot)
        results[metric] = res

        ci_str = f"[{res['ci_low']:+.4f}, {res['ci_high']:+.4f}]"
        sig = "YES" if res["ci_excludes_zero"] else "no"

        print(
            f"{metric:<20}"
            f"{res['observed_mean_diff']:>+12.4f}"
            f"{ci_str:>24}"
            f"{res['p_value_approx']:>12.4f}   {sig}"
        )

    return results


def run_ir_significance_by_num_gold_pages(
    path_a,
    path_b,
    label_a="A",
    label_b="B",
    n_boot=10000,
    num_gold_pages=1,
    label_suffix="",
):
    """
    Run paired bootstrap significance tests for IR metrics on a subset of questions
    defined by the number of gold pages.

    Parameters
    ----------
    path_a, path_b : Path or str
        Paths to eval_*.json files for run A and run B.
    label_a, label_b : str
        Human-readable labels for the runs (used in output).
    n_boot : int
        Number of bootstrap resamples.
    num_gold_pages : int
        Number of gold pages to filter on:
          - 1  → single-source questions
          - 2  → two-source questions
    label_suffix : str
        Extra text to add to the printed header, e.g. " (1 gold page)".

    Returns
    -------
    results : dict
        {metric_name: bootstrap_result_dict, ...} for this subset.
    """
    items_a = load_per_item(path_a)
    items_b = load_per_item(path_b)

    # Ensure same qa_ids in both runs
    ids_a = set(items_a.keys())
    ids_b = set(items_b.keys())
    if ids_a != ids_b:
        missing_a = ids_b - ids_a
        missing_b = ids_a - ids_b
        raise ValueError(
            "qa_id mismatch between runs -- not directly comparable.\n"
            f"  In B but not A: {sorted(missing_a)}\n"
            f"  In A but not B: {sorted(missing_b)}"
        )

    # Filter by number of gold pages
    ids_subset = [
        qid
        for qid in ids_a
        if len(items_a[qid]["gold_pages"]) == num_gold_pages
    ]

    if not ids_subset:
        header = f"IR metrics{label_suffix}: {label_b} - {label_a}  (n_boot={n_boot})"
        print(f"\n{header}")
        print("  (no items in this subset)")
        return {}

    # Build filtered dicts for this subset
    sub_a = {qid: items_a[qid] for qid in ids_subset}
    sub_b = {qid: items_b[qid] for qid in ids_subset}

    header = f"IR metrics{label_suffix}: {label_b} - {label_a}  (n_boot={n_boot})"
    print(f"\n{header}")
    print(
        f"{'metric':<16}"
        f"{'mean_diff':>12}"
        f"{'95% CI':>24}"
        f"{'p (approx)':>12}   sig?"
    )

    results = {}
    for name, fn in IR_METRICS.items():
        diffs = paired_diffs_ir(sub_a, sub_b, fn)
        res = paired_bootstrap_test(diffs, n_boot=n_boot)
        results[name] = res

        ci_str = f"[{res['ci_low']:+.4f}, {res['ci_high']:+.4f}]"
        sig = "YES" if res["ci_excludes_zero"] else "no"

        print(
            f"{name:<16}"
            f"{res['observed_mean_diff']:>+12.4f}"
            f"{ci_str:>24}"
            f"{res['p_value_approx']:>12.4f}   {sig}"
        )

    return results


if __name__ == "__main__":
    #
    # Experiment 1: fixed vs recursive chunking (vector retrieval held constant)
    # --------------------------------------------------------------------------
    # Positive mean_diff means: recursive > fixed for that metric.
    #

    ir_results_1 = run_ir_significance(
        RUN_LOG_DIR / "eval_2026-07-22T11-16-26+00-00_fixed.json",
        RUN_LOG_DIR / "eval_2026-07-21T18-40-31+00-00_recursive.json",
        label_a="fixed",
        label_b="recursive",
        n_boot=10000,
    )

    ragas_results_1 = run_ragas_significance(
        RUN_LOG_DIR / "eval_2026-07-22T11-16-26+00-00_fixed_ragas.csv",
        RUN_LOG_DIR / "eval_2026-07-21T18-40-31+00-00_recursive_ragas.csv",
        label_a="fixed",
        label_b="recursive",
        n_boot=10000,
    )

    #
    # Experiment 2: vector vs hybrid retrieval (recursive chunking held constant)
    # ---------------------------------------------------------------------------
    # Positive mean_diff means: hybrid > vector for that metric.
    #

    # Overall IR + RAGAS (all questions)
    ir_results_2 = run_ir_significance(
        RUN_LOG_DIR / "eval_2026-07-21T18-40-31+00-00_recursive.json",
        RUN_LOG_DIR / "eval_2026-07-27T16-14-10+00-00_recursive_hybrid.json",
        label_a="vector",
        label_b="hybrid",
        n_boot=10000,
    )

    ragas_results_2 = run_ragas_significance(
        RUN_LOG_DIR / "eval_2026-07-21T18-40-31+00-00_recursive_ragas.csv",
        RUN_LOG_DIR / "eval_2026-07-27T16-14-10+00-00_recursive_ragas.csv",
        label_a="vector",
        label_b="hybrid",
        n_boot=10000,
    )

    # By number of gold pages (IR only)
    ir_1gold = run_ir_significance_by_num_gold_pages(
        RUN_LOG_DIR / "eval_2026-07-21T18-40-31+00-00_recursive.json",
        RUN_LOG_DIR / "eval_2026-07-27T16-14-10+00-00_recursive_hybrid.json",
        label_a="vector",
        label_b="hybrid",
        n_boot=10000,
        num_gold_pages=1,
        label_suffix=" (1 gold page)",
    )

    ir_2gold = run_ir_significance_by_num_gold_pages(
        RUN_LOG_DIR / "eval_2026-07-21T18-40-31+00-00_recursive.json",
        RUN_LOG_DIR / "eval_2026-07-27T16-14-10+00-00_recursive_hybrid.json",
        label_a="vector",
        label_b="hybrid",
        n_boot=10000,
        num_gold_pages=2,
        label_suffix=" (2 gold pages)",
    )