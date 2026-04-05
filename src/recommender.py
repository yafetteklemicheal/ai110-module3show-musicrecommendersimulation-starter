from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_tempo_bpm: float
    target_valence: float
    target_danceability: float
    target_acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by compatibility with the user's profile."""
        scored = []
        for song in self.songs:
            score = 0.0
            
            if song.genre == user.favorite_genre:
                score += 2.0
            if song.mood == user.favorite_mood:
                score += 2.5
            
            energy_diff = abs(song.energy - user.target_energy)
            score += 3.6 * (1 - energy_diff)
            
            tempo_diff = abs(song.tempo_bpm - user.target_tempo_bpm)
            score += 1.2 * max(0, 1 - tempo_diff / 70)
            
            valence_diff = abs(song.valence - user.target_valence)
            score += 1.0 * (1 - valence_diff)
            
            dance_diff = abs(song.danceability - user.target_danceability)
            score += 0.5 * (1 - dance_diff)
            
            acoustic_diff = abs(song.acousticness - user.target_acousticness)
            score += 0.5 * (1 - acoustic_diff)
            
            scored.append((song, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a human-readable explanation for why a song is recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("matches your favorite genre")
        if song.mood == user.favorite_mood:
            reasons.append("matches your favorite mood")
        if abs(song.energy - user.target_energy) < 0.2:
            reasons.append("energy level is close to your preference")
        if abs(song.tempo_bpm - user.target_tempo_bpm) < 20:
            reasons.append("tempo aligns with your taste")
        if abs(song.valence - user.target_valence) < 0.2:
            reasons.append("valence matches your preference")
        return "Recommended because it " + ", ".join(reasons) if reasons else "has some compatible attributes"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song based on user preferences.
    Returns a numeric score and a list of scoring reasons.
    """
    score = 0.0
    reasons = []
    
    # Genre match: +1.0 points
    if song['genre'] == user_prefs['favorite_genre']:
        score += 1.0
        reasons.append("genre match (+1.0)")
    
    # Mood match: +1.0 point
    if song['mood'] == user_prefs['favorite_mood']:
        score += 1.0
        reasons.append("mood match (+1.0)")
    
    # Energy similarity: 2.0 * (1 - abs(diff))
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_score = 2.0 * (1 - energy_diff)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")
    
    # Tempo closeness: +0.8 points when near the target tempo
    tempo_diff = abs(song['tempo_bpm'] - user_prefs['target_tempo_bpm'])
    tempo_score = 0.8 * max(0, 1 - tempo_diff / 70)
    score += tempo_score
    reasons.append(f"tempo closeness (+{tempo_score:.2f})")
    
    # Valence similarity: +0.6 points
    valence_diff = abs(song['valence'] - user_prefs['target_valence'])
    valence_score = 0.6 * (1 - valence_diff)
    score += valence_score
    reasons.append(f"valence similarity (+{valence_score:.2f})")
    
    # Danceability similarity: +0.4 points
    dance_diff = abs(song['danceability'] - user_prefs['target_danceability'])
    dance_score = 0.4 * (1 - dance_diff)
    score += dance_score
    reasons.append(f"danceability similarity (+{dance_score:.2f})")
    
    # Acousticness similarity: +0.4 points
    acoustic_diff = abs(song['acousticness'] - user_prefs['target_acousticness'])
    acoustic_score = 0.4 * (1 - acoustic_diff)
    score += acoustic_score
    reasons.append(f"acousticness similarity (+{acoustic_score:.2f})")
    
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "This song " + " + ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
