"""
Emotional Intelligence

Core emotional intelligence system for agents.
Provides emotional awareness, understanding, and response capabilities.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class EmotionalContext:
    """Context for emotional processing."""
    speaker_emotion: Dict[str, float]
    content_emotion: Dict[str, float]
    situational_emotion: Dict[str, float]
    relationship_context: Optional[Dict[str, Any]] = None


class EmotionalIntelligence:
    """
    Manages emotional intelligence for agent interactions.

    Provides capabilities for:
    - Emotion recognition in text
    - Emotional understanding and empathy
    - Emotionally appropriate responses
    - Emotional regulation
    """

    # Basic emotion dimensions (valence, arousal)
    EMOTION_DIMENSIONS = {
        "joy": {"valence": 0.9, "arousal": 0.7},
        "sadness": {"valence": -0.7, "arousal": -0.3},
        "anger": {"valence": -0.5, "arousal": 0.8},
        "fear": {"valence": -0.6, "arousal": 0.7},
        "surprise": {"valence": 0.2, "arousal": 0.9},
        "disgust": {"valence": -0.7, "arousal": 0.3},
        "anticipation": {"valence": 0.4, "arousal": 0.6},
        "trust": {"valence": 0.7, "arousal": 0.2}
    }

    def __init__(self, empathy_level: float = 0.7):
        """
        Initialize emotional intelligence system.

        Args:
            empathy_level: Ability to understand and share feelings (0.0 to 1.0)
        """
        self.empathy_level = empathy_level
        self.emotional_history: List[Dict[str, Any]] = []
        self.emotional_patterns: Dict[str, Any] = {}

    def recognize_emotion(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, float]:
        """
        Recognize emotions in text.

        Args:
            text: Text to analyze
            context: Optional context

        Returns:
            Dictionary of emotions with intensities
        """
        # This would typically use an emotion recognition model
        # For now, provide a simple implementation

        emotions = {
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "disgust": 0.0,
            "anticipation": 0.0,
            "trust": 0.0
        }

        # Simple keyword matching (placeholder)
        positive_words = ["happy", "good", "great", "love", "wonderful"]
        negative_words = ["sad", "bad", "angry", "hate", "terrible"]

        text_lower = text.lower()

        for word in positive_words:
            if word in text_lower:
                emotions["joy"] += 0.2
                emotions["trust"] += 0.1

        for word in negative_words:
            if word in text_lower:
                emotions["sadness"] += 0.2
                emotions["anger"] += 0.1

        # Normalize
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v / total for k, v in emotions.items()}

        return emotions

    def understand_emotional_context(
        self,
        text: str,
        speaker_state: Optional[Dict[str, float]] = None,
        situational_context: Optional[Dict[str, Any]] = None
    ) -> EmotionalContext:
        """
        Understand the emotional context of an interaction.

        Args:
            text: Text to analyze
            speaker_state: Optional emotional state of speaker
            situational_context: Optional situational information

        Returns:
            EmotionalContext object
        """
        content_emotion = self.recognize_emotion(text)

        return EmotionalContext(
            speaker_emotion=speaker_state or content_emotion,
            content_emotion=content_emotion,
            situational_emotion=self._assess_situational_emotion(situational_context)
        )

    def _assess_situational_emotion(
        self,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Assess emotional tone of situation."""
        # Default neutral emotions
        return {emotion: 0.0 for emotion in self.EMOTION_DIMENSIONS.keys()}

    def generate_emotional_response(
        self,
        emotional_context: EmotionalContext,
        personality_traits: Optional[Dict[str, float]] = None
    ) -> str:
        """
        Generate an emotionally appropriate response.

        Args:
            emotional_context: Emotional context of interaction
            personality_traits: Optional personality traits

        Returns:
            Emotionally appropriate response text
        """
        # Determine appropriate emotional response
        response_emotion = self._determine_response_emotion(
            emotional_context,
            personality_traits
        )

        # Generate response based on emotion
        return self._generate_empathetic_response(response_emotion)

    def _determine_response_emotion(
        self,
        context: EmotionalContext,
        personality: Optional[Dict[str, float]] = None
    ) -> Dict[str, float]:
        """Determine appropriate emotional response."""
        # Mirror speaker emotion with empathy
        response_emotion = context.speaker_emotion.copy()

        # Adjust based on empathy level
        for emotion in response_emotion:
            response_emotion[emotion] *= self.empathy_level

        # Personality influence
        if personality:
            agreeableness = personality.get("agreeableness", 0.5)
            neuroticism = personality.get("neuroticism", 0.5)

            # High agreeableness = more positive responses
            if agreeableness > 0.6:
                response_emotion["joy"] += 0.1
                response_emotion["trust"] += 0.1

            # High neuroticism = more negative responses
            if neuroticism > 0.6:
                response_emotion["sadness"] += 0.1
                response_emotion["fear"] += 0.1

        return response_emotion

    def _generate_empathetic_response(
        self,
        emotion: Dict[str, float]
    ) -> str:
        """Generate empathetic response based on emotion."""
        # Find dominant emotion
        dominant = max(emotion.items(), key=lambda x: x[1])

        if dominant[0] == "joy" and dominant[1] > 0.3:
            return "I'm glad to hear that!"
        elif dominant[0] == "sadness" and dominant[1] > 0.3:
            return "I understand this is difficult for you."
        elif dominant[0] == "anger" and dominant[1] > 0.3:
            return "I can see why you'd feel upset about this."
        elif dominant[0] == "fear" and dominant[1] > 0.3:
            return "It's understandable to feel that way."
        else:
            return "I appreciate you sharing that with me."

    def regulate_emotion(
        self,
        current_emotion: Dict[str, float],
        target_state: str = "balanced"
    ) -> Dict[str, float]:
        """
        Regulate emotions toward a target state.

        Args:
            current_emotion: Current emotional state
            target_state: Target emotional state

        Returns:
            Regulated emotional state
        """
        if target_state == "balanced":
            # Move toward neutral
            regulated = current_emotion.copy()
            for emotion in regulated:
                regulated[emotion] *= 0.7  # Reduce intensity
            return regulated
        else:
            return current_emotion

    def get_emotional_summary(self) -> Dict[str, Any]:
        """Get summary of emotional intelligence metrics."""
        return {
            "empathy_level": self.empathy_level,
            "interactions_processed": len(self.emotional_history),
            "emotional_patterns": self.emotional_patterns
        }
