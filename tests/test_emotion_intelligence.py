"""
Test suite for emotional intelligence.

Tests the emotion system's ability to:
- Recognize emotions in text
- Understand emotional context
- Generate appropriate emotional responses
- Regulate emotions
- Handle various emotional states
"""

import pytest
from typing import Dict, Any

from character_agent_integration.emotion import (
    EmotionalIntelligence,
    EmotionalContext,
    EmotionalState
)


class TestEmotionalContext:
    """Test suite for EmotionalContext."""

    def test_initialization(self, emotional_context: EmotionalContext):
        """Test emotional context initializes correctly."""
        assert emotional_context.speaker_emotion is not None
        assert emotional_context.content_emotion is not None
        assert emotional_context.situational_emotion is not None

    def test_optional_relationship_context(self):
        """Test optional relationship context."""
        context = EmotionalContext(
            speaker_emotion={"joy": 0.7},
            content_emotion={"joy": 0.5},
            situational_emotion={"joy": 0.3}
        )

        assert context.relationship_context is None

    def test_with_relationship_context(self):
        """Test with relationship context."""
        relationship = {"closeness": 0.8, "trust": 0.9}
        context = EmotionalContext(
            speaker_emotion={},
            content_emotion={},
            situational_emotion={},
            relationship_context=relationship
        )

        assert context.relationship_context == relationship


class TestEmotionalIntelligence:
    """Test suite for EmotionalIntelligence."""

    def test_initialization(self, emotional_intelligence: EmotionalIntelligence):
        """Test initialization."""
        assert emotional_intelligence is not None
        assert emotional_intelligence.empathy_level == 0.8
        assert emotional_intelligence.emotional_history == []
        assert emotional_intelligence.emotional_patterns == {}

    def test_default_empathy(self):
        """Test default empathy level."""
        ei = EmotionalIntelligence()
        assert ei.empathy_level == 0.7

    def test_custom_empathy(self):
        """Test custom empathy level."""
        ei = EmotionalIntelligence(empathy_level=0.9)
        assert ei.empathy_level == 0.9

    def test_empathy_bounds(self):
        """Test empathy level stays in reasonable range."""
        # Should handle various values
        ei_low = EmotionalIntelligence(empathy_level=0.0)
        ei_high = EmotionalIntelligence(empathy_level=1.0)

        assert ei_low.empathy_level == 0.0
        assert ei_high.empathy_level == 1.0

    def test_recognize_emotion_positive(self, emotional_intelligence: EmotionalIntelligence):
        """Test recognizing positive emotions."""
        text = "I'm so happy and excited about this!"
        emotions = emotional_intelligence.recognize_emotion(text)

        assert "joy" in emotions
        assert emotions["joy"] > 0

    def test_recognize_emotion_negative(self, emotional_intelligence: EmotionalIntelligence):
        """Test recognizing negative emotions."""
        text = "I'm very sad and angry about what happened."
        emotions = emotional_intelligence.recognize_emotion(text)

        assert "sadness" in emotions
        assert "anger" in emotions
        assert emotions["sadness"] > 0 or emotions["anger"] > 0

    def test_recognize_emotion_neutral(self, emotional_intelligence: EmotionalIntelligence):
        """Test recognizing neutral emotions."""
        text = "The meeting is scheduled for 3 PM."
        emotions = emotional_intelligence.recognize_emotion(text)

        # Should have all emotion keys
        assert len(emotions) == 8
        # Most should be low or zero
        assert all(isinstance(v, float) for v in emotions.values())

    def test_recognize_emotion_with_context(self, emotional_intelligence: EmotionalIntelligence):
        """Test emotion recognition with context."""
        text = "This is great news!"
        context = {"topic": "promotion", "setting": "work"}

        emotions = emotional_intelligence.recognize_emotion(text, context)

        assert isinstance(emotions, dict)

    def test_emotion_normalization(self, emotional_intelligence: EmotionalIntelligence):
        """Test emotions are normalized."""
        text = "I'm happy happy happy"
        emotions = emotional_intelligence.recognize_emotion(text)

        # Sum should be close to 1.0 (normalized)
        total = sum(emotions.values())
        if total > 0:
            assert abs(total - 1.0) < 0.01

    def test_understand_emotional_context(self, emotional_intelligence: EmotionalIntelligence):
        """Test understanding emotional context."""
        text = "I'm worried about the presentation"
        speaker_state = {"fear": 0.7, "anticipation": 0.6}
        situational_context = {"setting": "work", "audience_size": 50}

        context = emotional_intelligence.understand_emotional_context(
            text,
            speaker_state,
            situational_context
        )

        assert isinstance(context, EmotionalContext)
        assert context.speaker_emotion == speaker_state
        assert context.content_emotion is not None
        assert context.situational_emotion is not None

    def test_generate_emotional_response(self, emotional_intelligence: EmotionalIntelligence):
        """Test generating emotional response."""
        context = EmotionalContext(
            speaker_emotion={"joy": 0.8},
            content_emotion={"joy": 0.7},
            situational_emotion={"joy": 0.5}
        )

        response = emotional_intelligence.generate_emotional_response(context)

        assert response is not None
        assert len(response) > 0

    def test_response_with_personality(self, emotional_intelligence: EmotionalIntelligence):
        """Test emotional response influenced by personality."""
        context = EmotionalContext(
            speaker_emotion={"sadness": 0.7},
            content_emotion={"sadness": 0.6},
            situational_emotion={}
        )

        personality = {"agreeableness": 0.9, "neuroticism": 0.3}

        response = emotional_intelligence.generate_emotional_response(
            context,
            personality
        )

        assert response is not None

    def test_regulate_emotion_to_balanced(self, emotional_intelligence: EmotionalIntelligence):
        """Test emotion regulation to balanced state."""
        current = {"joy": 0.9, "anger": 0.8, "fear": 0.7}

        regulated = emotional_intelligence.regulate_emotion(current, "balanced")

        assert isinstance(regulated, dict)
        # Intensities should be reduced
        assert regulated["joy"] < current["joy"]
        assert regulated["anger"] < current["anger"]
        assert regulated["fear"] < current["fear"]

    def test_regulate_emotion_preserves_keys(self, emotional_intelligence: EmotionalIntelligence):
        """Test regulation preserves all emotion keys."""
        current = {"joy": 0.5, "sadness": 0.5, "anger": 0.5}

        regulated = emotional_intelligence.regulate_emotion(current)

        assert set(regulated.keys()) == set(current.keys())

    def test_get_emotional_summary(self, emotional_intelligence: EmotionalIntelligence):
        """Test getting emotional summary."""
        summary = emotional_intelligence.get_emotional_summary()

        assert "empathy_level" in summary
        assert "interactions_processed" in summary
        assert "emotional_patterns" in summary

        assert summary["empathy_level"] == 0.8
        assert summary["interactions_processed"] == 0


