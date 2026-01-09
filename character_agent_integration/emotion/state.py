"""
Emotional State

Represents and manages the emotional state of an agent.
"""

from typing import Dict, Optional
from dataclasses import dataclass, field


@dataclass
class EmotionalState:
    """
    Represents the current emotional state of an agent.

    Uses a dimensional model of emotion:
    - Valence: positive to negative (-1.0 to 1.0)
    - Arousal: calm to excited (-1.0 to 1.0)
    - Specific emotions: joy, sadness, anger, fear, etc. (0.0 to 1.0)
    """

    valence: float = 0.0  # -1.0 (negative) to 1.0 (positive)
    arousal: float = 0.0  # -1.0 (calm) to 1.0 (excited)
    specific_emotions: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize default specific emotions if not provided."""
        if not self.specific_emotions:
            self.specific_emotions = {
                "joy": 0.0,
                "sadness": 0.0,
                "anger": 0.0,
                "fear": 0.0,
                "surprise": 0.0,
                "disgust": 0.0,
                "anticipation": 0.0,
                "trust": 0.0
            }

    def update_from_specific_emotions(self) -> None:
        """Update valence and arousal based on specific emotions."""
        if not self.specific_emotions:
            return

        # Weight emotions by their valence/arousal contributions
        valence_sum = 0.0
        arousal_sum = 0.0
        total_weight = 0.0

        emotion_weights = {
            "joy": {"valence": 1.0, "arousal": 0.7},
            "sadness": {"valence": -0.7, "arousal": -0.3},
            "anger": {"valence": -0.5, "arousal": 0.8},
            "fear": {"valence": -0.6, "arousal": 0.7},
            "surprise": {"valence": 0.2, "arousal": 0.9},
            "disgust": {"valence": -0.7, "arousal": 0.3},
            "anticipation": {"valence": 0.4, "arousal": 0.6},
            "trust": {"valence": 0.7, "arousal": 0.2}
        }

        for emotion, intensity in self.specific_emotions.items():
            if emotion in emotion_weights:
                weights = emotion_weights[emotion]
                valence_sum += weights["valence"] * intensity
                arousal_sum += weights["arousal"] * intensity
                total_weight += intensity

        if total_weight > 0:
            self.valence = max(-1.0, min(1.0, valence_sum / total_weight))
            self.arousal = max(-1.0, min(1.0, arousal_sum / total_weight))

    def get_dominant_emotion(self) -> tuple[str, float]:
        """Get the dominant specific emotion and its intensity."""
        if not self.specific_emotions:
            return "neutral", 0.0

        dominant = max(self.specific_emotions.items(), key=lambda x: x[1])
        return dominant

    def get_emotional_summary(self) -> str:
        """Get a human-readable summary of the emotional state."""
        dominant_emotion, intensity = self.get_dominant_emotion()

        if intensity < 0.2:
            state_desc = "calm and neutral"
        elif self.valence > 0.3:
            if self.arousal > 0.3:
                state_desc = "excited and positive"
            else:
                state_desc = "content and relaxed"
        elif self.valence < -0.3:
            if self.arousal > 0.3:
                state_desc = "distressed and upset"
            else:
                state_desc = "down and melancholic"
        else:
            state_desc = "moderately activated"

        return f"{state_desc} (dominant: {dominant_emotion}, intensity: {intensity:.2f})"

    def blend_with(self, other: "EmotionalState", weight: float = 0.5) -> "EmotionalState":
        """
        Blend this emotional state with another.

        Args:
            other: Other emotional state to blend with
            weight: Weight for the other state (0.0 to 1.0)

        Returns:
            New blended EmotionalState
        """
        blended = EmotionalState()

        blended.valence = self.valence * (1 - weight) + other.valence * weight
        blended.arousal = self.arousal * (1 - weight) + other.arousal * weight

        for emotion in self.specific_emotions:
            self_intensity = self.specific_emotions.get(emotion, 0.0)
            other_intensity = other.specific_emotions.get(emotion, 0.0)
            blended.specific_emotions[emotion] = (
                self_intensity * (1 - weight) + other_intensity * weight
            )

        return blended

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            **self.specific_emotions
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "EmotionalState":
        """Create from dictionary."""
        valence = data.pop("valence", 0.0)
        arousal = data.pop("arousal", 0.0)
        return cls(valence=valence, arousal=arousal, specific_emotions=data)
