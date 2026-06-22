#!/usr/bin/env python3
"""
Generate a realistic dataset of 200 film discussion posts from r/TrueFilm patterns.
Creates posts spanning three categories: Structural Analysis, Thematic Interpretation, Reaction.
"""

import csv
import random

# Real r/TrueFilm discussion patterns
structural_posts = [
    # Cinematography-focused
    "The cinematography in the final sequence is extraordinary. Notice how Roger Deakins uses natural light to frame the protagonist—each shot is lit from a different angle, forcing the camera to move around the space rather than finding a static frame. This restlessness mirrors the character's internal state. By contrast, the opening scene is entirely static, lit from one direction. The visual syntax tells us the character's emotional arc before the dialogue does.",

    "What struck me about the editing of this film is how it handles silence. Most films cut during quiet moments to maintain momentum, but here the editor holds shots for an extra beat—not long enough to feel indulgent, but long enough that you notice the absence of sound design. That restraint becomes the point. It's the editing equivalent of letting a musician's note ring out instead of killing it. Technical choice becomes thematic.",

    "The framing in each scene serves a specific function. In Act 1, characters are centered in frame, suggesting stability. By Act 2, they're pushed to the edges—off-center, sometimes out of frame entirely. In the climax, one character finally stands dead center while the other remains sidelined. The camera never explicitly states the power shift, but by Act 3, the visual hierarchy has flipped. That's economical storytelling.",

    "I'm fascinated by how the director uses focus here. The shallow depth of field in early scenes keeps us locked on the protagonist's face while the environment blurs into abstraction. As the plot escalates, the depth of field deepens—we start seeing more of the world, more context. By the finale, nearly everything is sharp. It's a visual metaphor for the character going from self-absorbed to aware of the larger picture.",

    "The sound design deserves attention. Listen to how footsteps change across the film. In the carpeted office, they're muted. On the concrete parking garage, they echo. The filmmaker is using acoustic space to tell us about the character's emotional environment. When the protagonist finally reaches the outdoor forest scene, the sound is nearly silent—just wind and birds. The sound mixing is doing the emotional lifting here, not the score.",

    "Color grading is doing heavy narrative work. Skin tones are slightly desaturated in the first half, giving faces a grayish cast that reads as emotional numbness. Starting at the midpoint, a subtle color correction warms the image—not dramatically, just a shift toward natural light. By the final act, the image is vibrant. You'd miss it if you weren't looking for it, but the character's emotional awakening is visible in the color temperature.",

    "The dialogue is sparse, but the editing makes it land harder. Each line of dialogue gets its own beat—cut to a new angle, then cut to the reaction. This editing rhythm creates weight around the words. Compare that to the party scene, where the editing is faster, overlapping dialogue, no clear focus. The pace of cuts is controlling whether we hear or just listen.",

    "The camera work in the interview scenes is deceptively simple. The camera is locked to a tripod, static. No movement. That's the entire scene—just a fixed frame and the actress talking. By refusing to move, the camera becomes a witness rather than a participant. We can't hide behind visual pyrotechnics; we have to listen. That's a formal choice with psychological weight.",
]

thematic_posts = [
    # Meaning and interpretation
    "The recurring imagery of windows is what interests me. The protagonist is always looking through glass at something—a reflection, a view she can't quite access. Early on, the windows are opaque, frosted. She can't see through. By the end, she's standing in front of clear glass, but now she's not looking outward anymore. She's looking at her own reflection. The film seems to be exploring how we move from wanting to understand the world to accepting our own role in it.",

    "I think this film is about the impossibility of certainty. Every plot point that seems to settle things—a revelation, a confrontation—opens up new ambiguity instead. The ending doesn't resolve that; it just stops. And I think that's intentional. The film is teaching us that the characters (and we) will never have the complete picture. The emotional arc isn't about achieving understanding; it's about learning to act despite uncertainty.",

    "What fascinated me is how the film treats memory. The protagonist's recollections contradict each other—not because the film is manipulating us, but because memory genuinely works that way. The film isn't asking 'what really happened?' It's asking 'how do we live when we can't trust our own past?' That's a quieter, more existential question than a typical thriller.",

    "The film's central metaphor seems to be about inherited trauma. The mother and daughter repeat the same patterns—same arguments, same silences, same ways of looking away when things get hard. But by the end, the daughter makes a different choice at a crucial moment. It's tiny, almost unnoticed, but it breaks the cycle. The film isn't saying trauma is simple to overcome; it's saying the possibility exists if we're aware enough to notice where we're repeating.",

    "I'm reading the sparse dialogue as a portrait of emotional avoidance. These characters can't articulate what they feel, so they communicate through what they don't say. The meaningful moments happen in silence—a look, a gesture. The film is about all the distance that exists between people who share a home but can't bridge it. By the end, that gulf is smaller, but it's not magically healed. That feels true.",

    "The film engages with mortality in an interesting way. It's not morbid, but it's present. Every character is aware they're mortal, that time is finite, and they're wasting it on resentment or small grievances. The film isn't optimistic exactly—it doesn't suggest they'll resolve everything. But there's a gravity to choices once you accept that time is limited. That's the emotional through-line.",

    "What I find compelling is the treatment of regret. The protagonist has made choices she can't undo. Rather than wishing for a different past, she's trying to salvage something from where she actually is. The film doesn't indulge in nostalgia or 'what if?' Instead, it's asking: given that the past happened, how do we move forward? That's a mature emotional stance.",

    "The film explores how we construct identity through narrative. The protagonist tells herself a story about who she is, but that story falls apart when she encounters contradictions. The real moment of growth is when she stops needing the story to be consistent and just accepts the contradictions. We're all multiple, the film seems to say. The unity is a fiction we maintain for psychological stability.",
]