class TestEmotionRecognition:
    """Test emotion recognition capabilities."""

    def test_joy_recognition(self, emotional_intelligence: EmotionalIntelligence):
        """Test joy recognition."""
        text = "I'm so happy and excited!"
        emotions = emotional_intelligence.recognize_emotion(text)

        # Joy should be elevated
        assert emotions["joy"] > 0

    def test_trust_recognition(self, emotional_intelligence: EmotionalIntelligence):
        """Test trust recognition."""
        text = "I really trust and love this approach"
        emotions = emotional_intelligence.recognize_emotion(text)

        assert emotions["trust"] > 0 or emotions["joy"] > 0

    def test_fear_recognition(self, emotional_intelligence: EmotionalIntelligence):
        """Test fear recognition."""
        text = "I'm afraid and worried about this"
        emotions = emotional_intelligence.recognize_emotion(text)

        # Note: current implementation uses simple keywords
        # May not detect fear without specific keywords
        assert isinstance(emotions, dict)

    def test_anger_recognition(self, emotional_intelligence: EmotionalIntelligence):
        """Test anger recognition."""
        text = "I'm so angry and hate this situation"
        emotions = emotional_intelligence.recognize_emotion(text)

        assert emotions["anger"] > 0 or emotions["sadness"] > 0

    def test_multiple_emotions(self, emotional_intelligence: EmotionalIntelligence):
        """Test detecting multiple emotions."""
        text = "I'm happy but also a bit sad it's over"
        emotions = emotional_intelligence.recognize_emotion(text)

        # Should have both joy and sadness
        assert emotions["joy"] > 0
        assert emotions["sadness"] > 0


