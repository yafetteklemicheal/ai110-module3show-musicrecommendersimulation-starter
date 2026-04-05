"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Specific taste profile for comparisons
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy", 
        "target_energy": 0.75,
        "target_tempo_bpm": 120,
        "target_valence": 0.8,
        "target_danceability": 0.8,
        "target_acousticness": 0.2
    }

    print("User Profile:")
    print(f"  Genre: {user_prefs['favorite_genre']}")
    print(f"  Mood: {user_prefs['favorite_mood']}")
    print(f"  Target Energy: {user_prefs['target_energy']}")
    print(f"  Target Tempo: {user_prefs['target_tempo_bpm']} BPM\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("=" * 80)
    print("TOP 5 RECOMMENDATIONS")
    print("=" * 80)
    
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Score: {score:.2f}")
        print(f"   Why: {explanation}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
