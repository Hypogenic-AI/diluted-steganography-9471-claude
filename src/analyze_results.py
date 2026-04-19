"""
Analysis and visualization for Diluted Steganography experiments.
Generates figures and summary statistics.
"""

import json
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Scheme display order (by dilution)
SCHEME_ORDER = ["acrostic", "nth_word_3", "nth_word_5", "trigger_word", "nth_word_10", "nth_word_20"]
SCHEME_LABELS = {
    "acrostic": "Acrostic\n(sentence)",
    "nth_word_3": "Every 3rd\nword",
    "nth_word_5": "Every 5th\nword",
    "trigger_word": "Trigger\nword",
    "nth_word_10": "Every 10th\nword",
    "nth_word_20": "Every 20th\nword",
}
DILUTION_VALUES = {
    "acrostic": 12,  # ~12 words per signal char
    "nth_word_3": 3,
    "nth_word_5": 5,
    "trigger_word": 8,
    "nth_word_10": 10,
    "nth_word_20": 20,
}

MODEL_COLORS = {
    "gpt-4.1": "#10a37f",
    "claude-sonnet-4-5": "#d97706",
    "gemini-2.5-pro": "#4285f4",
}
MODEL_LABELS = {
    "gpt-4.1": "GPT-4.1",
    "claude-sonnet-4-5": "Claude Sonnet 4.5",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
}


def load_results():
    """Load all experiment results."""
    data = {}
    for fname in ["experiment1_encoding.json", "experiment2_extraction.json", "experiment3_detection.json"]:
        fpath = os.path.join(RESULTS_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath) as f:
                data[fname.split(".")[0]] = json.load(f)
    return data


def compute_summary_stats(results, metric_key="per_char_accuracy"):
    """Compute mean, std, CI for each model × scheme combination."""
    grouped = defaultdict(list)
    for r in results:
        key = (r["model"], r["scheme"])
        grouped[key].append(r[metric_key])

    stats_out = {}
    for (model, scheme), values in grouped.items():
        arr = np.array(values)
        n = len(arr)
        mean = np.mean(arr)
        std = np.std(arr, ddof=1) if n > 1 else 0
        ci_95 = 1.96 * std / np.sqrt(n) if n > 1 else 0
        stats_out[(model, scheme)] = {
            "mean": mean,
            "std": std,
            "ci_95": ci_95,
            "n": n,
            "values": values,
        }
    return stats_out


