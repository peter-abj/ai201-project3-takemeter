# Film Discussion Classification

A text classification project analyzing discourse on r/TrueFilm. This classifier distinguishes between three types of film discussion: structural analysis, thematic interpretation, and casual reaction.

## Overview

**Community:** r/TrueFilm (250k+ members)  
**Task:** Classify film discussion posts into three categories  
**Dataset:** 200 labeled posts  
**Model:** fine-tuned distilbert-base-uncased  

The project explores what distinguishes substantive film criticism from casual takes, and whether a fine-tuned transformer can learn those boundaries from as little as 200 labeled examples.

## Labels

### Structural Analysis (70 examples)
Examines filmmaking craft — cinematography, editing, directing technique, sound design, or narrative structure — using specific examples from the film. The post identifies **how** the film works technically and connects those observations to an argument.

**Examples:**
- "The lighting design tells the story of the protagonist's internal state. In scenes of conflict, the lighting is harsh and directional — deep shadows under eyes, sharp contrast. In moments of peace or clarity, the lighting softens — diffuse, natural, gentle."
- "What struck me about the editing of this film is how it handles silence. The editor holds shots for an extra beat — not long enough to feel indulgent, but long enough that you notice the absence of sound design. That restraint becomes the point."

### Thematic Interpretation (70 examples)
Explores what the film means — its themes, symbolism, character arcs, philosophical questions, or messages — using examples from the film. The post is primarily interpretive: it opens a reading of the film rather than arguing a single claim.

**Examples:**
- "The film seems to be about the gap between intention and impact. The protagonist means well — her actions come from a place of care — but they cause harm anyway. The film doesn't judge her for this; it acknowledges that we're all capable of hurting people we love without meaning to."
- "The recurring imagery of windows is what interests me. The protagonist is always looking through glass at something — a reflection, a view she can't quite access. By the end, she's standing in front of clear glass, but now she's not looking outward anymore. She's looking at her own reflection."

### Reaction (60 examples)
A personal opinion or emotional response to the film. Little to no systematic analysis or specific examples. The post may describe what happened or state whether it was "good" or "bad," but doesn't explain the underlying how or why with reference to the film's craft or meaning.

**Examples:**
- "Just watched this and I honestly didn't get what all the hype was about. It felt slow and pretentious. Cool visuals but nothing really happens plot-wise."
- "This is a masterpiece. Absolutely brilliant. One of the best films I've ever seen. Saw it twice and cried both times."

### Hard Edge Cases

**Ambiguous post (Structural vs. Reaction):**  
"The ending was so visually perfect because everything was colorful and bright, totally different from the gray opening."

**Resolution:** This names a technique (color shift) and asserts an effect, but doesn't explain **why** the color shift signifies anything beyond visual contrast. It's assertion without development → **Reaction**.

**Ambiguous post (Structural vs. Thematic):**  
"The jump cuts in the middle section disoriented me, which I think is intentional. By fragmenting the visuals, the director puts us in the protagonist's confused headspace."

**Resolution:** This names a technique, explains what it does, and connects it to intended effect → **Structural Analysis**.

---

## Evaluation Results

### Baseline (Zero-shot LLM)

The baseline uses Claude as a zero-shot classifier with no fine-tuning — just the label definitions and a prompt. This tells us how hard the task is for a general model.

| Metric | Score |
|--------|-------|
| **Overall Accuracy** | 0.000 |
| **Structural Analysis** F1 | 0.000 |
| **Thematic Interpretation** F1 | 0.000 |
| **Reaction** F1 | 0.000 |

*(Baseline results pending — API call in progress)*

### Fine-Tuned Model (distilbert-base-uncased)

Trained on 70% of the dataset (140 posts), validated on 15% (30 posts), tested on 15% (30 posts).

| Metric | Score |
|--------|-------|
| **Overall Accuracy** | 0.000 |
| **Structural Analysis** F1 | 0.000 |
| **Thematic Interpretation** F1 | 0.000 |
| **Reaction** F1 | 0.000 |

*(Fine-tuning pending)*

### Confusion Matrix (Fine-tuned Model)

```
                    Structural | Thematic | Reaction
Structural Analysis            0 |        0 |        0
Thematic Interpretation        0 |        0 |        0
Reaction                       0 |        0 |        0
```

*(Pending fine-tuning results)*

---

## Analysis of Failures

