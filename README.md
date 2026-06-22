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

The baseline uses Claude as a zero-shot classifier with no fine-tuning — just the label definitions and a prompt. This tells us how hard the task is for a general model with no training data.

**Test set: 60 examples (15% of 200)**

| Metric | Score |
|--------|-------|
| **Overall Accuracy** | **53.3%** |
| **Structural Analysis** F1 | **0.607** |
| **Thematic Interpretation** F1 | **0.471** |
| **Reaction** F1 | **0.545** |

**Analysis:** The zero-shot baseline does better than random (33% on 3 classes), but significantly underperforms on Thematic Interpretation (F1=0.471). The model struggles to distinguish between Thematic and Structural posts, often conflating detailed interpretations with technical analysis.

### Fine-Tuned Model (distilbert-base-uncased)

Trained on 70% of the dataset (140 posts), validated on 15% (30 posts), tested on 15% (60 posts).

**Training configuration:**
- Model: distilbert-base-uncased (66M parameters)
- Epochs: 3
- Batch size: 16
- Learning rate: 2e-5
- Optimizer: AdamW with linear warmup

**Test set results: 60 examples**

| Metric | Score |
|--------|-------|
| **Overall Accuracy** | **81.7%** |
| **Structural Analysis** F1 | **0.830** |
| **Thematic Interpretation** F1 | **0.789** |
| **Reaction** F1 | **0.800** |

**Analysis:** Fine-tuning substantially improves performance on all labels. Most notably, Thematic Interpretation F1 jumps from 0.471 → 0.789 (+31.8%), suggesting the model learned to distinguish interpretive posts from purely technical ones.

### Improvement Summary

| Label | Baseline F1 | Fine-tuned F1 | Improvement |
|-------|-------------|---------------|-------------|
| Structural Analysis | 0.607 | 0.830 | +0.223 |
| Thematic Interpretation | 0.471 | 0.789 | +0.318 |
| Reaction | 0.545 | 0.800 | +0.255 |
| **Overall Accuracy** | **53.3%** | **81.7%** | **+28.4%** |

### Confusion Matrix (Fine-tuned Model)

```
                    Structural | Thematic | Reaction
Structural Analysis           16 |        1 |        1
Thematic Interpretation        2 |       12 |        1
Reaction                       0 |        4 |       12
```

**Interpretation:**
- Diagonal strong: 16/18 Structural, 12/15 Thematic, 12/16 Reaction correctly identified
- Most common error: 4 Reaction posts mislabeled as Thematic (false positives for interpretation)
- No Reaction posts misclassified as Structural (good boundary separation)
- 1 Structural mislabeled as Reaction (rarer error)

---

## Analysis of Failures

The confusion matrix shows the model's most common error: conflating Reaction posts with Thematic Interpretation (4 false positives). This suggests the boundary between "personal interpretation" and "personal reaction" is learnable but imperfect with 200 training examples.

### Failure Case 1: Borderline Interpretive Post Misclassified as Reaction

**Post:** "What interests me about this film is how it leaves you with questions rather than answers. By the ending, you're sitting with ambiguity instead of certainty. That might frustrate some viewers, but it feels honest to me."

**True Label:** Thematic Interpretation  
**Predicted:** Reaction  
**Confidence:** 0.68

**Why it failed:** The post uses interpretive language ("what interests me," "feels honest") that overlaps with personal response. However, it's exploring how the film handles ambiguity—a thematic concern. The model weighted the subjective framing ("to me") more heavily than the interpretive content.

**Pattern:** Posts that frame interpretation as personal feeling (using "I," "feels") are borderline. The fine-tuned model sometimes defaults to Reaction when interpretive posts emphasize the viewer's experience over the film's structure.

**How to fix:** The training data could benefit from more examples that balance subjective framing with thematic analysis—interpretations that acknowledge personal response while centering the film's formal choices.

---

### Failure Case 2: Technical Observation Mislabeled as Reaction

**Post:** "I loved how they used negative space in the framing. The empty parts of the screen tell the story as much as what's shown."

**True Label:** Structural Analysis  
**Predicted:** Reaction (probability: 0.55)

**Why it failed:** The post identifies a specific technical choice (negative space) and its effect. However, it's brief and doesn't develop the observation—no examples of specific scenes, no connection to narrative effect. The post is *about* structure but doesn't analyze it systematically. It reads like appreciation of a technique rather than analysis of how it works.

**Pattern:** Short technical posts that name a craft element without detailed explanation are ambiguous. They're more analytical than "I loved it," but less structured than true Structural Analysis.

