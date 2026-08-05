

# eval_significance.py
# Paired bootstrap significance testing for Experiment 1 (chunking) / Experiment 2 (retrieval),
# including subgroup analysis by question_type (extractive vs synthesis).
#
# References:
# - Smucker, Allan, Carterette (2007), "A comparison of statistical significance
#   tests for information retrieval evaluation", CIKM '07 -- bootstrap/permutation
#   preferred over Wilcoxon/sign tests for paired IR comparisons.
# - Holm (1979) step-down procedure for multiple-comparison correction, applied
#   across the full family of tests run in a single analysis session.

from pathlib import Path
import json
import numpy as np
import pandas as pd

RUN_LOG_DIR = Path("run_logs")

IR_METRICS = {
    "recall_at_k": lambda item: item["recall_at_k"],
    "precision_at_k": lambda item: item["precision_at_k"],
    "reciprocal_rank": lambda item: item["reciprocal_rank"],
    "hit": lambda item: 1.0 if item["hit"] else 0.0,
}

RAGAS_METRICS = ["faithfulness", "context_precision", "answer_relevancy"]


def load_per_item(eval_json_path):
    with open(eval_json_path) as f:
        log = json.load(f)
    return {item["qa_id"]: item for item in log["per_item"]}


def paired_diffs_ir(items_a, items_b, metric_fn):
    ids_a, ids_b = set(items_a), set(items_b)
    if ids_a != ids_b:
        missing_a = ids_b - ids_a
        missing_b = ids_a - ids_b
        raise ValueError(
            f"qa_id mismatch between runs -- not directly comparable.\n"
            f"  In B but not A: {sorted(missing_a)}\n"
            f"  In A but not B: {sorted(missing_b)}"
        )
    diffs = np.array([metric_fn(items_b[qid]) - metric_fn(items_a[qid]) for qid in ids_a])
    return diffs


def paired_bootstrap_test(diffs, n_boot=10000, ci=0.95, seed=42):
    rng = np.random.default_rng(seed)
    n = len(diffs)
    observed_mean = diffs.mean()

    boot_means = np.empty(n_boot)
    for b in range(n_boot):
        sample = rng.choice(diffs, size=n, replace=True)
        boot_means[b] = sample.mean()

    alpha = 1 - ci
    ci_low, ci_high = np.percentile(boot_means, [100 * alpha / 2, 100 * (1 - alpha / 2)])

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


def holm_correction(results_list):
    """
    Holm step-down correction across a family of results (each a dict with
    'label' and 'p_value_approx'). Adds 'p_holm' and 'significant_holm' in place.
    """
    n = len(results_list)
    indexed = list(enumerate(results_list))
    indexed.sort(key=lambda x: x[1]["p_value_approx"])

    prev_adjusted = 0.0
    for rank, (orig_idx, res) in enumerate(indexed):
        adjusted = (n - rank) * res["p_value_approx"]
        adjusted = max(adjusted, prev_adjusted)
        adjusted = min(adjusted, 1.0)
        res["p_holm"] = adjusted
        res["significant_holm"] = adjusted < 0.05
        prev_adjusted = adjusted

    return results_list


def run_ir_significance(path_a, path_b, label_a="A", label_b="B", n_boot=10000,
                         question_type=None, label_suffix=""):
    items_a = load_per_item(path_a)
    items_b = load_per_item(path_b)

    if question_type is not None:
        keep = [qid for qid in items_a if items_a[qid]["question_type"] == question_type]
        items_a = {qid: items_a[qid] for qid in keep}
        items_b = {qid: items_b[qid] for qid in keep}

    header = f"IR metrics{label_suffix}: {label_b} - {label_a}  (n={len(items_a)}, n_boot={n_boot})"
    print(f"\n{header}")
    if not items_a:
        print("  (no items in this subset)")
        return {}

    print(f"{'metric':<16}{'mean_diff':>12}{'95% CI':>24}{'p (approx)':>12}   sig?")
    results = {}
    for name, fn in IR_METRICS.items():
        diffs = paired_diffs_ir(items_a, items_b, fn)
        res = paired_bootstrap_test(diffs, n_boot=n_boot)
        res["label"] = f"IR{label_suffix}: {name}"
        results[name] = res
        ci_str = f"[{res['ci_low']:+.4f}, {res['ci_high']:+.4f}]"
        sig = "YES" if res["ci_excludes_zero"] else "no"
        print(f"{name:<16}{res['observed_mean_diff']:>+12.4f}{ci_str:>24}{res['p_value_approx']:>12.4f}   {sig}")
    return results


