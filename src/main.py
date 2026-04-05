"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import List, Dict
from recommender import load_songs, recommend_songs


def print_recommendations(title: str, user_prefs: Dict, songs: List[Dict], k: int = 5) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    print(f"Genre: {user_prefs['favorite_genre']}, Mood: {user_prefs['favorite_mood']}, Energy: {user_prefs['target_energy']}, Tempo: {user_prefs['target_tempo_bpm']} BPM")
    print(f"Valence: {user_prefs['target_valence']}, Danceability: {user_prefs['target_danceability']}, Acousticness: {user_prefs['target_acousticness']}")

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Score: {score:.2f}")
        print(f"   Why: {explanation}")
    print("\n" + "=" * 80)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    profiles = [
        {
            "name": "High-Energy Pop",
            "prefs": {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.9,
                "target_tempo_bpm": 130,
                "target_valence": 0.9,
                "target_danceability": 0.9,
                "target_acousticness": 0.1,
            },
        },
        {
            "name": "Chill Lofi",
            "prefs": {
                "favorite_genre": "lofi",
                "favorite_mood": "chill",
                "target_energy": 0.35,
                "target_tempo_bpm": 80,
                "target_valence": 0.6,
                "target_danceability": 0.6,
                "target_acousticness": 0.75,
            },
        },
        {
            "name": "Deep Intense Rock",
            "prefs": {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.95,
                "target_tempo_bpm": 150,
                "target_valence": 0.4,
                "target_danceability": 0.65,
                "target_acousticness": 0.1,
            },
        },
        {
            "name": "Edge Case: High Energy Sad",
            "prefs": {
                "favorite_genre": "pop",
                "favorite_mood": "melancholic",
                "target_energy": 0.9,
                "target_tempo_bpm": 130,
                "target_valence": 0.2,
                "target_danceability": 0.6,
                "target_acousticness": 0.2,
            },
        },
        {
            "name": "Edge Case: Calm Metal",
            "prefs": {
                "favorite_genre": "metal",
                "favorite_mood": "relaxed",
                "target_energy": 0.2,
                "target_tempo_bpm": 70,
                "target_valence": 0.5,
                "target_danceability": 0.3,
                "target_acousticness": 0.5,
            },
        },
    ]

    print("=" * 80)
    print("USER PROFILE EXPERIMENTS")
    print("=" * 80)

    for profile in profiles:
        print_recommendations(profile["name"], profile["prefs"], songs, k=5)

    # Specific comment: With the current weight settings, songs like Sunrise City rank first for pop/happy profiles because they match genre and mood while also being very close on energy, tempo, and valence.
    # The higher energy weight means that a strong energy match can pull a song ahead even when the genre or mood match is not perfect.


if __name__ == "__main__":
    main()
