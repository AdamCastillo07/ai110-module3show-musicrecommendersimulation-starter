# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

My recommender is content based: instead of learning from other users' behavior (like implicit feedback such as skips or repeats), it compares each song's own attributes directly against one user's declared taste profile and ranks songs by how closely they match.

Song features used:
- `genre` — categorical (e.g. pop, lofi, rock, jazz)
- `mood` — categorical (e.g. happy, chill, intense, relaxed)
- `energy` — continuous, 0 to 1
- `acousticness` — continuous, 0 to 1

I left `tempo_bpm`, `valence`, and `danceability` out of the scoring rule for now since the `UserProfile` doesn't capture user preferences for them, and with only 10 songs in the catalog, extra features add complexity without much added accuracy.

**What `UserProfile` stores:**
- `favorite_genre` and `favorite_mood` — the user's preferred categories
- `target_energy` — the energy level (0 to 1) the user wants, rather than just "high" or "low"
- `likes_acoustic` — a boolean for whether the user prefers acoustic-leaning songs

**How the score is computed (`score_song`):**
Each song gets a score built from four parts:
1. **Genre match**: a fixed bonus if `song.genre == favorite_genre`, else 0
2. **Mood match**: a fixed bonus if `song.mood == favorite_mood`, else 0
3. **Energy closeness**: `1 - abs(song.energy - target_energy)`, so a song scores higher the closer its energy is to the target, rather than just rewarding high energy
4. **Acousticness match**: a smaller bonus if `(song.acousticness > 0.5) == likes_acoustic`

These four parts are weighted and summed into one score, and `explain_recommendation` reports which of the four actually matched, so every recommendation is traceable back to a specific reason.

**Algorithm Recipe (finalized weights):**

| Component | Type | Weight | Contribution |
|---|---|---|---|
| Genre match | binary | 2.0 | `2.0` if `song.genre == favorite_genre` else `0` |
| Mood match | binary | 1.5 | `1.5` if `song.mood == favorite_mood` else `0` |
| Energy closeness | continuous | 1.5 | `1.5 * (1 - abs(song.energy - target_energy))` |
| Acousticness match | binary | 0.5 | `0.5` if `(song.acousticness > 0.5) == likes_acoustic` else `0` |

Max possible score: **5.5** (2.0 + 1.5 + 1.5 + 0.5)

Genre outweighs mood because I'm treating genre as the more stable, long-term taste signal and mood as a secondary refinement on top of it. Energy closeness is weighted the same as mood since, being continuous, it almost always contributes *some* points, so it shouldn't be allowed to outweigh an exact mood match just for being "close enough." Acousticness is the smallest weight because it's meant to act as a tie-breaker, not a core signal.

**Potential biases in this recipe:**
- With mostly one song per genre and mood in the current catalog, a user whose `favorite_genre` or `favorite_mood` doesn't exist in the catalog gets no bonus from those two components at all, so the system quietly falls back to ranking by energy/acousticness only — it never signals "we don't have your genre."
- Weighting genre above mood means two users with the same mood preference but different genre preferences can get very different top recommendations even when their actual listening context (energy, acousticness) is identical — the system favors genre loyalty over situational fit.
- Fixed, hand-picked weights (2.0 / 1.5 / 1.5 / 0.5) encode my own judgment about what should matter, not anything learned from real listener behavior, so they could just as easily reflect my assumptions as they reflect good recommendations.

**How songs are chosen (`recommend_songs` / `Recommender.recommend`):**
Scoring and ranking are kept separate: `score_song` computes one song's match quality for one user, with no knowledge of the rest of the catalog. Ranking then calls `score_song` on every song, sorts the results by score descending, and returns the top `k`. Without this second step there'd be scores but no ordered recommendation list.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the starter profile (`genre=pop, mood=happy, energy=0.8`):

```
Loaded songs: 18

Top Recommendations (genre=pop, mood=happy, energy=0.8)
=======================================================

1. Sunrise City - Neon Echo  (Score: 4.97)
     - genre match +2.0
     - mood match +1.5
     - energy closeness +1.47

2. Gym Hero - Max Pulse  (Score: 3.30)
     - genre match +2.0
     - energy closeness +1.30

3. Rooftop Lights - Indigo Parade  (Score: 2.94)
     - mood match +1.5
     - energy closeness +1.44

4. Block Party Anthem - Trap Lantern  (Score: 1.50)
     - energy closeness +1.50

5. Night Drive Loop - Neon Echo  (Score: 1.42)
     - energy closeness +1.42
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