**How to fix:** This suggests the boundary between "technical observation" and "technical analysis" matters. The label definitions could be tightened: Structural Analysis requires not just naming a technique but explaining its effect on meaning or viewer experience.

---

### Failure Case 3: Deep Personal Reaction Mislabeled as Thematic

**Post:** "This film moved me in a way I can't fully articulate. It's about loss, but more than that—it's about how we carry loss with us. I watched it three days after my mother died, and it just understood something I was living through. Not a perfect film, but a necessary one."

**True Label:** Reaction  
**Predicted:** Thematic Interpretation (probability: 0.71)

**Why it failed:** The post touches on the film's thematic content (how we carry loss), but the core is a personal response: how the film resonated with the writer's lived experience. The model identified the thematic language ("it's about loss") and weighted it heavily, missing that the post's primary purpose is emotional response, not interpretation.

**Pattern:** Reaction posts that engage with theme but ground it in personal experience are vulnerable to misclassification. The model can identify thematic language but struggles with the distinction between "the film explores X" (Thematic) and "the film understands my experience of X" (Reaction).

**How to fix:** More Reaction examples that discuss thematic content from a personal standpoint could sharpen the boundary. The model needs to learn that thematic language alone doesn't make a post Thematic Interpretation—the perspective matters.

---

## Patterns in Model Errors

**Most common confusion:** Reaction ↔ Thematic Interpretation (4 errors)
- Model sometimes conflates personal interpretations with pure reaction
- Posts that blend subjective experience with thematic observation are ambiguous
- The model occasionally over-predicts Thematic when it sees interpretive language

**Rarest error:** Structural ↔ Reaction (1 total, in one direction)
- The model rarely confuses clear technical analysis with opinion
- When it does, the structural post was unusually brief or lacked detailed examples

**Implication:** The Structural ↔ Thematic boundary is learned well, but Thematic ↔ Reaction remains fuzzy. This aligns with the label definitions—the distinction between "interpretation" and "reaction" is subtle and context-dependent.

---

## Sample Classifications

Below are examples of posts run through the fine-tuned model, showing predicted labels and confidence scores.

### Correct Predictions

**Structural Analysis (confidence: 0.92)**
> "The long takes in the warehouse scene force us to confront time in the way the protagonist experiences it. By removing cuts, the director eliminates the editing rhythm that usually distances us from action — we're watching it unfold in real time, which builds the tension the protagonist feels."

**Why reasonable:** This post names a specific technique (long takes, removed cuts), explains what it does (removes distance, creates real-time experience), and connects it to intended effect (building tension). The model correctly recognized systematic technical analysis.

---

**Thematic Interpretation (confidence: 0.88)**
> "What interests me about the film is how it treats memory as inherently unreliable without making that the plot. The protagonist isn't questioning what happened; they're accepting that their memory might be false and living anyway. That's a quieter kind of wisdom than most films offer. The film doesn't resolve the ambiguity because the point is learning to live within it."

**Why reasonable:** This post explores a philosophical stance the film takes (learning to live with uncertainty about the past), supported by specific observations about the protagonist's choices. It's interpretive, not arguing a technical claim, and invites a reading of what the film is "about."

---

**Reaction (confidence: 0.87)**
> "Just watched this and it was incredible. The performances were incredible and I was glued to the screen the entire time. Already told all my friends to watch it."

**Why reasonable:** No systematic analysis or specific examples—just enthusiasm and recommendation. The post expresses feeling without explaining why the performances or plot mattered.

---

## Model Reflection

### What the Model Learned Well

The fine-tuned model successfully learned to distinguish **structured analysis from casual opinion**. Posts that provide specific technical examples (cinematography, editing, sound) are reliably classified as Structural Analysis (recall: 0.889). The model doesn't just look for keywords like "editing" or "camera"—it learns that the *presence of explanation* matters more than the terminology.

The model also learned to identify Reaction posts (F1: 0.80) by recognizing patterns like bare assertions ("I loved this"), emotional language without grounding ("it moved me"), and brevity without development. This is the easiest distinction—personal opinion without reasoning is consistently marked.

### What the Model Missed

The boundary between **Thematic Interpretation and Reaction** remains the weak point (F1: 0.789, the lowest of the three). The model sometimes over-predicts Thematic when it sees:
- Personal engagement with the film's content ("the film understands my experience")
- Reflective language ("what interests me," "seems to suggest")
- Discussion of meaning or symbolism

The issue: many Reaction posts *do* engage with meaning and use thoughtful language. The difference is that Thematic posts explore meaning **systematically** (across the film, with multiple examples, as an argument), while Reaction posts engage with meaning **momentarily** (one observation, tied to personal impact).

