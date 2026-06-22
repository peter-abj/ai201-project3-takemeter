#!/usr/bin/env python3
"""
Run zero-shot baseline on test set using an LLM.
This establishes baseline performance before fine-tuning.

Requires: Claude API key via environment variable ANTHROPIC_API_KEY
"""

import csv
import json
import random
from collections import defaultdict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import numpy as np

try:
    import anthropic
except ImportError:
    print("anthropic package required. Install with: pip install anthropic")
    exit(1)


def load_and_split_data(csv_file, train_ratio=0.7, val_ratio=0.15):
    """Load CSV and split into train/val/test"""
    posts = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            posts.append({"text": row["text"], "label": row["label"]})

    random.shuffle(posts)

    n = len(posts)
    train_size = int(n * train_ratio)
    val_size = int(n * val_ratio)

    train = posts[:train_size]
    val = posts[train_size:train_size + val_size]
    test = posts[train_size + val_size:]

    print(f"Dataset split: {len(train)} train, {len(val)} val, {len(test)} test")
    print(f"Label distribution in train: {defaultdict(int, {p['label']: 0 for p in train})}")
    for post in train:
        # Count
        pass
    label_counts = defaultdict(int)
    for post in train:
        label_counts[post["label"]] += 1
    print(f"  {dict(label_counts)}")

    return train, val, test


def create_baseline_prompt(label_definitions):
    """Create the zero-shot classification prompt"""
    return f"""You are a film discussion classifier. Classify the following post into ONE of these categories:

1. Structural Analysis: Examines the filmmaking craft (cinematography, editing, directing, sound design, narrative structure) using specific examples from the film. The post identifies how the film works technically and connects observations to an argument.

2. Thematic Interpretation: Explores what the film means (its themes, symbolism, character arcs, philosophical questions, or messages) using examples from the film. The post is interpretive and opens a reading of the film.

3. Reaction: A personal opinion or emotional response to the film. Little to no systematic analysis or specific examples. The post describes what happened or states whether it was good/bad without explaining the underlying how or why.

IMPORTANT: Respond with ONLY the label name, nothing else. Choose from: "Structural Analysis", "Thematic Interpretation", or "Reaction".

Post to classify:
"""


def run_baseline(test_set, label_definitions):
    """Run zero-shot LLM baseline on test set"""

    client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var
    prompt_template = create_baseline_prompt(label_definitions)

    predictions = []
    true_labels = []
    unparseable = 0

    print(f"\nRunning baseline on {len(test_set)} test examples...")

    for i, example in enumerate(test_set):
        text = example["text"]
        true_label = example["label"]

        full_prompt = prompt_template + f"\n{text}"

        try:
            message = client.messages.create(
                model="claude-opus-4-8",
                max_tokens=10,
                messages=[{"role": "user", "content": full_prompt}]
            )

            response = message.content[0].text.strip()

            # Parse response
            if "Structural Analysis" in response:
                pred = "Structural Analysis"
            elif "Thematic Interpretation" in response:
                pred = "Thematic Interpretation"
            elif "Reaction" in response:
                pred = "Reaction"
            else:
                # Try fuzzy matching
                if "structural" in response.lower() or "craft" in response.lower():
                    pred = "Structural Analysis"
                elif "thematic" in response.lower() or "meaning" in response.lower():
                    pred = "Thematic Interpretation"
                elif "reaction" in response.lower() or "opinion" in response.lower():
                    pred = "Reaction"
                else:
                    unparseable += 1
                    pred = None

            if pred:
                predictions.append(pred)
                true_labels.append(true_label)

            if (i + 1) % 20 == 0:
                print(f"  Processed {i + 1}/{len(test_set)}")

        except Exception as e:
            print(f"Error on example {i}: {e}")
            unparseable += 1

    # Calculate metrics
    accuracy = accuracy_score(true_labels, predictions)
    precision, recall, f1, support = precision_recall_fscore_support(
        true_labels, predictions, labels=["Structural Analysis", "Thematic Interpretation", "Reaction"],
        zero_division=0
    )

    cm = confusion_matrix(true_labels, predictions,
                          labels=["Structural Analysis", "Thematic Interpretation", "Reaction"])

    results = {
        "accuracy": accuracy,
        "unparseable_count": unparseable,
        "total_test": len(test_set),
        "successful_predictions": len(predictions),
        "per_class_metrics": {
            "Structural Analysis": {"precision": precision[0], "recall": recall[0], "f1": f1[0]},
            "Thematic Interpretation": {"precision": precision[1], "recall": recall[1], "f1": f1[1]},
            "Reaction": {"precision": precision[2], "recall": recall[2], "f1": f1[2]}
        },
        "confusion_matrix": cm.tolist()
    }

    return results, true_labels, predictions


def main():
    import os

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        exit(1)

    # Load data
    train, val, test = load_and_split_data("truefilm_labeled.csv")

    # Label definitions (from planning.md)
    label_definitions = {
        "Structural Analysis": "examines filmmaking craft (cinematography, editing, directing, sound design, narrative structure) with specific examples",
        "Thematic Interpretation": "explores what the film means (themes, symbolism, character development, messages) with examples",
        "Reaction": "personal opinion or emotional response; little systematic analysis or examples"
    }

    # Run baseline
    results, true_labels, predictions = run_baseline(test, label_definitions)

    # Print results
    print("\n" + "="*60)
    print("BASELINE RESULTS (Zero-shot LLM)")
    print("="*60)
    print(f"Overall Accuracy: {results['accuracy']:.3f}")
    print(f"Successful predictions: {results['successful_predictions']}/{results['total_test']}")
    print(f"Unparseable responses: {results['unparseable_count']}")

    print("\nPer-class metrics:")
    for label, metrics in results["per_class_metrics"].items():
        print(f"\n{label}:")
        print(f"  Precision: {metrics['precision']:.3f}")
        print(f"  Recall: {metrics['recall']:.3f}")
        print(f"  F1: {metrics['f1']:.3f}")

    print("\nConfusion Matrix (rows=true, cols=predicted):")
    print("                    Structural | Thematic | Reaction")
    labels = ["Structural Analysis", "Thematic Interpretation", "Reaction"]
    for i, row_label in enumerate(labels):
        row = results["confusion_matrix"][i]
        print(f"{row_label:25} {row[0]:>10} | {row[1]:>8} | {row[2]:>8}")

    # Save results
    with open("baseline_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to baseline_results.json")

    return results


if __name__ == "__main__":
    main()
