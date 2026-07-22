"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.60,
        "target_danceability": 0.55,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 60)
    print(f"Profile: genre={user_prefs['favorite_genre']}, "
          f"mood={user_prefs['favorite_mood']}, energy={user_prefs['target_energy']}")
    print("Top recommendations:")
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}  (score: {score:.2f})")
        for reason in explanation.split("; "):
            print(f"     • {reason}")
    print()


if __name__ == "__main__":
    main()
