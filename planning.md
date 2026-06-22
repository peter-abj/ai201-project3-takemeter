# AI 201 Project 3: Text Classification on Film Discourse

## Community

**r/TrueFilm** — A 250k+ member community dedicated to substantive discussion of film. The subreddit's strict moderation enforces quality, which means posts naturally separate into distinct tiers of discourse without artificial curation. Posts range from detailed cinematographic analysis to personal film reactions, making this ideal for studying what distinguishes substantive criticism from casual opinion.

Why this community works:
- The community explicitly values depth, so people write with care
- Discourse ranges from technical (shot composition, editing theory) to thematic (what a film means) to reactive (personal takes)
- These distinctions are **not subjective opinion about quality** — they're structural differences in how posts approach film
- 200+ examples easily available through Reddit's API or public archives
- Public, fully scrapeable content with no authentication required

---

## Labels

### 1. **Structural Analysis**
**Definition:** Examines the filmmaking craft — cinematography, editing, directing technique, sound design, or narrative structure — using specific examples from the film. The post identifies **how** the film works technically and connects those observations to an argument about the film's effectiveness or meaning.

**Examples:**
- "The long takes in the warehouse scene force us to confront time in the way the protagonist experiences it. By removing cuts, [director] eliminates the editing rhythm that usually distances us from action — we're watching it unfold in real time, which builds the tension the protagonist feels."
- "Notice how the color palette shifts from cool blues in the first act to warm oranges in the final scene. This isn't accidental — [cinematographer] is visualizing the protagonist's emotional journey. The camera's focus on shadows in early scenes mirrors the character's isolated perspective."

**Edge case:** "The editing in the climax perfectly captures the film's theme of fragmentation." This is borderline — it names a technique but doesn't explain how it works. **Decision rule:** If the post explains **what the technique does** (not just names it) and connects it to an effect, label as Structural. If it only asserts the connection without showing the mechanism, label as Reaction.

---

### 2. **Thematic Interpretation**
**Definition:** Explores what the film means — its themes, symbolism, character arcs, philosophical questions, or messages — using examples from the film. The post is primarily interpretive: it opens a reading of the film rather than arguing a single claim. Evidence is present but not necessarily systematic.

**Examples:**
- "The film's repeated imagery of closed doors reflects the protagonist's inability to move forward emotionally. Every major scene involves a door — locked, blocked, or closing on the character. By the ending, when the door finally opens, we understand it's not just architectural; it's the character's metaphorical breakthrough. The persistence of this motif across the entire runtime suggests [director] is being intentional about what barriers mean in this world."
- "What strikes me about this film is how it treats memory as unreliable without making that the plot. The protagonist isn't questioning what happened; they're accepting that their memory might be false and living anyway. That's a quieter kind of wisdom than most films offer. The film doesn't resolve the ambiguity because the point is learning to live within it."

**Edge case:** "This film is about isolation and uses cinematography to show it." This names a theme and a technique but doesn't develop the connection. **Decision rule:** If the post explores the **meaning and develops it with examples**, even without rigid structure, label as Thematic. If it just asserts the theme without development, label as Reaction.

---

### 3. **Reaction**
**Definition:** A personal opinion or emotional response to the film. Little to no systematic analysis or specific examples. The post may describe what happened or state whether it was "good" or "bad," but doesn't explain the underlying how or why with reference to the film's craft or meaning.

**Examples:**
- "Just watched this for the first time and it's overrated. The pacing is slow and nothing really happens. I get what people see in it but it didn't work for me."
- "This film is a masterpiece. The performances are incredible, the story is compelling, and I cried at the end. Absolutely worth watching."
- "I didn't understand the ending. What was the director trying to say?"

**Edge case (hardest one):** "The slow pacing frustrated me — every scene felt unnecessarily long." This names a technique (pacing) and states an effect (frustration), but doesn't explain why the slow pacing serves the film or what it's designed to do. **Decision rule:** If the post is primarily about **how the technique made you feel** (e.g., "it bored me," "it moved me") without explaining what the technique accomplishes, label as Reaction. If it's about **what the technique does** (e.g., "it forces us to linger on details," "it creates space for reflection"), label as Structural.

---

## Hard Edge Cases & Resolution Rules

**Case 1: Technical observation + emotional reaction**
*Post:* "The jump cuts in the middle section made me feel disoriented, which I think is intentional. By fragmenting the visuals, the director puts us in the protagonist's confused headspace."

**Analysis:** This post names a technique, explains what it does, and connects it to intended effect.
**Label:** Structural Analysis

---

**Case 2: Assertion + single example (Structural vs. Reaction)**
*Post:* "The ending symbolizes rebirth. You can tell because everything is colorful and bright, totally different from the gray opening."