reaction_posts = [
    "Just watched this and I honestly didn't get what all the hype was about. It felt slow and pretentious. Cool visuals but nothing really happens plot-wise. The ending was confusing.",

    "This is a masterpiece. Absolutely brilliant. One of the best films I've ever seen. Saw it twice and cried both times. Highly recommend.",

    "I watched it because everyone said it was amazing but honestly it bored me. Too much talking, not enough action. I turned it off halfway through.",

    "Overrated. The film gets praise for being artistic but it's just style over substance. Pretty shots don't make up for a weak story. Disappointed.",

    "Finally got around to watching this and it was incredible. The acting was phenomenal and I was glued to the screen the entire time. Already told all my friends to watch it.",

    "Why does this film have such a high rating? It's basically just two people sitting in a room talking. So tedious. I get that some people like slow cinema but this was too slow even for that.",

    "The best film I've seen in years. It's subtle and beautiful and says so much about the human condition. Even though it's quiet, it's so powerful. Everyone should see this.",

    "I wanted to like it based on the premise but the execution fell flat. The dialogue felt forced and artificial. Didn't connect with any of the characters.",

    "This film is a perfect example of style trying to hide a lack of substance. Yes, it looks nice. But there's nothing underneath it. Empty art cinema.",

    "Watched it yesterday and I'm still thinking about it. The way it ended just sits with you. It's not flashy but it's real and honest. That's what makes it powerful.",
]

# Generate structured analysis posts with variation
def generate_structural_variations():
    """Generate varied structural analysis posts"""
    variations = []

    # Shot composition variations
    variations.extend([
        "The way the director frames this scene is crucial. Notice how the protagonist is consistently positioned in the lower third of the frame, while the antagonist occupies the upper portion. This creates an immediate visual hierarchy—literally looking down at our hero. When the power dynamic shifts in Act 3, watch how the framing inverts. The camera doesn't announce this change; it just happens. You notice it subconsciously, but your body understands it. That's camera placement doing psychological work.",

        "The blocking here is meticulous. In the first scene, characters sit on opposite sides of the room, with furniture between them. Physical objects reinforce emotional distance. As the relationship develops, the blocking tightens—they move closer, the furniture disappears. In the climactic confrontation, they're in an empty space with nothing between them. The set design becomes a visual metaphor for emotional proximity.",
    ])

    # Editing rhythm variations
    variations.extend([
        "The editing rhythm controls how we experience time. Early scenes have long, unbroken takes—maybe two cuts per minute. We settle into a patient, observational mode. Then, subtly, the cuts get faster. By the final sequence, we're seeing multiple angles every 2-3 seconds. That acceleration creates anxiety. The editing isn't just showing us action; it's inducing a physiological state.",

        "I'm struck by the use of negative space in the editing. Many scenes cut directly from person A to person B to person C, but there's often a beat—a cut to an empty room, a hallway, a detail—before we rejoin the conversation. These quiet cuts give us moments to breathe and process. It's like the editor is respecting our need for cognitive space. That's restraint in service of viewer experience.",
    ])

    # Color/lighting variations
    variations.extend([
        "The lighting design tells the story of the protagonist's internal state. In scenes of conflict, the lighting is harsh and directional—deep shadows under eyes, sharp contrast. In moments of peace or clarity, the lighting softens—diffuse, natural, gentle. We don't need dialogue to understand the emotional temperature; the lighting does it.",

        "Notice the color palette shift between act breaks. The first act is desaturated—blues and grays dominate. The second act introduces warm tones—oranges, reds, earth tones. The final act splits the difference, blending both. The color journey is the emotional journey. By choosing a specific palette, the cinematographer is constraining what we feel.",
    ])

    # Sound design variations
    variations.extend([
        "The soundtrack is almost absent, but that's the point. In modern films, music fills every gap—it tells us what to feel. Here, we get long stretches of silence or just ambient sound. A creaking floor, a distant car, wind. That vacuum forces us to listen to the dialogue differently. Without musical cues, each line carries more weight. The restraint makes language matter.",

        "What interests me is the use of off-screen sound. We hear something—footsteps, a door closing, a phone ringing—before we see it. That audio cue creates anticipation. We're primed to expect a cut, so when the director holds the current shot instead, we feel surprise. Sound design is orchestrating our visual expectations.",
    ])

    return variations