def run_ragas_significance(csv_a, csv_b, label_a="A", label_b="B", n_boot=10000,
                            question_type=None, qa_set=None, label_suffix=""):
    df_a = pd.read_csv(csv_a)
    df_b = pd.read_csv(csv_b)

    has_qa_id = "qa_id" in df_a.columns and "qa_id" in df_b.columns

    if has_qa_id:
        df_a = df_a.set_index("qa_id")
        df_b = df_b.set_index("qa_id").loc[df_a.index]
    else:
        if not df_a["user_input"].equals(df_b["user_input"]):
            raise ValueError(
                "RAGAS CSVs are not in the same question order and have no qa_id "
                "column to align on. Apply the build_ragas_dataset qa_id patch "
                "and re-run evaluation before proceeding."
            )
        print("  (paired by row order -- user_input sequence verified identical)")

    if question_type is not None:
        if not has_qa_id:
            raise ValueError(
                "Subgroup filtering by question_type requires a qa_id column in "
                "the RAGAS CSVs -- apply the build_ragas_dataset patch and re-run "
                "evaluation before filtering by subgroup."
            )
        if qa_set is None:
            raise ValueError("qa_set must be provided to map qa_id -> question_type.")
        type_map = {item["qa_id"]: item["question_type"] for item in qa_set}
        keep_ids = [qid for qid in df_a.index if type_map.get(qid) == question_type]
        df_a = df_a.loc[keep_ids]
        df_b = df_b.loc[keep_ids]

    header = f"RAGAS metrics{label_suffix}: {label_b} - {label_a}  (n={len(df_a)}, n_boot={n_boot})"
    print(f"\n{header}")
    if len(df_a) == 0:
        print("  (no items in this subset)")
        return {}

    print(f"{'metric':<20}{'mean_diff':>12}{'95% CI':>24}{'p (approx)':>12}   sig?")
    results = {}
    for metric in RAGAS_METRICS:
        diffs = (df_b[metric] - df_a[metric]).to_numpy()
        res = paired_bootstrap_test(diffs, n_boot=n_boot)
        res["label"] = f"RAGAS{label_suffix}: {metric}"
        results[metric] = res
        ci_str = f"[{res['ci_low']:+.4f}, {res['ci_high']:+.4f}]"
        sig = "YES" if res["ci_excludes_zero"] else "no"
        print(f"{metric:<20}{res['observed_mean_diff']:>+12.4f}{ci_str:>24}{res['p_value_approx']:>12.4f}   {sig}")
    return results