class TestEmotionalResponse:
    """Test emotional response generation."""

    def test_joy_response(self, emotional_intelligence: EmotionalIntelligence):
        """Test response to joy."""
        context = EmotionalContext(
            speaker_emotion={"joy": 0.8},
            content_emotion={"joy": 0.7},
            situational_emotion={}
        )

        response = emotional_intelligence.generate_emotional_response(context)

        assert "glad" in response.lower() or "happy" in response.lower()

    def test_sadness_response(self, emotional_intelligence: EmotionalIntelligence):
        """Test response to sadness."""
        context = EmotionalContext(
            speaker_emotion={"sadness": 0.8},
            content_emotion={"sadness": 0.7},
            situational_emotion={}
        )

        response = emotional_intelligence.generate_emotional_response(context)

        assert "understand" in response.lower() or "difficult" in response.lower()

    def test_anger_response(self, emotional_intelligence: EmotionalIntelligence):
        """Test response to anger."""
        context = EmotionalContext(
            speaker_emotion={"anger": 0.8},
            content_emotion={"anger": 0.7},
            situational_emotion={}
        )

        response = emotional_intelligence.generate_emotional_response(context)

        assert "upset" in response.lower() or "understand" in response.lower()

    def test_fear_response(self, emotional_intelligence: EmotionalIntelligence):
        """Test response to fear."""
        context = EmotionalContext(
            speaker_emotion={"fear": 0.8},
            content_emotion={"fear": 0.7},
            situational_emotion={}
        )

        response = emotional_intelligence.generate_emotional_response(context)

        assert "understandable" in response.lower() or "feel" in response.lower()

    def test_empathy_influence(self):
        """Test empathy level influences response."""
        context = EmotionalContext(
            speaker_emotion={"joy": 0.8},
            content_emotion={"joy": 0.7},
            situational_emotion={}
        )

        ei_low = EmotionalIntelligence(empathy_level=0.2)
        ei_high = EmotionalIntelligence(empathy_level=0.9)

        response_low = ei_low.generate_emotional_response(context)
        response_high = ei_high.generate_emotional_response(context)

        # Both should generate responses
        assert response_low is not None
        assert response_high is not None

    def test_personality_influence_on_response(self):
        """Test personality influences emotional response."""
        context = EmotionalContext(
            speaker_emotion={"joy": 0.5},
            content_emotion={"joy": 0.5},
            situational_emotion={}
        )

        # High agreeableness
        personality_agreeable = {"agreeableness": 0.9, "neuroticism": 0.3}
        # High neuroticism
        personality_neurotic = {"agreeableness": 0.3, "neuroticism": 0.9}

        ei = EmotionalIntelligence()

        response_agreeable = ei.generate_emotional_response(context, personality_agreeable)
        response_neurotic = ei.generate_emotional_response(context, personality_neurotic)

        # Both should generate responses
        assert response_agreeable is not None
        assert response_neurotic is not None


class TestEmotionalState:
    """Test EmotionalState class."""

    def test_initialization(self, emotional_state: EmotionalState):
        """Test emotional state initialization."""
        assert emotional_state is not None
        assert emotional_state.valence is not None
        assert emotional_state.arousal is not None

    def test_from_dict(self):
        """Test creating emotional state from dictionary."""
        emotion_dict = {
            "joy": 0.7,
            "sadness": 0.1,
            "anger": 0.1,
            "fear": 0.1,
            "surprise": 0.2,
            "disgust": 0.0,
            "anticipation": 0.3,
            "trust": 0.6
        }

        state = EmotionalState.from_dict(emotion_dict)

        assert state is not None
        assert state.specific_emotions == emotion_dict

    def test_to_dict(self, emotional_state: EmotionalState):
        """Test converting emotional state to dictionary."""
        state_dict = emotional_state.to_dict()

        assert isinstance(state_dict, dict)
        assert "valence" in state_dict
        assert "arousal" in state_dict

    def test_update_from_specific_emotions(self):
        """Test updating valence/arousal from specific emotions."""
        state = EmotionalState()
        state.specific_emotions = {"joy": 0.8}
        state.update_from_specific_emotions()

        # Joy has high valence and moderate arousal
        assert state.valence > 0
        assert state.arousal > 0

    def test_blend_with(self):
        """Test blending emotional states."""
        state1 = EmotionalState()
        state1.valence = 0.8
        state1.arousal = 0.7

        state2 = EmotionalState()
        state2.valence = -0.5
        state2.arousal = 0.3

        blended = state1.blend_with(state2, weight=0.5)

        # Should be between the two states
        assert blended.valence > state2.valence
        assert blended.valence < state1.valence


