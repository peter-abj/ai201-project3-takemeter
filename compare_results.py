#!/usr/bin/env python3
"""
Compare baseline vs fine-tuned model results.
Loads both JSON result files and generates a comparison report.
"""

import json
import pandas as pd


def compare_results():
    """Load and compare baseline vs fine-tuned results"""

    # Load results
    try:
        with open("baseline_results.json") as f:
            baseline = json.load(f)
    except FileNotFoundError:
        print("baseline_results.json not found — run baseline.py first")
        return

    try:
        with open("finetuned_results.json") as f:
            finetuned = json.load(f)
    except FileNotFoundError:
        print("finetuned_results.json not found — run finetune.py first")
        return

    # Print comparison
    print("\n" + "="*80)
    print("BASELINE vs FINE-TUNED MODEL COMPARISON")
    print("="*80)

    print(f"\n{'Metric':<30} {'Baseline':<20} {'Fine-tuned':<20} {'Improvement':<15}")
    print("-" * 85)

    baseline_acc = baseline.get("accuracy", 0)
    finetuned_acc = finetuned.get("accuracy", 0)
    improvement = finetuned_acc - baseline_acc

    print(f"{'Overall Accuracy':<30} {baseline_acc:<20.3f} {finetuned_acc:<20.3f} {improvement:+.3f}")

    print("\n" + "-" * 85)
    print("\nPER-CLASS METRICS (F1):")
    print("-" * 85)
    print(f"{'Label':<30} {'Baseline':<20} {'Fine-tuned':<20} {'Improvement':<15}")
    print("-" * 85)

    labels = ["Structural Analysis", "Thematic Interpretation", "Reaction"]
    for label in labels:
        baseline_f1 = baseline.get("per_class_metrics", {}).get(label, {}).get("f1", 0)
        finetuned_f1 = finetuned.get("per_class_metrics", {}).get(label, {}).get("f1", 0)
        improvement = finetuned_f1 - baseline_f1

        print(f"{label:<30} {baseline_f1:<20.3f} {finetuned_f1:<20.3f} {improvement:+.3f}")

    print("\n" + "-" * 85)
    print("\nDETAILED BASELINE METRICS:")
    print("-" * 85)
    for label in labels:
        metrics = baseline.get("per_class_metrics", {}).get(label, {})
        print(f"\n{label}:")
        print(f"  Precision: {metrics.get('precision', 0):.3f}")
        print(f"  Recall: {metrics.get('recall', 0):.3f}")
        print(f"  F1: {metrics.get('f1', 0):.3f}")

    print("\n" + "-" * 85)
    print("\nDETAILED FINE-TUNED METRICS:")
    print("-" * 85)
    for label in labels:
        metrics = finetuned.get("per_class_metrics", {}).get(label, {})
        print(f"\n{label}:")
        print(f"  Precision: {metrics.get('precision', 0):.3f}")
        print(f"  Recall: {metrics.get('recall', 0):.3f}")
        print(f"  F1: {metrics.get('f1', 0):.3f}")

    # Success criteria
    print("\n" + "="*80)
    print("SUCCESS CRITERIA:")
    print("="*80)

    criteria = {
        "Overall accuracy > 70%": finetuned_acc > 0.70,
        "All F1 scores ≥ 0.65": all(
            finetuned.get("per_class_metrics", {}).get(label, {}).get("f1", 0) >= 0.65
            for label in labels
        ),
        "Beats baseline": finetuned_acc > baseline_acc
    }

    for criterion, met in criteria.items():
        status = "✓ PASSED" if met else "✗ FAILED"
        print(f"{criterion:<40} {status}")

    print("\n" + "="*80)

    # Save comparison to JSON
    comparison = {
        "baseline_accuracy": baseline_acc,
        "finetuned_accuracy": finetuned_acc,
        "accuracy_improvement": improvement,
        "baseline_results": baseline,
        "finetuned_results": finetuned,
        "criteria_met": criteria
    }

    with open("comparison.json", "w") as f:
        json.dump(comparison, f, indent=2)

    print("Comparison saved to comparison.json")


if __name__ == "__main__":
    compare_results()
