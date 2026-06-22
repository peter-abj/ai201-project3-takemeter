# Demo Video Instructions

Record a 3–5 minute video showing the project in action. This is the final piece of Milestone 6.

## What to Show

### 1. Model Classifications (2 min)
Show 3–5 posts being classified by the fine-tuned model with label and confidence visible.

**Script option:**

> "I'll demonstrate the fine-tuned distilbert classifier on some real film discussion posts. For each post, I'll show the predicted label and confidence score."

**Posts to classify:**

**Post 1 (Structural Analysis):**
```
"The long takes in the warehouse scene force us to confront time 
in the way the protagonist experiences it. By removing cuts, 
the director eliminates the editing rhythm that usually distances 
us from action. We're watching it unfold in real time, which 
builds the tension the protagonist feels."
```
Expected: **Structural Analysis** (confidence: ~0.92)

**Post 2 (Thematic Interpretation):**
```
"What interests me about the film is how it treats memory as 
unreliable without making that the plot. The protagonist doesn't 
question what happened; they accept that their memory might be 
false and live anyway. That's a quieter kind of wisdom than most 
films offer."
```
Expected: **Thematic Interpretation** (confidence: ~0.88)

**Post 3 (Reaction):**
```
"Just watched this and it was incredible. The acting was phenomenal 
and I was glued to the screen. Already told all my friends to watch it."
```
Expected: **Reaction** (confidence: ~0.87)

### 2. Correct Prediction Explanation (1 min)
Pick one correct prediction and explain **why the model got it right**.

**Suggested: Use Post 1 (Structural Analysis)**

> "This prediction is correct. The post identifies a specific technical choice—the use of long takes—and explains what it accomplishes. This is exactly what Structural Analysis means: naming a craft element and showing how it affects the viewer. The model learned to recognize this pattern."

### 3. Incorrect Prediction (1 min)
Show one example where the model failed and explain **what went wrong**.

**Use this example (from the README):**
```
True Label: Thematic Interpretation
Predicted: Reaction (confidence: 0.68)

Post: "What interests me about this film is how it leaves you with 
questions rather than answers. By the ending, you're sitting with 
ambiguity instead of certainty. That might frustrate some viewers, 
but it feels honest to me."
```

**Explanation:**
> "This is a case where the model confused Thematic Interpretation with Reaction. The post is exploring how the film handles ambiguity—a thematic concern. But because the post uses subjective framing ('to me,' 'feels honest'), the model weighted personal response more heavily. This is the most common error the model makes: it sometimes can't distinguish between personal interpretation and personal reaction."

### 4. Evaluation Report (1 min)
Walk through the evaluation results.

**Show:**
- Baseline vs fine-tuned comparison (overall accuracy improvement)
- Confusion matrix visualization
- Per-class F1 scores

**Narration option:**
> "The fine-tuned model achieves 81.7% accuracy on the test set, up from 53.3% for the zero-shot baseline. The most improvement came on Thematic Interpretation, which jumped from 0.471 to 0.789 F1. The confusion matrix shows most errors occur between Thematic and Reaction—the hardest boundary for the model to learn."

## How to Create the Demo

### Option 1: Python Script + Manual Recording
Use the `demo.py` script to generate predictions, then screen-record your terminal output:

```bash
python3 demo.py
```

Then record your screen as you:
1. Run the script to show classifications
2. Navigate to the README and confusion_matrix.png
3. Narrate the findings

### Option 2: Jupyter Notebook
Load the predictions in a Jupyter notebook and record it there (better for professional presentation).

### Option 3: Slides + Screen Recording
Create slides with:
- Example posts and predicted labels
- Evaluation metrics table
- Confusion matrix image
- Failure analysis screenshot from README

Record your narration over the slides.

## Technical Tips

- **Screen resolution:** Use 1280x720 or higher
- **Font size:** Make terminal text readable (16pt+)
- **Audio:** Speak clearly, moderate pace (not too fast)
- **Length:** 3–5 minutes (not too short, not too long)
- **File format:** MP4 or webm (standard video formats)
- **Submission:** Save as `demo.mp4` in the repo root

## Checklist

- [ ] Show 3–5 posts with predicted labels and confidence scores
- [ ] Explain one correct prediction with reasoning
- [ ] Explain one incorrect prediction with analysis of why it failed
- [ ] Walk through evaluation report (accuracy, F1, confusion matrix)
- [ ] Audio is clear and narration explains the results
- [ ] Video is 3–5 minutes long
- [ ] Save as `demo.mp4` in repo root

---

**Note:** If you're submitting to a system that requires a shared link, upload the demo.mp4 to Google Drive or another sharing service and include the link in the README.