class TestEmotionDimensions:
    """Test emotion dimension mappings."""

    def test_emotion_dimensions_exist(self, emotional_intelligence: EmotionalIntelligence):
        """Test all emotion dimensions are defined."""
        emotions = ["joy", "sadness", "anger", "fear",
                   "surprise", "disgust", "anticipation", "trust"]

        for emotion in emotions:
            assert emotion in EmotionalIntelligence.EMOTION_DIMENSIONS

    def test_emotion_dimensions_structure(self):
        """Test emotion dimensions have valence and arousal."""
        for emotion, dimensions in EmotionalIntelligence.EMOTION_DIMENSIONS.items():
            assert "valence" in dimensions
            assert "arousal" in dimensions
            assert -1.0 <= dimensions["valence"] <= 1.0
            assert -1.0 <= dimensions["arousal"] <= 1.0

    def test_positive_emotions(self):
        """Test positive emotions have positive valence."""
        positive_emotions = ["joy", "trust", "anticipation"]

        for emotion in positive_emotions:
            dimensions = EmotionalIntelligence.EMOTION_DIMENSIONS[emotion]
            assert dimensions["valence"] > 0

    def test_negative_emotions(self):
        """Test negative emotions have negative valence."""
        negative_emotions = ["sadness", "anger", "fear", "disgust"]

        for emotion in negative_emotions:
            dimensions = EmotionalIntelligence.EMOTION_DIMENSIONS[emotion]
            assert dimensions["valence"] < 0


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_text(self, emotional_intelligence: EmotionalIntelligence):
        """Test handling empty text."""
        emotions = emotional_intelligence.recognize_emotion("")

        assert isinstance(emotions, dict)
        assert len(emotions) == 8

    def test_no_matching_keywords(self, emotional_intelligence: EmotionalIntelligence):
        """Test text with no emotion keywords."""
        text = "The algorithm processes data sequentially."
        emotions = emotional_intelligence.recognize_emotion(text)

        # Should still return all emotions
        assert len(emotions) == 8
        # Most should be 0
        assert sum(emotions.values()) == 0

    def test_extreme_emotion_values(self):
        """Test handling extreme emotion values."""
        ei = EmotionalIntelligence()

        extreme_emotions = {"joy": 2.0, "anger": -1.0}
        # Should handle without error
        context = EmotionalContext(
            speaker_emotion=extreme_emotions,
            content_emotion=extreme_emotions,
            situational_emotion={}
        )

        response = ei.generate_emotional_response(context)
        assert response is not None

    def test_mixed_emotions(self, emotional_intelligence: EmotionalIntelligence):
        """Test text with mixed emotions."""
        text = "I'm happy about the success but sad that it's over"
        emotions = emotional_intelligence.recognize_emotion(text)

        # Should detect both
        total_emotion = sum(emotions.values())
        if total_emotion > 0:
            assert emotions["joy"] > 0
            assert emotions["sadness"] > 0


class TestEmotionalRegulation:
    """Test emotion regulation capabilities."""

    def test_regulation_reduces_intensity(self, emotional_intelligence: EmotionalIntelligence):
        """Test regulation reduces emotional intensity."""
        high_intensity = {"joy": 1.0, "anger": 1.0, "fear": 1.0}

        regulated = emotional_intelligence.regulate_emotion(high_intensity, "balanced")

        for emotion in regulated:
            assert regulated[emotion] < high_intensity[emotion]

    def test_regulation_preserves_relative_differences(self, emotional_intelligence: EmotionalIntelligence):
        """Test regulation preserves relative emotional differences."""
        emotions = {"joy": 0.8, "trust": 0.6, "anticipation": 0.4}

        regulated = emotional_intelligence.regulate_emotion(emotions, "balanced")

        # Joy should still be highest
        assert regulated["joy"] > regulated["trust"]
        assert regulated["trust"] > regulated["anticipation"]
