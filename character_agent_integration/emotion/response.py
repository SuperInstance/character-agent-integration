"""
Emotional Response

Generates emotionally appropriate responses for agents.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class EmotionalResponse:
    """
    An emotionally appropriate response.

    Contains the response text along with its emotional characteristics.
    """
    text: str
    emotion: Dict[str, float]
    valence: float
    arousal: float
    empathy_level: float
    appropriateness: float

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "emotion": self.emotion,
            "valence": self.valence,
            "arousal": self.arousal,
            "empathy_level": self.empathy_level,
            "appropriateness": self.appropriateness
        }


class EmotionalResponseGenerator:
    """Generates emotionally appropriate responses."""

    def __init__(self):
        """Initialize the response generator."""
        self.response_templates = {
            "joy": [
                "That's wonderful to hear!",
                "I'm so glad for you!",
                "That makes me happy!"
            ],
            "sadness": [
                "I understand this is difficult.",
                "I'm here for you.",
                "It's okay to feel this way."
            ],
            "anger": [
                "I can see why you're upset.",
                "Your feelings are valid.",
                "Let's work through this together."
            ],
            "fear": [
                "It's understandable to feel that way.",
                "You're not alone in this.",
                "We can face this together."
            ]
        }

    def generate_response(
        self,
        input_emotion: Dict[str, float],
        empathy_level: float = 0.7,
        personality_traits: Optional[Dict[str, float]] = None
    ) -> EmotionalResponse:
        """
        Generate an emotionally appropriate response.

        Args:
            input_emotion: Emotional state to respond to
            empathy_level: Level of empathy to show
            personality_traits: Optional personality traits

        Returns:
            EmotionalResponse object
        """
        # Determine dominant emotion
        dominant_emotion = max(input_emotion.items(), key=lambda x: x[1])
        emotion_name, intensity = dominant_emotion

        # Select appropriate response template
        if intensity > 0.3 and emotion_name in self.response_templates:
            templates = self.response_templates[emotion_name]
            import random
            text = random.choice(templates)
        else:
            text = "I appreciate you sharing that with me."

        # Calculate response emotional characteristics
        response_valence = self._calculate_response_valence(
            input_emotion, empathy_level
        )
        response_arousal = self._calculate_response_arousal(
            input_emotion, empathy_level
        )

        # Apply personality influence
        if personality_traits:
            text = self._apply_personality(
                text, personality_traits
            )

        return EmotionalResponse(
            text=text,
            emotion=input_emotion,
            valence=response_valence,
            arousal=response_arousal,
            empathy_level=empathy_level,
            appropriateness=self._assess_appropriateness(
                input_emotion, text
            )
        )

    def _calculate_response_valence(
        self,
        input_emotion: Dict[str, float],
        empathy_level: float
    ) -> float:
        """Calculate appropriate valence for response."""
        # Mirror input emotion somewhat, but moderate with empathy
        joy = input_emotion.get("joy", 0.0)
        sadness = input_emotion.get("sadness", 0.0)
        anger = input_emotion.get("anger", 0.0)

        valence = (joy * 0.9 + sadness * -0.7 + anger * -0.5)
        return max(-1.0, min(1.0, valence * empathy_level))

    def _calculate_response_arousal(
        self,
        input_emotion: Dict[str, float],
        empathy_level: float
    ) -> float:
        """Calculate appropriate arousal for response."""
        # Moderate arousal relative to input
        emotions = list(input_emotion.values())
        if not emotions:
            return 0.0

        avg_arousal = sum(emotions) / len(emotions)
        return max(-1.0, min(1.0, avg_arousal * empathy_level * 0.7))

    def _apply_personality(
        self,
        text: str,
        personality: Dict[str, float]
    ) -> str:
        """Apply personality to response."""
        # High extraversion: more enthusiastic
        if personality.get("extraversion", 0.5) > 0.7:
            text = text + " " + "I'm really excited to talk more about this!"

        # High agreeableness: more supportive
        if personality.get("agreeableness", 0.5) > 0.7:
            text = "I want to support you. " + text

        return text

    def _assess_appropriateness(
        self,
        input_emotion: Dict[str, float],
        response_text: str
    ) -> float:
        """Assess how appropriate the response is."""
        # Placeholder: would use more sophisticated analysis
        return 0.8
