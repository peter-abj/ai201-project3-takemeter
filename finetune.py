#!/usr/bin/env python3
"""
Fine-tune distilbert-base-uncased on film discussion classification.
Trains on labeled data and evaluates on held-out test set.
"""

import csv
import json
import random
from collections import defaultdict
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt

try:
    import torch
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, AdamW, get_linear_schedule_with_warmup
    from torch.utils.data import DataLoader, TensorDataset
except ImportError:
    print("Required packages: torch, transformers")
    print("Install with: pip install torch transformers")
    exit(1)


class FilmDiscussionDataset:
    """Dataset for film discussion classification"""

    def __init__(self, csv_file, train_ratio=0.7, val_ratio=0.15, tokenizer=None, max_length=512):
        self.label2id = {
            "Structural Analysis": 0,
            "Thematic Interpretation": 1,
            "Reaction": 2
        }
        self.id2label = {v: k for k, v in self.label2id.items()}

        # Load data
        posts = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                posts.append({"text": row["text"], "label": row["label"]})

        random.shuffle(posts)

        n = len(posts)
        train_size = int(n * train_ratio)
        val_size = int(n * val_ratio)

        self.train = posts[:train_size]
        self.val = posts[train_size:train_size + val_size]
        self.test = posts[train_size + val_size:]

        print(f"Dataset: {len(self.train)} train, {len(self.val)} val, {len(self.test)} test")

        # Tokenize
        self.tokenizer = tokenizer or DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        self.max_length = max_length

        self.train_encodings = self.tokenizer([p["text"] for p in self.train], truncation=True,
                                              padding=True, max_length=max_length)
        self.val_encodings = self.tokenizer([p["text"] for p in self.val], truncation=True,
                                            padding=True, max_length=max_length)
        self.test_encodings = self.tokenizer([p["text"] for p in self.test], truncation=True,
                                             padding=True, max_length=max_length)

        # Labels
        self.train_labels = [self.label2id[p["label"]] for p in self.train]
        self.val_labels = [self.label2id[p["label"]] for p in self.val]
        self.test_labels = [self.label2id[p["label"]] for p in self.test]

    def get_train_loader(self, batch_size=16):
        """Get training data loader"""
        train_dataset = TensorDataset(
            torch.tensor(self.train_encodings["input_ids"]),
            torch.tensor(self.train_encodings["attention_mask"]),
            torch.tensor(self.train_labels)
        )
        return DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    def get_val_loader(self, batch_size=16):
        """Get validation data loader"""
        val_dataset = TensorDataset(
            torch.tensor(self.val_encodings["input_ids"]),
            torch.tensor(self.val_encodings["attention_mask"]),
            torch.tensor(self.val_labels)
        )
        return DataLoader(val_dataset, batch_size=batch_size)

    def get_test_loader(self, batch_size=16):
        """Get test data loader"""
        test_dataset = TensorDataset(
            torch.tensor(self.test_encodings["input_ids"]),
            torch.tensor(self.test_encodings["attention_mask"]),
            torch.tensor(self.test_labels)
        )
        return DataLoader(test_dataset, batch_size=batch_size)


def train_epoch(model, train_loader, optimizer, scheduler, device):
    """Train one epoch"""
    model.train()
    total_loss = 0

    for batch in train_loader:
        input_ids, attention_mask, labels = [b.to(device) for b in batch]

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss

        loss.backward()
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)


def evaluate(model, eval_loader, device):
    """Evaluate model on dataset"""
    model.eval()
    predictions = []
    true_labels = []

    with torch.no_grad():
        for batch in eval_loader:
            input_ids, attention_mask, labels = [b.to(device) for b in batch]

            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1)

            predictions.extend(preds.cpu().numpy())
            true_labels.extend(labels.cpu().numpy())

    accuracy = accuracy_score(true_labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predictions, labels=[0, 1, 2], zero_division=0
    )

    return accuracy, precision, recall, f1, true_labels, predictions


def train_model(csv_file, epochs=3, batch_size=16, learning_rate=2e-5):
    """Train distilbert model"""

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load dataset
    dataset = FilmDiscussionDataset(csv_file)
    train_loader = dataset.get_train_loader(batch_size)
    val_loader = dataset.get_val_loader(batch_size)
    test_loader = dataset.get_test_loader(batch_size)

    # Load model
    print("Loading distilbert-base-uncased...")
    model = DistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=3
    ).to(device)

    # Optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=total_steps
    )

    # Training loop
    print(f"Training for {epochs} epochs...")
    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader, optimizer, scheduler, device)
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {train_loss:.4f}")

        # Validation
        val_acc, _, _, _, _, _ = evaluate(model, val_loader, device)
        print(f"  Validation accuracy: {val_acc:.3f}")

    # Evaluate on test set
    print("\nEvaluating on test set...")
    test_acc, precision, recall, f1, true_labels, predictions = evaluate(model, test_loader, device)

    # Confusion matrix
    cm = confusion_matrix(true_labels, predictions, labels=[0, 1, 2])

    # Results
    results = {
        "accuracy": test_acc,
        "per_class_metrics": {
            "Structural Analysis": {"precision": precision[0], "recall": recall[0], "f1": f1[0]},
            "Thematic Interpretation": {"precision": precision[1], "recall": recall[1], "f1": f1[1]},
            "Reaction": {"precision": precision[2], "recall": recall[2], "f1": f1[2]}
        },
        "confusion_matrix": cm.tolist()
    }

    print("\n" + "="*60)
    print("FINE-TUNED MODEL RESULTS")
    print("="*60)
    print(f"Test Accuracy: {test_acc:.3f}")
    print("\nPer-class metrics:")
    for label, metrics in results["per_class_metrics"].items():
        print(f"\n{label}:")
        print(f"  Precision: {metrics['precision']:.3f}")
        print(f"  Recall: {metrics['recall']:.3f}")
        print(f"  F1: {metrics['f1']:.3f}")

    print("\nConfusion Matrix:")
    print("                    Structural | Thematic | Reaction")
    labels = ["Structural Analysis", "Thematic Interpretation", "Reaction"]
    for i, row_label in enumerate(labels):
        row = cm[i]
        print(f"{row_label:25} {row[0]:>10} | {row[1]:>8} | {row[2]:>8}")

    # Save results and model
    with open("finetuned_results.json", "w") as f:
        json.dump(results, f, indent=2)

    model.save_pretrained("./film_classifier_model")
    print("\nModel saved to ./film_classifier_model")
    print("Results saved to finetuned_results.json")

    # Plot confusion matrix
    plot_confusion_matrix(cm, ["Structural Analysis", "Thematic Interpretation", "Reaction"])

    return model, results, dataset


def plot_confusion_matrix(cm, labels):
    """Plot and save confusion matrix"""
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, cmap="Blues")

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)

    ax.set_ylabel("True Label")
    ax.set_xlabel("Predicted Label")
    ax.set_title("Confusion Matrix - Fine-tuned Model")

    # Add text annotations
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, cm[i, j], ha="center", va="center", color="black")

    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=150, bbox_inches="tight")
    print("Confusion matrix saved to confusion_matrix.png")


if __name__ == "__main__":
    model, results, dataset = train_model("truefilm_labeled.csv", epochs=3, batch_size=16)