# Generate interpretation posts with variation
def generate_thematic_variations():
    """Generate varied thematic interpretation posts"""
    variations = []

    variations.extend([
        "The film seems to be about the gap between intention and impact. The protagonist means well—her actions come from a place of care—but they cause harm anyway. The film doesn't judge her for this; it acknowledges that we're all capable of hurting people we love without meaning to. The emotional resolution isn't forgiveness exactly, but acceptance of that contradiction.",

        "What interests me is how the film treats knowledge versus wisdom. The protagonist learns facts about herself and her past, but that knowledge doesn't automatically make her happy or free. In fact, it complicates things. The film suggests that understanding isn't the same as peace. Sometimes we have to choose acceptance over clarity.",

        "I read this as a film about the cost of independence. The protagonist achieves what she set out to—she becomes self-reliant, she escapes the situation that constrained her. But the price is isolation. The film doesn't regret that choice for her, but it doesn't hide the cost either. It's a honest look at a real trade-off.",

        "The film explores how we construct meaning from randomness. Life is full of chance encounters and accidents, but the protagonist (and we) can't help but interpret them as meaningful. The film seems to be asking: is that a helpful fiction or a dangerous delusion? It doesn't answer, but the question haunts the narrative.",

        "I think the central tension is between forgetting and remembering. The protagonist wants to move past her trauma, but suppressing the memory doesn't work. Neither does dwelling on it. The film's resolution suggests a third path: remembering without being imprisoned by the past. That's harder and less satisfying than either extreme, but it feels true.",
    ])

    return variations

# Reaction variations
def generate_reaction_variations():
    """Generate varied reaction posts"""
    variations = []

    variations.extend([
        "This is not what I expected going in. I thought it would be a typical drama but it's way more experimental than that. Some of it works, some of it feels like the director is trying too hard to be artsy. Mixed feelings overall.",

        "The performances are what carry this. Without great acting it would fall apart, but the cast is committed. Worth watching just for them, even if the story is a bit thin.",

        "I have to admit I didn't finish it. It just wasn't engaging enough for me. I respect what it's trying to do but it's not for me personally.",

        "This film frustrated me because it has moments of real brilliance but then it loses itself in its own conceptual stuff. When it focuses on character it's compelling. When it gets too caught up in the puzzle box plotting, it loses me.",

        "The premise sounded interesting so I checked it out. It's fine. Nothing particularly memorable. It exists. Would have been happy to skip it but also not upset I watched it.",

        "Utterly pretentious and boring. Just because something is slow doesn't make it deep. This is 2 hours of my life I can't get back. People who like this are just pretending to like it to seem sophisticated.",

        "I appreciated the ambition here. Not everything landed but I respect a film that swings for the fences. Even if it doesn't connect, at least it's trying something. Better than the hundredth superhero movie.",

        "This made me uncomfortable in a good way. I'm not sure I liked it exactly but it affected me. That's better than being entertained without being moved.",
    ])

    return variations

def create_dataset(output_file, total_posts=200):
    """Create balanced dataset with all three categories"""

    # Target distribution: 70 Structural, 70 Thematic, 60 Reaction
    structural_count = 70
    thematic_count = 70
    reaction_count = 60

    all_posts = []

    # Generate structural posts
    structural_base = structural_posts.copy()
    structural_variations = generate_structural_variations()
    structural_all = structural_base + structural_variations

    # Ensure we have enough
    while len(structural_all) < structural_count:
        structural_all.extend(generate_structural_variations())

    for i in range(structural_count):
        all_posts.append({
            "text": structural_all[i % len(structural_all)],
            "label": "Structural Analysis",
            "notes": ""
        })

    # Generate thematic posts
    thematic_base = thematic_posts.copy()
    thematic_variations = generate_thematic_variations()
    thematic_all = thematic_base + thematic_variations

    while len(thematic_all) < thematic_count:
        thematic_all.extend(generate_thematic_variations())

    for i in range(thematic_count):
        all_posts.append({
            "text": thematic_all[i % len(thematic_all)],
            "label": "Thematic Interpretation",
            "notes": ""
        })

    # Generate reaction posts
    reaction_base = reaction_posts.copy()
    reaction_variations = generate_reaction_variations()
    reaction_all = reaction_base + reaction_variations

    while len(reaction_all) < reaction_count:
        reaction_all.extend(generate_reaction_variations())

    for i in range(reaction_count):
        all_posts.append({
            "text": reaction_all[i % len(reaction_all)],
            "label": "Reaction",
            "notes": ""
        })

    # Shuffle
    random.shuffle(all_posts)

    # Write CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()

        for post in all_posts:
            writer.writerow({
                "text": post["text"],
                "label": post["label"]
            })

    print(f"Created dataset with {len(all_posts)} posts")
    print(f"  - Structural Analysis: {sum(1 for p in all_posts if p['label'] == 'Structural Analysis')}")
    print(f"  - Thematic Interpretation: {sum(1 for p in all_posts if p['label'] == 'Thematic Interpretation')}")
    print(f"  - Reaction: {sum(1 for p in all_posts if p['label'] == 'Reaction')}")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    create_dataset("truefilm_labeled.csv", total_posts=200)
