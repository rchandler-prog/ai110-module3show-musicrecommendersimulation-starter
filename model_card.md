# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

During my experiments I found that the ranking is dominated by the **energy** feature
combined with a small, imbalanced catalog. Energy is weighted `2.0` *and* it is the
feature that varies most from song to song, so it effectively decides the order; because
pop songs happen to be high-energy and lofi songs low-energy, energy and genre reinforce
each other instead of acting as independent signals. This produces a **filter-bubble
effect**: the "neutral" profile (all targets set to 0.5) returns three lofi tracks at the
top, simply because lofi's mid-low feature values sit closest to the middle — so a user
with no strong taste is always nudged toward lofi. The catalog is also imbalanced (3 of
10 songs are lofi, but only 1 rock and 1 jazz), so lofi and pop fans get several plausible
options while a rock or jazz fan gets one real match followed by unrelated filler. Finally,
**mood is under-weighted** (`1.0`) relative to genre (`2.0`), so a "Happy Pop" user is
served the intense workout track *Gym Hero* — the system honors the genre label over the
actual vibe the user asked for.

---

## 7. Evaluation

### Profiles tested

I stress-tested the recommender with three normal profiles and two adversarial ones
(profiles with preferences that fight each other). All output below comes from
`python -m src.main`.

**High-Energy Pop**
```
1. Sunrise City — Neon Echo  (score: 6.77)   pop / happy
2. Gym Hero — Max Pulse  (score: 5.83)       pop / intense
3. Rooftop Lights — Indigo Parade  (4.65)    indie pop / happy
4. Storm Runner — Voltline  (3.42)           rock / intense
5. Night Drive Loop — Neon Echo  (3.22)      synthwave / moody
```

**Chill Lofi**
```
1. Library Rain — Paper Lanterns  (6.97)     lofi / chill
2. Midnight Coding — LoRoom  (6.75)          lofi / chill
3. Focus Flow — LoRoom  (5.84)               lofi / focused
4. Spacewalk Thoughts — Orbit Bloom  (4.67)  ambient / chill
5. Coffee Shop Stories — Slow Stereo  (3.84) jazz / relaxed
```

**Deep Intense Rock**
```
1. Storm Runner — Voltline  (6.90)           rock / intense
2. Gym Hero — Max Pulse  (4.39)              pop / intense
3. Night Drive Loop — Neon Echo  (3.56)      synthwave / moody
4. Sunrise City — Neon Echo  (3.31)          pop / happy
5. Rooftop Lights — Indigo Parade  (3.19)    indie pop / happy
```

**Adversarial — Loud but Chill** (energy 0.95 + mood "chill")
```
1. Gym Hero — Max Pulse  (5.51)              pop / intense
2. Sunrise City — Neon Echo  (5.31)          pop / happy
3. Storm Runner — Voltline  (3.86)           rock / intense
4. Midnight Coding — LoRoom  (3.80)          lofi / chill
5. Library Rain — Paper Lanterns  (3.58)     lofi / chill
```

**Adversarial — Genreless Middle** (all targets 0.5, unknown genre/mood)
```
1. Midnight Coding — LoRoom  (3.66)          lofi / chill
2. Focus Flow — LoRoom  (3.61)               lofi / focused
3. Library Rain — Paper Lanterns  (3.52)     lofi / chill
4. Coffee Shop Stories — Slow Stereo  (3.49) jazz / relaxed
5. Spacewalk Thoughts — Orbit Bloom  (3.32)  ambient / chill
```

### Profile comparisons — what changed and why

- **High-Energy Pop vs. Chill Lofi:** These are near mirror images. Pop pulls loud, happy,
  danceable tracks (energy ~0.8–0.9); Lofi pulls quiet, mellow tracks (energy ~0.35). The
  energy target flips the whole list, which is exactly what those two profiles are testing.
- **Chill Lofi vs. Deep Intense Rock:** Opposite ends of the energy scale. Lofi's #1 scores
  from *low* energy closeness while Rock's #1 (*Storm Runner*, energy 0.91) scores from
  *high* energy — same math, opposite direction. This confirms the system differentiates
  "chill lofi" from "intense rock," which was the original design goal.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, so they *share* songs
  (Gym Hero, Storm Runner, Sunrise City all appear in both) but in a different order. Genre
  and mood act as the tie-breakers — pop-genre songs float up for the Pop user, intense-mood
  songs float up for the Rock user.
- **Loud but Chill (adversarial) vs. Chill Lofi:** Same "chill" mood, but cranking the energy
  target to 0.95 completely overrides it — the loud profile gets *Gym Hero* and *Sunrise
  City* on top and the real chill tracks drop to #4–#5. This shows energy dominates mood.

### What surprised me

The **weight experiment** was the biggest surprise. I doubled the energy weight (2.0 → 4.0)
and halved the genre weight (2.0 → 1.0). I expected the rankings to reshuffle a lot — but
the **order barely moved**; only the scores changed (the gaps between songs shrank and
off-genre songs crept closer to the top):

```
Chill Lofi — ORIGINAL (genre 2.0 / energy 2.0):
  Library Rain 6.97, Midnight Coding 6.75, Focus Flow 5.84, Spacewalk 4.67, Coffee Shop 3.84
Chill Lofi — EXPERIMENT (genre 1.0 / energy 4.0):
  Library Rain 7.97, Midnight Coding 7.61, Focus Flow 6.74, Spacewalk 6.53, Coffee Shop 5.80
```

The change made the results *different* (compressed scores, off-genre songs closer) but not
more *accurate*. The reason is that in this tiny catalog genre and energy are correlated —
lofi songs are already low-energy — so the two signals say the same thing and re-weighting
one doesn't break the tie.

### Plain-language note (why "Gym Hero" shows up for Happy Pop)

Imagine you tell the app: "I like happy pop music." The app gives you *Gym Hero*, which is
really an intense workout song. Why? The app gives **2 points for matching the genre** (it
*is* pop) and lots of points for being **high-energy** (it's very loud, and you asked for
high energy). But matching your **mood** ("happy") is only worth **1 point** — and *Gym
Hero* is "intense," not "happy." So the app decides that a loud pop song is close enough,
even though the feeling is wrong. In short: the system trusts the *genre label* and the
*loudness* more than the *mood*, so it can hand a gym-pump track to someone who just wanted
something cheerful.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