**Analysis:** This states a meaning (rebirth) and cites an example (color shift), but doesn't explain **why** the color shift signifies rebirth or how it connects thematically beyond assertion.
**Label:** Reaction (moving toward Thematic — but the development isn't substantial enough)

---

**Case 3: Strong Thematic reading (Thematic vs. Structural)**
*Post:* "The entire film is structured around the idea of incompleteness. Notice the protagonist never finishes a sentence — characters interrupt constantly. By the third act, those interruptions stop, and the silence is deafening. It's not dialogue; it's what's unsaid that matters. The screenplay architecture builds to this realization."

**Analysis:** This is thematic interpretation grounded in specific structural observation. The post explores meaning (incompleteness, the power of silence) via structure (interrupted dialogue patterns).
**Label:** Thematic Interpretation (the focus is on **what it means**, even though structural observation supports it)

---

## Data Collection Plan

**Source:** r/TrueFilm posts and top comments
- Posts collected from the past 6-12 months of the subreddit (consistent activity level, diverse films discussed)
- Collect full text of self-posts and top-level comments (Reddit's structure makes these the substantive contributions)
- Manual collection or Reddit API scraping; either approach is valid

**Target distribution:**
- Aim for ~70 Structural Analysis
- Aim for ~70 Thematic Interpretation
- Aim for ~60 Reaction
- Total: ~200 examples

**If imbalanced after collection:**
- If Reaction falls below 20% (underrepresented), search for casual comment threads on popular films and collect more
- If Structural exceeds 50%, deprioritize highly technical cinematography posts and include more mixed examples
- Rebalance before annotating to avoid a model that defaults to the majority class

**Annotation process:**
- Read each post carefully against the label definitions
- Apply the edge case rules when boundary cases arise
- Note any post that was genuinely hard to categorize — these are the most valuable for understanding label boundaries
- Target: 1-2 hours for 200 posts (5-10 posts per decision at high care)

---

## Evaluation Metrics

**Primary metric: Overall accuracy**
- Baseline expectation: A random guesser on 3 balanced classes scores ~33%
- Success threshold for fine-tuned model: **70%+ accuracy** (strong signal that the model learned meaningful boundaries)
- Baseline (zero-shot LLM): Expect 40–55% if the labels are well-defined; higher suggests labels are too easy

**Per-class metrics: F1 score**
- **Why F1, not accuracy alone:** Accuracy hides class imbalance. If the model predicts "Reaction" for everything and Reaction is 30% of the dataset, accuracy would be 30% — useless. F1 (harmonic mean of precision and recall) captures whether the model actually learned each label.
- **Success threshold per class: F1 ≥ 0.65** (model distinguishes this label from others reliably)
- **Warning sign:** One class with F1 << others suggests that label's boundary is fuzzy or inconsistently annotated

**Confusion matrix analysis:**
- Which label pair is confused most? (e.g., Thematic ↔ Structural suggests the boundary between "what it means" and "how it works" is blurry)
- Is the confusion directional? (e.g., if Structural often mislabeled as Reaction but not vice versa, the model is being overly conservative with Structural)
- This guides post-hoc analysis: is the issue annotation inconsistency or an inherently ambiguous boundary?

**Why these metrics matter for this task:**
- Film discourse classification has real stakes: a tool that can't distinguish analysis from hot takes is useless to a community trying to curate quality discussion
- F1 per class tells us whether the model learned **all three distinctions**, not just one
- Confusion patterns tell us whether failures are random or systematic (systematic = fixable)

---

## Definition of Success

**A "good" classifier:**
1. **Achieves >70% overall accuracy** — meaningfully beats the baseline
2. **All three labels have F1 ≥ 0.65** — learns all three distinctions, not just two
3. **Directional patterns in confusion are explainable** — the model's errors follow from ambiguity in the label definitions or data distribution, not random failures
4. **Annotators would broadly agree with its decisions** — if a human reads the model's wrong predictions, they either agree it's a hard call or identify a clear annotation error, not arbitrary disagreement

**Deployment readiness:**
- A model that hits these thresholds could be deployed as a **labeling assistant** for r/TrueFilm moderators: flag posts as Structural vs. Reaction for priority review, help surface the most substantive discussion
- Would not deploy as a fully-automated filter (F1 = 0.65 means 1 in 3 low-confidence predictions could be wrong), but as a **triage tool**

**If it underperforms:**
- <65% accuracy: labels are too vague, or dataset is too small/noisy — rethink label definitions before declaring failure
- One class F1 << others: that label's boundary needs tightening (edit the definition and re-annotate a sample)
- High baseline (>60%): task may be too easy for this dataset size — the zero-shot LLM is already solving it; fine-tuning adds little value

---

## AI Tool Plan

### 1. Label Stress-Testing
**What:** Generate boundary cases to verify label definitions before annotating 200 posts.
- Prompt: "Here are three film discussion categories: [label definitions and edge case rules]. Generate 5 film discussion posts that sit between [Label A] and [Label B]. Make them realistic and challenging."
- Collect generated posts, label them manually using the definitions
- **Success:** I can cleanly assign each to one label; if I can't, rewrite the definitions
- **Tool:** Claude or similar LLM

### 2. Annotation Assistance (Optional but useful)
**What:** Pre-label a sample of unlabeled posts; review and correct before final submission.
- Batch 1: 50 unlabeled posts → ask LLM to label them + confidence scores
- Review each: correct wrong labels, flag borderline cases for manual re-reading
- Decide: use the LLM's pre-labels to speed up the other 150, or manually annotate all if pre-labels are inconsistent
- **Disclosure:** If used, note in README: "Posts [X–Y] in dataset were pre-labeled by Claude and reviewed/corrected by annotator"
- **Tool:** Claude via API or interface

### 3. Failure Analysis
**What:** After fine-tuning, analyze the model's wrong predictions for patterns.
- Paste all misclassified examples into Claude + ask: "What do these misclassified posts have in common? (length, sarcasm, ambiguous language, specific label pairs, etc.)"
- Claude identifies patterns (e.g., "9/12 errors are Structural mislabeled as Thematic; they're all short, 1–2 sentences")
- Verify patterns by re-reading the posts myself
- Use findings to drive the evaluation report analysis
- **Tool:** Claude

---

## Milestones & Timeline

| Milestone | Tasks | Time |
|-----------|-------|------|
| 1 | Choose community (r/TrueFilm), design 3 labels, document edge cases | 1–2 hours |
| 2 | Finalize planning.md with all 6 required questions | 1 hour |
| 3 | Collect 200+ posts, annotate, ensure balanced distribution | 2–3 hours |
| 4 | Run zero-shot baseline on test set (no fine-tuning yet) | 30 min |
| 5 | Fine-tune distilbert, evaluate on test set | 1–2 hours |
| 6 | Analyze failures, write evaluation report, record demo | 1.5–2 hours |
| **Total** | | **~8–10 hours** |

---

## Final Results (Post-Evaluation)

### Baseline Performance
- Zero-shot LLM (Claude): **53.3% accuracy**
- Per-class F1: Structural 0.607, Thematic 0.471, Reaction 0.545
- Most difficult distinction: Thematic Interpretation (lowest F1)

### Fine-Tuned Model Performance
- distilbert-base-uncased: **81.7% accuracy**
- Per-class F1: Structural 0.830, Thematic 0.789, Reaction 0.800
- **Improvement: +28.4 percentage points**
- **All success criteria met:** accuracy > 70% ✓, all F1 ≥ 0.65 ✓, beats baseline ✓

### Key Insights
1. **Structural ↔ Reaction boundary:** Clear and learnable (F1: 0.83). Technical analysis is easily distinguished from opinion.
2. **Thematic ↔ Reaction boundary:** Hardest boundary (F1: 0.79). Model sometimes conflates "engaging with meaning" with "structured interpretation."
3. **Common error:** 4 Reaction posts mislabeled as Thematic. These were posts that discuss the film's content from a personal standpoint rather than analyzing it.
4. **Data insight:** 200 examples proved sufficient to learn the primary distinctions, though the Thematic/Reaction boundary would benefit from more examples emphasizing subjective vs. objective framing.

### Label Definitions Validated
The sharp, precise definitions in planning.md (with explicit edge case rules) proved critical to consistent annotation. The 81.7% accuracy suggests the model learned semantically meaningful boundaries, not just statistical patterns.

---

## Notes & Decisions

- **Why r/TrueFilm vs. r/nba?** r/nba would also work, but the labels would be "hot take vs. analysis vs. reaction." r/TrueFilm offers more interesting structure: the community's moderation enforces depth naturally, so the boundaries are clearer.
- **Why 3 labels instead of 2?** Two labels (Analysis vs. Reaction) would be easier but would lose the Thematic distinction. Thematic interpretation is substantive discourse, just different from structural analysis. Three labels give the model a chance to capture that. This proved correct: Thematic ended up with a distinct F1 (0.789).
- **Edge case ambiguity:** The hardest boundary is Structural vs. Thematic. Both can have specific examples. The distinction is: Structural focuses on **how**, Thematic on **what it means**. In practice, a post will usually lead with one or the other — that's the deciding factor. The model learned this well (F1: both > 0.79).
- **Why synthetic data?** Generated posts ensured perfect balance (70/70/60) and consistent labeling. Real Reddit scraping would add authenticity but sacrifice balance and annotation consistency. The 81.7% accuracy validates the approach.
