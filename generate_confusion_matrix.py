#!/usr/bin/env python3
"""Generate confusion matrix visualization"""

import json
import numpy as np
import matplotlib.pyplot as plt

with open("finetuned_results.json") as f:
    results = json.load(f)

cm = np.array(results["confusion_matrix"])

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

labels = ["Structural\nAnalysis", "Thematic\nInterpretation", "Reaction"]

# Plot heatmap
im = ax.imshow(cm, cmap="Blues", aspect='auto')

# Set ticks and labels
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(labels, fontsize=11)
ax.set_yticklabels(labels, fontsize=11)

ax.set_ylabel("True Label", fontsize=12, fontweight='bold')
ax.set_xlabel("Predicted Label", fontsize=12, fontweight='bold')
ax.set_title("Fine-Tuned Model Confusion Matrix\n(n=60 test examples)", fontsize=13, fontweight='bold', pad=20)

# Add text annotations
for i in range(len(labels)):
    for j in range(len(labels)):
        value = cm[i, j]
        text_color = "white" if value > cm.max() / 2 else "black"
        text = ax.text(j, i, int(value), ha="center", va="center",
                      color=text_color, fontsize=14, fontweight='bold')

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Count", fontsize=11)

plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150, bbox_inches="tight")
print("Saved confusion_matrix.png")

# Also print as text table
print("\nConfusion Matrix (rows=true label, cols=predicted label):")
print("=" * 60)
header = "True / Pred"
print(f"{header:<25} Structural | Thematic | Reaction")
print("-" * 60)
for i, label in enumerate(["Structural Analysis", "Thematic Interp.", "Reaction"]):
    row = cm[i]
    print(f"{label:<25} {row[0]:>10} | {row[1]:>8} | {row[2]:>8}")
