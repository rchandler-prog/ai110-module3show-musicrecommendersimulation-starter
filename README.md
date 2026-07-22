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

The recommender compares each song against a user's **taste profile** and gives it a
score. The higher the score, the better the match. It then sorts every song by score
and returns the top `k`.

### Data

- **Each `Song`** carries: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`,
  `danceability`, and `acousticness` (plus `id`, `title`, `artist`).
- **The user profile** is a dictionary of *target* preferences:

  ```python
  user_prefs = {
      "favorite_genre": "lofi",
      "favorite_mood": "chill",
      "target_energy": 0.35,
      "target_valence": 0.60,
      "target_danceability": 0.55,
  }
  ```

### Algorithm Recipe

For each song, the score is the sum of these rules:

| Rule | Points | Reason for the weight |
|------|--------|-----------------------|
| **Genre match** | `+2.0` | Strongest single signal of taste (exact match on `genre`). |
| **Mood match** | `+1.0` | Half of genre — mood is real but coarser (e.g. "chill" spans several genres). |
| **Energy similarity** | `+2.0 × (1 − |song.energy − target_energy|)` | Sharpest *numeric* discriminator (rock ≈ 0.91 vs lofi ≈ 0.35). |
| **Valence similarity** | `+1.0 × (1 − |song.valence − target_valence|)` | Supporting signal; songs cluster in the mid range so it's weighted lower. |
| **Danceability similarity** | `+1.0 × (1 − |song.danceability − target_danceability|)` | Supporting signal, weighted lower for the same reason. |

Every rule that fires also appends a plain-language reason (e.g. "genre match (lofi)"),
which powers the "Because: …" explanation shown with each recommendation.

**Choosing what to recommend:** score all songs, sort highest-to-lowest, return the top
`k`. For the lofi/chill profile above, this correctly ranks the two lofi/chill tracks at
the top and pushes an intense rock track to the bottom.

### Potential Biases I Expect

- **Genre over-prioritization.** Because a genre match is worth `+2.0`, the system may
  over-favor exact-genre songs and overlook a song from a *different* genre that actually
  matches the user's mood and energy really well. A great "chill" jazz track could lose to
  a mediocre lofi track just because the label matches.
- **Mid-range blindness.** The energy/valence/danceability terms reward songs closest to
  the target, so profiles with mid-range targets (≈0.5) can accidentally rank *bland,
  average* songs highly instead of songs the user would find distinctive.
- **Popularity/exposure gap.** The recipe only sees audio features, not how well-known a
  song is — so it can't correct for a catalog that under-represents some genres or artists
  (our sample catalog has only 1 rock and 1 jazz song, but 3 lofi).

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

Produced by running `python -m src.main` with the lofi/chill taste profile:

```
Loaded songs: 10

============================================================
Profile: genre=lofi, mood=chill, energy=0.35
Top recommendations:
============================================================

1. Library Rain — Paper Lanterns  (score: 6.97)
     • genre match (lofi) (+2.0)
     • mood match (chill) (+1.0)
     • energy close to target (+2.00)
     • valence close to target (+1.00)
     • danceability close to target (+0.97)

2. Midnight Coding — LoRoom  (score: 6.75)
     • genre match (lofi) (+2.0)
     • mood match (chill) (+1.0)
     • energy close to target (+1.86)
     • valence close to target (+0.96)
     • danceability close to target (+0.93)

3. Focus Flow — LoRoom  (score: 5.84)
     • genre match (lofi) (+2.0)
     • energy close to target (+1.90)
     • valence close to target (+0.99)
     • danceability close to target (+0.95)

4. Spacewalk Thoughts — Orbit Bloom  (score: 4.67)
     • mood match (chill) (+1.0)
     • energy close to target (+1.86)
     • valence close to target (+0.95)
     • danceability close to target (+0.86)

5. Coffee Shop Stories — Slow Stereo  (score: 3.84)
     • energy close to target (+1.96)
     • valence close to target (+0.89)
     • danceability close to target (+0.99)
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



