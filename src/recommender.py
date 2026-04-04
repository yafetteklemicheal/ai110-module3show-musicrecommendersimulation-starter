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
        # Score and sort songs
        scored = []
        for song in self.songs:
            score = 0.0
            
            if song.genre == user.favorite_genre:
                score += 4.0
            if song.mood == user.favorite_mood:
                score += 2.5
            
            energy_diff = abs(song.energy - user.target_energy)
            score += 1.8 * (1 - energy_diff)
            
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

def score_song(user_prefs: Dict, song: Dict) -> float:
    """
    Scores a single song based on user preferences.
    Returns a numeric score reflecting compatibility.
    """
    score = 0.0
    
    # Genre match: +2.0 points
    if song['genre'] == user_prefs['favorite_genre']:
        score += 2.0
    
    # Mood match: +1.0 point
    if song['mood'] == user_prefs['favorite_mood']:
        score += 1.0
    
    # Energy similarity: 1.0 * (1 - abs(diff))
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    score += 1.0 * (1 - energy_diff)
    
    # Additional balanced weights for other features
    tempo_diff = abs(song['tempo_bpm'] - user_prefs['target_tempo_bpm'])
    score += 0.8 * max(0, 1 - tempo_diff / 70)  # Normalize tempo diff
    
    valence_diff = abs(song['valence'] - user_prefs['target_valence'])
    score += 0.6 * (1 - valence_diff)
    
    dance_diff = abs(song['danceability'] - user_prefs['target_danceability'])
    score += 0.4 * (1 - dance_diff)
    
    acoustic_diff = abs(song['acousticness'] - user_prefs['target_acousticness'])
    score += 0.4 * (1 - acoustic_diff)
    
    return score

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score = score_song(user_prefs, song)
        reasons = []
        
        if song['genre'] == user_prefs['favorite_genre']:
            reasons.append("matches your favorite genre")
        if song['mood'] == user_prefs['favorite_mood']:
            reasons.append("matches your favorite mood")
        if abs(song['energy'] - user_prefs['target_energy']) < 0.2:
            reasons.append("close to your preferred energy level")
        if abs(song['tempo_bpm'] - user_prefs['target_tempo_bpm']) < 20:
            reasons.append("tempo matches your preference")
        if abs(song['valence'] - user_prefs['target_valence']) < 0.2:
            reasons.append("valence aligns with your taste")
        
        explanation = "This song " + ", ".join(reasons) if reasons else "has some matching attributes"
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