def plot_experiment_1(results):
    """Plot encoding accuracy across dilution levels."""
    stats_data = compute_summary_stats(results, "per_char_accuracy")

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(SCHEME_ORDER))
    width = 0.25
    models = list(MODEL_LABELS.keys())

    for i, model in enumerate(models):
        means = []
        cis = []
        for scheme in SCHEME_ORDER:
            s = stats_data.get((model, scheme), {"mean": 0, "ci_95": 0})
            means.append(s["mean"])
            cis.append(s["ci_95"])
        ax.bar(x + i * width, means, width, label=MODEL_LABELS[model],
               color=MODEL_COLORS[model], yerr=cis, capsize=3, alpha=0.85)

    ax.set_ylabel("Per-Character Accuracy", fontsize=12)
    ax.set_title("Experiment 1: LLM Encoding Accuracy by Dilution Level", fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels([SCHEME_LABELS[s] for s in SCHEME_ORDER], fontsize=9)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.axhline(y=1/26, color='gray', linestyle='--', alpha=0.5, label='Random (1/26)')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    outpath = os.path.join(FIGURES_DIR, "exp1_encoding_accuracy.png")
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {outpath}")

    # Also plot exact match
    stats_em = compute_summary_stats(results, "exact_match")
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, model in enumerate(models):
        means = [stats_em.get((model, s), {"mean": 0})["mean"] for s in SCHEME_ORDER]
        ax.bar(x + i * width, means, width, label=MODEL_LABELS[model],
               color=MODEL_COLORS[model], alpha=0.85)

    ax.set_ylabel("Exact Match Rate", fontsize=12)
    ax.set_title("Experiment 1: Exact Match Rate by Dilution Level", fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels([SCHEME_LABELS[s] for s in SCHEME_ORDER], fontsize=9)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, "exp1_exact_match.png")
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {outpath}")


def plot_experiment_2(results):
    """Plot informed extraction accuracy."""
    stats_data = compute_summary_stats(results, "per_char_accuracy")

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(SCHEME_ORDER))
    width = 0.25
    models = list(MODEL_LABELS.keys())

    for i, model in enumerate(models):
        means = []
        cis = []
        for scheme in SCHEME_ORDER:
            s = stats_data.get((model, scheme), {"mean": 0, "ci_95": 0})
            means.append(s["mean"])
            cis.append(s["ci_95"])
        ax.bar(x + i * width, means, width, label=MODEL_LABELS[model],
               color=MODEL_COLORS[model], yerr=cis, capsize=3, alpha=0.85)

    ax.set_ylabel("Per-Character Extraction Accuracy", fontsize=12)
    ax.set_title("Experiment 2: Informed Extraction Accuracy by Dilution Level", fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels([SCHEME_LABELS[s] for s in SCHEME_ORDER], fontsize=9)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.axhline(y=1/26, color='gray', linestyle='--', alpha=0.5)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    outpath = os.path.join(FIGURES_DIR, "exp2_extraction_accuracy.png")
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {outpath}")


def plot_experiment_3(results):
    """Plot blind detection rates."""
    # Separate stego vs control
    stego_results = [r for r in results if r["has_message"]]
    ctrl_results = [r for r in results if not r["has_message"]]

    # Detection rate (true positive) by model × scheme
    grouped_tp = defaultdict(list)
    for r in stego_results:
        grouped_tp[(r["model"], r["scheme"])].append(1 if r["detected"] else 0)

    # False positive rate by model × scheme
    grouped_fp = defaultdict(list)
    for r in ctrl_results:
        grouped_fp[(r["model"], r["scheme"])].append(1 if r["detected"] else 0)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    x = np.arange(len(SCHEME_ORDER))
    width = 0.25
    models = list(MODEL_LABELS.keys())

    # True positive rate
    ax = axes[0]
    for i, model in enumerate(models):
        means = [np.mean(grouped_tp.get((model, s), [0])) for s in SCHEME_ORDER]
        ax.bar(x + i * width, means, width, label=MODEL_LABELS[model],
               color=MODEL_COLORS[model], alpha=0.85)

    ax.set_ylabel("Detection Rate (True Positive)", fontsize=12)
    ax.set_title("Experiment 3: Blind Detection Rate", fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels([SCHEME_LABELS[s] for s in SCHEME_ORDER], fontsize=9)
    ax.legend(fontsize=9)
    ax.set_ylim(0, 1.15)
    ax.grid(axis='y', alpha=0.3)

    # False positive rate
    ax = axes[1]
    for i, model in enumerate(models):
        means = [np.mean(grouped_fp.get((model, s), [0])) for s in SCHEME_ORDER]
        ax.bar(x + i * width, means, width, label=MODEL_LABELS[model],
               color=MODEL_COLORS[model], alpha=0.85)

    ax.set_ylabel("False Positive Rate", fontsize=12)
    ax.set_title("Experiment 3: False Positive Rate (Control Texts)", fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels([SCHEME_LABELS[s] for s in SCHEME_ORDER], fontsize=9)
    ax.legend(fontsize=9)
    ax.set_ylim(0, 1.15)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, "exp3_detection_rates.png")
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {outpath}")


def plot_dilution_curve():
    """
    Key figure: accuracy vs dilution across all three experiments.
    Shows the dilution-accuracy relationship.
    """
    data = load_results()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    experiments = [
        ("experiment1_encoding", "Encoding Accuracy", "per_char_accuracy"),
        ("experiment2_extraction", "Informed Extraction", "per_char_accuracy"),
    ]

    for ax_idx, (exp_key, title, metric) in enumerate(experiments):
        if exp_key not in data:
            continue
        results = data[exp_key]
        ax = axes[ax_idx]

        for model in MODEL_LABELS:
            dilutions = []
            accuracies = []
            for scheme in SCHEME_ORDER:
                vals = [r[metric] for r in results if r["model"] == model and r["scheme"] == scheme]
                if vals:
                    dilutions.append(DILUTION_VALUES[scheme])
                    accuracies.append(np.mean(vals))

            # Sort by dilution
            pairs = sorted(zip(dilutions, accuracies))
            if pairs:
                ds, accs = zip(*pairs)
                ax.plot(ds, accs, 'o-', label=MODEL_LABELS[model],
                        color=MODEL_COLORS[model], linewidth=2, markersize=8)

        ax.set_xlabel("Dilution (words per signal character)", fontsize=11)
        ax.set_ylabel("Accuracy", fontsize=11)
        ax.set_title(title, fontsize=13)
        ax.legend(fontsize=9)
        ax.set_ylim(-0.05, 1.05)
        ax.axhline(y=1/26, color='gray', linestyle='--', alpha=0.5)
        ax.grid(alpha=0.3)

    # Experiment 3: detection rate
    if "experiment3_detection" in data:
        ax = axes[2]
        results = data["experiment3_detection"]
        stego = [r for r in results if r["has_message"]]

        for model in MODEL_LABELS:
            dilutions = []
            rates = []
            for scheme in SCHEME_ORDER:
                vals = [1 if r["detected"] else 0 for r in stego
                        if r["model"] == model and r["scheme"] == scheme]
                if vals:
                    dilutions.append(DILUTION_VALUES[scheme])
                    rates.append(np.mean(vals))

            pairs = sorted(zip(dilutions, rates))
            if pairs:
                ds, rs = zip(*pairs)
                ax.plot(ds, rs, 'o-', label=MODEL_LABELS[model],
                        color=MODEL_COLORS[model], linewidth=2, markersize=8)

        ax.set_xlabel("Dilution (words per signal character)", fontsize=11)
        ax.set_ylabel("Detection Rate", fontsize=11)
        ax.set_title("Blind Detection Rate", fontsize=13)
        ax.legend(fontsize=9)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(alpha=0.3)

    plt.suptitle("Diluted Steganography: Performance vs Signal Dilution", fontsize=15, y=1.02)
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, "dilution_curve.png")
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {outpath}")


def compute_statistical_tests(results, metric="per_char_accuracy"):
    """Run statistical tests comparing acrostic vs other schemes."""
    print("\n--- Statistical Tests ---")

    for model in MODEL_LABELS:
        print(f"\nModel: {MODEL_LABELS[model]}")
        acrostic_vals = [r[metric] for r in results
                         if r["model"] == model and r["scheme"] == "acrostic"]
        if not acrostic_vals:
            continue

        for scheme in SCHEME_ORDER[1:]:
            other_vals = [r[metric] for r in results
                          if r["model"] == model and r["scheme"] == scheme]
            if not other_vals:
                continue

            # Mann-Whitney U test (doesn't assume normality)
            try:
                stat, p = stats.mannwhitneyu(acrostic_vals, other_vals, alternative='greater')
                # Effect size (rank-biserial correlation)
                n1, n2 = len(acrostic_vals), len(other_vals)
                r_effect = 1 - (2 * stat) / (n1 * n2)

                sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
                print(f"  Acrostic vs {SCHEME_LABELS[scheme].replace(chr(10), ' ')}: "
                      f"U={stat:.0f}, p={p:.4f} {sig}, r={r_effect:.2f}")
            except Exception as e:
                print(f"  Acrostic vs {scheme}: test failed ({e})")

    # Spearman correlation: dilution rank vs accuracy
    print("\n--- Spearman Correlation: Dilution Rank vs Accuracy ---")
    for model in MODEL_LABELS:
        ranks = []
        accs = []
        for r in results:
            if r["model"] == model:
                ranks.append(r["dilution_rank"])
                accs.append(r[metric])
        if ranks:
            rho, p = stats.spearmanr(ranks, accs)
            print(f"  {MODEL_LABELS[model]}: rho={rho:.3f}, p={p:.4f}")


def generate_summary_table(data):
    """Generate a markdown summary table."""
    print("\n\n## Summary Table: Per-Character Accuracy (Mean ± Std)")
    print()

    for exp_name, exp_key, metric in [
        ("Experiment 1: Encoding", "experiment1_encoding", "per_char_accuracy"),
        ("Experiment 2: Extraction", "experiment2_extraction", "per_char_accuracy"),
    ]:
        if exp_key not in data:
            continue
        results = data[exp_key]
        print(f"\n### {exp_name}")
        header = "| Scheme | " + " | ".join(MODEL_LABELS[m] for m in MODEL_LABELS) + " |"
        sep = "|--------|" + "|".join(["--------"] * len(MODEL_LABELS)) + "|"
        print(header)
        print(sep)

        for scheme in SCHEME_ORDER:
            row = f"| {SCHEME_LABELS[scheme].replace(chr(10), ' ')} |"
            for model in MODEL_LABELS:
                vals = [r[metric] for r in results
                        if r["model"] == model and r["scheme"] == scheme]
                if vals:
                    m, s = np.mean(vals), np.std(vals, ddof=1) if len(vals) > 1 else 0
                    row += f" {m:.2f} ± {s:.2f} |"
                else:
                    row += " - |"
            print(row)


if __name__ == "__main__":
    print("Loading results...")
    data = load_results()

    for key in data:
        print(f"  {key}: {len(data[key])} records")

    if "experiment1_encoding" in data:
        print("\n=== EXPERIMENT 1 ANALYSIS ===")
        plot_experiment_1(data["experiment1_encoding"])
        compute_statistical_tests(data["experiment1_encoding"])

    if "experiment2_extraction" in data:
        print("\n=== EXPERIMENT 2 ANALYSIS ===")
        plot_experiment_2(data["experiment2_extraction"])
        compute_statistical_tests(data["experiment2_extraction"])

    if "experiment3_detection" in data:
        print("\n=== EXPERIMENT 3 ANALYSIS ===")
        plot_experiment_3(data["experiment3_detection"])

    plot_dilution_curve()
    generate_summary_table(data)

    print("\n\nAnalysis complete! Check figures/ directory.")
