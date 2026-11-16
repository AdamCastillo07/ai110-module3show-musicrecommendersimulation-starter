import csv
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
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts with numeric fields converted."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.5
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 0.5

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences and returns (score, reasons)."""
    score = 0.0
    reasons = []

    favorite_genre = user_prefs.get("genre")
    if favorite_genre is not None and song.get("genre") == favorite_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match +{GENRE_WEIGHT}")

    favorite_mood = user_prefs.get("mood")
    if favorite_mood is not None and song.get("mood") == favorite_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match +{MOOD_WEIGHT}")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        closeness = 1 - abs(song.get("energy", 0.0) - target_energy)
        energy_points = ENERGY_WEIGHT * closeness
        score += energy_points
        reasons.append(f"energy closeness +{energy_points:.2f}")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        song_is_acoustic = song.get("acousticness", 0.0) > 0.5
        if song_is_acoustic == likes_acoustic:
            score += ACOUSTIC_WEIGHT
            reasons.append(f"acousticness match +{ACOUSTIC_WEIGHT}")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts by score descending, and returns the top k."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "No matching preferences"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
