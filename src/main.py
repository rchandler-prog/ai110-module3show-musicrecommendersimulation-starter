"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Profiles used to stress-test the recommender.
# The last two are "adversarial": they mix preferences that fight each other.
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop", "favorite_mood": "happy",
        "target_energy": 0.90, "target_valence": 0.85, "target_danceability": 0.85,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi", "favorite_mood": "chill",
        "target_energy": 0.35, "target_valence": 0.60, "target_danceability": 0.55,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock", "favorite_mood": "intense",
        "target_energy": 0.90, "target_valence": 0.50, "target_danceability": 0.60,
    },
    "Adversarial: Loud but Chill (energy 0.95 + mood chill)": {
        "favorite_genre": "pop", "favorite_mood": "chill",
        "target_energy": 0.95, "target_valence": 0.50, "target_danceability": 0.70,
    },
    "Adversarial: Genreless Middle (all targets 0.5)": {
        "favorite_genre": "unknown", "favorite_mood": "unknown",
        "target_energy": 0.50, "target_valence": 0.50, "target_danceability": 0.50,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print("\n" + "=" * 60)
    print(f"Profile: {name}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(
        recommend_songs(user_prefs, songs, k=k), start=1
    ):
        print(f"\n{rank}. {song['title']} — {song['artist']}  (score: {score:.2f})")
        for reason in explanation.split("; "):
            print(f"     • {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