if __name__ == "__main__":
    from qa_set import QA_SET  # needed for RAGAS subgroup filtering by qa_id

    print("=" * 70)
    print("EXPERIMENT 1: fixed vs recursive chunking (own Holm family)")
    print("=" * 70)
    exp1_results = []
    r = run_ir_significance(
        RUN_LOG_DIR / "eval_2026-08-05T15-53-56+00-00_fixed_vector.json",
        RUN_LOG_DIR / "eval_2026-08-05T16-08-52+00-00_recursive_vector.json",
        label_a="fixed", label_b="recursive",
    )
    exp1_results.extend(r.values())
    r = run_ragas_significance(
        RUN_LOG_DIR / "eval_2026-08-05T15-53-56+00-00_fixed_vector_ragas.csv",
        RUN_LOG_DIR / "eval_2026-08-05T16-08-52+00-00_recursive_vector_ragas.csv",
        label_a="fixed", label_b="recursive",
    )
    exp1_results.extend(r.values())

    print(f"\nHOLM CORRECTION -- Experiment 1 ({len(exp1_results)} tests, alpha=0.05)")
    holm_correction(exp1_results)
    print(f"{'test':<45}{'p_raw':>10}{'p_holm':>10}   sig (holm)?")
    for res in sorted(exp1_results, key=lambda r: r["p_value_approx"]):
        sig = "YES" if res["significant_holm"] else "no"
        print(f"{res['label']:<45}{res['p_value_approx']:>10.4f}{res['p_holm']:>10.4f}   {sig}")

    # --- Experiment 2: UPDATE these 4 paths to the NEW post-merge eval runs ---
    NEW_VECTOR_JSON = RUN_LOG_DIR / "eval_2026-08-05T16-08-52+00-00_recursive_vector.json"
    NEW_HYBRID_JSON = RUN_LOG_DIR / "eval_2026-08-05T16-20-37+00-00_recursive_hybrid.json"
    NEW_VECTOR_RAGAS = RUN_LOG_DIR / "eval_2026-08-05T16-08-52+00-00_recursive_vector_ragas.csv"
    NEW_HYBRID_RAGAS = RUN_LOG_DIR / "eval_2026-08-05T16-20-37+00-00_recursive_hybrid_ragas.csv"

    # Two independent analyses, each on its own subgroup -- no merged/overall run.
    # Each subgroup gets its OWN Holm correction: these are treated as two
    # separate research questions (extractive-question retrieval quality vs.
    # synthesis-question retrieval quality), not one pooled experiment, so each
    # family's false-positive rate is controlled independently rather than
    # pooling both into a single correction that would implicitly re-merge them.

    print("=" * 70)
    print("EXPERIMENT 2a: vector vs hybrid retrieval -- EXTRACTIVE questions only")
    print("=" * 70)
    extractive_results = []
    r = run_ir_significance(NEW_VECTOR_JSON, NEW_HYBRID_JSON, label_a="vector", label_b="hybrid",
                             question_type="extractive", label_suffix=" (extractive)")
    extractive_results.extend(r.values())
    r = run_ragas_significance(NEW_VECTOR_RAGAS, NEW_HYBRID_RAGAS, label_a="vector", label_b="hybrid",
                                question_type="extractive", qa_set=QA_SET, label_suffix=" (extractive)")
    extractive_results.extend(r.values())

    print(f"\nHOLM CORRECTION -- extractive subgroup ({len(extractive_results)} tests, alpha=0.05)")
    holm_correction(extractive_results)
    print(f"{'test':<45}{'p_raw':>10}{'p_holm':>10}   sig (holm)?")
    for res in sorted(extractive_results, key=lambda r: r["p_value_approx"]):
        sig = "YES" if res["significant_holm"] else "no"
        print(f"{res['label']:<45}{res['p_value_approx']:>10.4f}{res['p_holm']:>10.4f}   {sig}")

    print("\n" + "=" * 70)
    print("EXPERIMENT 2b: vector vs hybrid retrieval -- SYNTHESIS questions only")
    print("=" * 70)
    synthesis_results = []
    r = run_ir_significance(NEW_VECTOR_JSON, NEW_HYBRID_JSON, label_a="vector", label_b="hybrid",
                             question_type="synthesis", label_suffix=" (synthesis)")
    synthesis_results.extend(r.values())
    r = run_ragas_significance(NEW_VECTOR_RAGAS, NEW_HYBRID_RAGAS, label_a="vector", label_b="hybrid",
                                question_type="synthesis", qa_set=QA_SET, label_suffix=" (synthesis)")
    synthesis_results.extend(r.values())

    print(f"\nHOLM CORRECTION -- synthesis subgroup ({len(synthesis_results)} tests, alpha=0.05)")
    holm_correction(synthesis_results)
    print(f"{'test':<45}{'p_raw':>10}{'p_holm':>10}   sig (holm)?")
    for res in sorted(synthesis_results, key=lambda r: r["p_value_approx"]):
        sig = "YES" if res["significant_holm"] else "no"
        print(f"{res['label']:<45}{res['p_value_approx']:>10.4f}{res['p_holm']:>10.4f}   {sig}")