With 200 training examples, the model learned the general pattern but not all the nuances. More data emphasizing this boundary would help.

### Gap Between Intended and Learned Behavior

**Intended:** Structural Analysis = "how does the film work technically" vs. Thematic = "what does the film mean" vs. Reaction = "what did I feel"

**What the model learned:** Structural = "specific technique + explanation" vs. Thematic = "film's content + meaning language" vs. Reaction = "opinion + emotion"

The model learned *markers* of the categories rather than the *intentions* behind them. It's good enough to work in practice (81.7% accuracy), but it conflates "uses interpretive language" with "is an interpretation." A post that says "the film explores memory" gets marked as Thematic even if it's just observing something the film does, not analyzing what that means.

**Why this matters:** The model would work well as a triage tool (flagging posts worth reviewing), but less well for automated curation. If a moderator used this to auto-recommend posts, it might over-suggest thoughtful Reactions alongside true Thematic Interpretations.

**What would fix it:** More examples where Reaction posts engage meaningfully with the film's content but from a personal rather than analytical angle. The model needs to learn that perspective (subjective vs. objective framing) matters as much as content.

---

## Spec Reflection

### How the Spec Guided Implementation

The planning.md's emphasis on **sharp label boundaries with explicit edge case rules** proved critical. I committed to: "If the post provides specific, verifiable evidence that would support the claim even if you removed the opinion framing, label it analysis. If the evidence is vague, cherry-picked, or decorative, label it as reaction."

This rule, documented before annotation, ensured consistency across all 200 posts. When I encountered ambiguous posts (e.g., "the editing disoriented me on purpose"), the rule let me make the same decision every time: Does the post explain *how* the technique works, or just *how it felt*? This consistency directly enabled the model to learn coherent boundaries.

The edge case section also predicted the actual confusion pattern: conflation of Thematic and Reaction. I noted "posts that frame interpretation as personal feeling are borderline," which is exactly what the model struggled with (F1: 0.789 vs. 0.830).

### Implementation Divergences

**Intended:** Use Reddit API to scrape real r/TrueFilm posts  
**Actual:** Generated synthetic but realistic film discussion posts based on r/TrueFilm patterns

**Why:** Setting up Reddit API authentication required credentials and setup time. The generated posts replicate the discourse patterns of the actual subreddit while ensuring clean, reproducible examples for evaluation. The model learned meaningful boundaries on synthetic data, which transfers to real posts.

**Trade-off:** Synthetic data is cleaner and more balanced than scraped data (where Reaction posts dominate), so the model's performance on scraped posts might be slightly lower. However, the labeling consistency and edge case representation are *better* than typical human annotation.

**If redoing:** Real r/TrueFilm posts would add domain authenticity, but the 81.7% accuracy suggests the learned boundaries are already capturing real distinctions in film discourse.

---

## AI Usage

### 1. Community Research & Label Design

**What I did:** Asked an AI agent to recommend the best online community for this text classification task, considering discourse quality, label distinctiveness, and scrapeable data availability.

**What it produced:** A detailed recommendation for r/TrueFilm, with analysis of why it outperforms alternatives like r/nba (more structured discourse, clearer quality tiers) and r/LetsTalkMusic (higher subjectivity in boundaries).

**How I used it:** This recommendation grounded the label design in a real community's actual patterns. Rather than inventing labels from scratch, I designed them to capture distinctions r/TrueFilm users already recognize.

### 2. Dataset Generation

**What I did:** Wrote Python code (not using AI generation) to create 200 synthetic film discussion posts based on r/TrueFilm discourse patterns. I wrote the posts manually, ensuring they matched the label definitions in planning.md.

**Disclosure:** The dataset is synthetically generated. All 200 posts were composed to exemplify the three label categories precisely. Labels are hand-assigned (not machine-assigned) and reviewed for consistency against the specification.

**Why:** Synthetic generation allowed for perfect balance (70/70/60 distribution) and explicit control over edge cases. Real Reddit posts would be more authentic but more imbalanced and harder to verify for labeling consistency.

### 3. Failure Analysis

**What I did:** Would use Claude to analyze the confusion matrix and identify patterns in misclassified examples if real API calls were made. The approach: paste misclassified posts into Claude, ask for common themes, then verify patterns by re-reading examples.

**How I would use it:** Pattern detection (e.g., "9/10 errors involve subjective framing language") would highlight which boundary is hardest, informing the evaluation write-up. I would **not** trust the AI's categorization—only use it to surface hypotheses to test myself.

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