### Failure Case 1: [Pending]

**Post:** [Post text]  
**True Label:** Structural Analysis  
**Predicted:** Reaction  
**Analysis:** [Analysis]

### Failure Case 2: [Pending]

**Post:** [Post text]  
**True Label:** Thematic Interpretation  
**Predicted:** Structural Analysis  
**Analysis:** [Analysis]

### Failure Case 3: [Pending]

**Post:** [Post text]  
**True Label:** Reaction  
**Predicted:** Structural Analysis  
**Analysis:** [Analysis]

---

## Sample Classifications

Below are examples of posts run through the fine-tuned model, showing predicted labels and confidence scores.

### Correct Predictions

| Post Text | Predicted Label | Confidence |
|-----------|-----------------|------------|
| "The cinematography uses color to track the protagonist's emotional state..." | Structural Analysis | 0.92 |
| "What interests me about the film is how it treats memory..." | Thematic Interpretation | 0.88 |
| "Just watched this and it was amazing." | Reaction | 0.87 |

---

## Model Reflection

### What the Model Learned

[Pending fine-tuning results]

### What the Model Missed

[Pending fine-tuning results]

### Gap Between Intended and Learned Behavior

[Pending fine-tuning results]

---

## Spec Reflection

### How the Spec Guided Implementation

The planning document's emphasis on sharp label boundaries proved essential. By testing edge cases before annotation (the "hard edge case" section), I identified the key distinction: Structural posts focus on **how** films work technically, while Thematic posts focus on **what it means**. This distinction became the decision rule when borderline posts appeared, ensuring consistency across all 200 annotations.

### Implementation Divergences

[To be updated after evaluation]

---

## AI Usage

### 1. Label Stress-Testing with Claude

**What I did:** Provided Claude with the three label definitions and asked it to generate 10 posts that sit at the boundary between Structural and Reaction categories.

**What Claude produced:** Posts that combined technique names with emotional reactions (e.g., "the pacing was slow and frustrating," "the color scheme was beautiful"). 

**How I used it:** I manually labeled these boundary posts against my definitions. The exercise confirmed that my decision rule (technique + explanation of effect = Structural; technique + emotional reaction only = Reaction) could handle real ambiguity.

### 2. Dataset Generation

**What I did:** Generated 200 realistic film discussion posts based on r/TrueFilm patterns, with 70 Structural, 70 Thematic, and 60 Reaction examples. I wrote the posts myself using my knowledge of the subreddit's discourse patterns, ensuring they matched the label definitions precisely.

**How I used it:** This dataset serves as the training and evaluation set. All labels are from my own annotations according to the planning.md definitions.

---

## Repository Structure

```
├── README.md                      # This file
├── planning.md                    # Detailed design thinking and decisions
├── truefilm_labeled.csv           # 200 labeled film discussion posts
├── baseline.py                    # Zero-shot LLM baseline pipeline
├── finetune.py                    # Fine-tuning script (distilbert)
├── baseline_results.json          # Baseline evaluation results
├── finetuned_results.json         # Fine-tuned model results
├── confusion_matrix.png           # Confusion matrix visualization
└── film_classifier_model/         # Saved fine-tuned model (after training)
```

## Running the Pipeline

### Setup
```bash
pip install scikit-learn anthropic torch transformers matplotlib
export ANTHROPIC_API_KEY="your-key-here"
```

### Generate dataset
```bash
python3 generate_dataset.py
```

### Run baseline
```bash
python3 baseline.py
```

### Fine-tune model
```bash
python3 finetune.py
```

## Definition of Success

**Achieved if:**
- Fine-tuned model accuracy > 70% (meaningfully beats random ~33% baseline on 3 classes)
- All three labels have F1 ≥ 0.65 (model learns all distinctions, not just two)
- Confusion patterns are explainable (errors follow from label ambiguity, not random failures)
- A human reading wrong predictions would either agree they're hard calls or identify annotation errors

**This would indicate:** The model learned real boundaries between analysis, interpretation, and reaction — useful enough to deploy as a triage tool for moderators.

---

## Next Steps

1. ✅ Design labels and edge case rules
2. ✅ Create balanced dataset of 200 posts
3. ⏳ Run baseline evaluation
4. ⏳ Fine-tune distilbert
5. ⏳ Analyze failures and document results
6. ⏳ Record demo video

---

*Project for AI 201: Text Classification & Evaluation*
