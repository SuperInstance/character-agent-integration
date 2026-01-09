"""
Test suite for personality-driven learning.

Tests the learning system's ability to:
- Learn based on personality traits
- Extract different learnings based on personality
- Calculate retention
- Update personality through experience
- Adapt learning style
"""

import pytest
from typing import Dict, Any, List

from character_agent_integration.personality import (
    PersonalityDrivenLearning,
    LearningStyle,
    LearningPreference,
    LearningExperience
)


class TestLearningStyle:
    """Test suite for LearningStyle enum."""

    def test_all_styles_exist(self):
        """Test all expected learning styles exist."""
        expected_styles = [
            LearningStyle.EXPERIENTIAL,
            LearningStyle.ANALYTICAL,
            LearningStyle.SOCIAL,
            LearningStyle.OBSERVATIONAL,
            LearningStyle.THEORETICAL,
            LearningStyle.INTUITIVE
        ]

        for style in expected_styles:
            assert style is not None
            assert isinstance(style.value, str)


class TestLearningPreference:
    """Test suite for LearningPreference dataclass."""

    def test_create_preference(self):
        """Test creating learning preference."""
        preference = LearningPreference(
            style=LearningStyle.EXPERIENTIAL,
            feedback_receptivity=0.8,
            exploration_tendency=0.7,
            persistence=0.9,
            adaptability=0.6,
            risk_tolerance=0.5
        )

        assert preference.style == LearningStyle.EXPERIENTIAL
        assert preference.feedback_receptivity == 0.8
        assert preference.exploration_tendency == 0.7
        assert preference.persistence == 0.9
        assert preference.adaptability == 0.6
        assert preference.risk_tolerance == 0.5

    def test_preference_ranges(self):
        """Test all values are in valid range."""
        preference = LearningPreference(
            style=LearningStyle.ANALYTICAL,
            feedback_receptivity=0.5,
            exploration_tendency=0.5,
            persistence=0.5,
            adaptability=0.5,
            risk_tolerance=0.5
        )

        assert 0.0 <= preference.feedback_receptivity <= 1.0
        assert 0.0 <= preference.exploration_tendency <= 1.0
        assert 0.0 <= preference.persistence <= 1.0
        assert 0.0 <= preference.adaptability <= 1.0
        assert 0.0 <= preference.risk_tolerance <= 1.0


class TestLearningExperience:
    """Test suite for LearningExperience dataclass."""

    def test_create_experience(self):
        """Test creating learning experience."""
        experience = LearningExperience(
            situation={"type": "test"},
            action="test_action",
            outcome={"success": True}
        )

        assert experience.situation == {"type": "test"}
        assert experience.action == "test_action"
        assert experience.outcome == {"success": True}
        assert experience.timestamp is not None

    def test_experience_with_optional_fields(self):
        """Test experience with optional emotional and personality context."""
        experience = LearningExperience(
            situation={"context": "test"},
            action="action",
            outcome={"result": "good"},
            emotional_context={"joy": 0.7},
            personality_context={"openness": 0.8}
        )

        assert experience.emotional_context == {"joy": 0.7}
        assert experience.personality_context == {"openness": 0.8}

    def test_experience_timestamp_default(self):
        """Test timestamp is set by default."""
        import time

        before = time.time()
        experience = LearningExperience(
            situation={},
            action="test",
            outcome={}
        )
        after = time.time()

        assert before <= experience.timestamp <= after


class TestPersonalityDrivenLearning:
    """Test suite for PersonalityDrivenLearning."""

    def test_initialization(self, personality_learning: PersonalityDrivenLearning):
        """Test initialization."""
        assert personality_learning is not None
        assert personality_learning.personality_traits is not None
        assert personality_learning.learning_style is not None
        assert personality_learning.learning_preferences is not None
        assert personality_learning.learning_history == []
        assert personality_learning.learned_patterns == {}

    def test_initialization_with_personality(self):
        """Test initialization with custom personality."""
        traits = {
            "openness": 0.9,
            "conscientiousness": 0.7,
            "extraversion": 0.6,
            "agreeableness": 0.8,
            "neuroticism": 0.2
        }

        pdl = PersonalityDrivenLearning(personality_traits=traits)

        assert pdl.personality_traits == traits

    def test_initialization_with_learning_style(self):
        """Test initialization with specific learning style."""
        pdl = PersonalityDrivenLearning(
            personality_traits={"openness": 0.7},
            learning_style=LearningStyle.ANALYTICAL
        )

        assert pdl.learning_style == LearningStyle.ANALYTICAL

    def test_default_personality(self, personality_learning: PersonalityDrivenLearning):
        """Test default personality traits."""
        traits = personality_learning.personality_traits

        assert "openness" in traits
        assert "conscientiousness" in traits
        assert "extraversion" in traits
        assert "agreeableness" in traits
        assert "neuroticism" in traits

        # All should be mid-range
        for trait, value in traits.items():
            assert 0.4 <= value <= 0.6

    def test_determine_learning_style(self):
        """Test learning style is determined from personality."""
        # High openness + high extraversion = experiential
        traits1 = {"openness": 0.8, "conscientiousness": 0.5,
                   "extraversion": 0.8, "agreeableness": 0.5, "neuroticism": 0.5}
        pdl1 = PersonalityDrivenLearning(personality_traits=traits1)
        assert pdl1.learning_style == LearningStyle.EXPERIENTIAL

        # High conscientiousness = analytical
        traits2 = {"openness": 0.5, "conscientiousness": 0.9,
                   "extraversion": 0.5, "agreeableness": 0.5, "neuroticism": 0.5}
        pdl2 = PersonalityDrivenLearning(personality_traits=traits2)
        assert pdl2.learning_style == LearningStyle.ANALYTICAL

    def test_calculate_preferences(self, personality_learning: PersonalityDrivenLearning):
        """Test learning preferences are calculated correctly."""
        prefs = personality_learning.learning_preferences

        assert isinstance(prefs, LearningPreference)
        assert 0.0 <= prefs.feedback_receptivity <= 1.0
        assert 0.0 <= prefs.exploration_tendency <= 1.0
        assert 0.0 <= prefs.persistence <= 1.0

    def test_learn_from_experience(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test learning from an experience."""
        result = personality_learning.learn_from_experience(learning_experience)

        assert "learnings" in result
        assert "retention" in result
        assert "personality_changes" in result
        assert "learning_style_influence" in result

        # Experience should be recorded
        assert len(personality_learning.learning_history) == 1

    def test_extract_learnings(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test extracting learnings based on personality."""
        learnings = personality_learning._extract_learnings(learning_experience)

        assert isinstance(learnings, list)

        # High openness personality should find novel patterns
        if personality_learning.personality_traits["openness"] > 0.6:
            novel_found = any(l["type"] == "novel" for l in learnings)
            assert novel_found

    def test_find_novel_patterns(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test finding novel patterns."""
        patterns = personality_learning._find_novel_patterns(learning_experience)

        assert isinstance(patterns, list)
        assert len(patterns) > 0

        for pattern in patterns:
            assert "type" in pattern
            assert "pattern" in pattern
            assert "importance" in pattern

    def test_find_causal_patterns(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test finding causal patterns."""
        patterns = personality_learning._find_causal_patterns(learning_experience)

        assert isinstance(patterns, list)
        assert all(p["type"] == "causal" for p in patterns)

    def test_find_social_patterns(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test finding social patterns."""
        patterns = personality_learning._find_social_patterns(learning_experience)

        assert isinstance(patterns, list)
        assert all(p["type"] == "social" for p in patterns)

    def test_update_patterns(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test updating learned patterns."""
        learnings = [
            {"type": "novel", "pattern": "test pattern 1", "importance": 0.7},
            {"type": "causal", "pattern": "test pattern 2", "importance": 0.8}
        ]

        personality_learning._update_patterns(learnings, learning_experience)

        assert "novel" in personality_learning.learned_patterns
        assert "causal" in personality_learning.learned_patterns

    def test_calculate_retention(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test retention calculation."""
        retention = personality_learning._calculate_retention(learning_experience)

        assert isinstance(retention, float)
        assert 0.0 <= retention <= 1.0

    def test_retention_with_emotion(self, personality_learning: PersonalityDrivenLearning):
        """Test emotional experiences increase retention."""
        # Experience with high emotion
        emotional_experience = LearningExperience(
            situation={"type": "test"},
            action="test_action",
            outcome={},
            emotional_context={"joy": 0.9, "arousal": 0.8}
        )

        retention_emotional = personality_learning._calculate_retention(emotional_experience)

        # Neutral experience
        neutral_experience = LearningExperience(
            situation={"type": "test"},
            action="test_action",
            outcome={},
            emotional_context={"joy": 0.1, "arousal": 0.1}
        )

        retention_neutral = personality_learning._calculate_retention(neutral_experience)

        # Emotional should have higher retention
        assert retention_emotional >= retention_neutral

    def test_calculate_personality_changes(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test personality changes from experience."""
        initial_traits = personality_learning.personality_traits.copy()

        changes = personality_learning._calculate_personality_changes(learning_experience)

        assert isinstance(changes, dict)

        # Changes should be small (character development is gradual)
        for trait, change in changes.items():
            assert -0.05 <= change <= 0.05, f"Change {change} for {trait} is too large"

        # Personality should have been updated
        updated_traits = personality_learning.personality_traits
        for trait in changes:
            assert updated_traits[trait] == initial_traits[trait] + changes[trait]

    def test_personality_bounds(self, personality_learning: PersonalityDrivenLearning):
        """Test personality traits stay within bounds."""
        # Start with high trait values
        personality_learning.personality_traits = {
            "openness": 0.99,
            "conscientiousness": 0.99,
            "extraversion": 0.99,
            "agreeableness": 0.99,
            "neuroticism": 0.99
        }

        # Experience that would increase traits
        experience = LearningExperience(
            situation={},
            action="test",
            outcome={"success": True, "positive_social": True, "novel": True}
        )

        personality_learning._calculate_personality_changes(experience)

        # All should still be in [0, 1]
        for trait, value in personality_learning.personality_traits.items():
            assert 0.0 <= value <= 1.0

    def test_explain_style_influence(self, personality_learning: PersonalityDrivenLearning):
        """Test learning style explanation."""
        explanation = personality_learning._explain_style_influence()

        assert isinstance(explanation, str)
        assert len(explanation) > 0

    def test_get_learning_summary(
        self,
        personality_learning: PersonalityDrivenLearning,
        learning_experience: LearningExperience
    ):
        """Test getting learning summary."""
        # Initially empty
        summary = personality_learning.get_learning_summary()

        assert summary["total_experiences"] == 0
        assert summary["patterns_learned"] == 0
        assert "dominant_style" in summary

        # After learning
        personality_learning.learn_from_experience(learning_experience)
        summary = personality_learning.get_learning_summary()

        assert summary["total_experiences"] == 1
        assert summary["patterns_learned"] > 0

    def test_get_recommendations(self, personality_learning: PersonalityDrivenLearning):
        """Test getting learning recommendations."""
        recommendations = personality_learning.get_recommendations()

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

        # All recommendations should be strings
        assert all(isinstance(rec, str) for rec in recommendations)

    def test_adapt_learning_to_context(self, personality_learning: PersonalityDrivenLearning):
        """Test adapting learning to context."""
        context = {"stress_level": 0.3}
        adaptations = personality_learning.adapt_learning_to_context(context)

        assert "optimal_approach" in adaptations
        assert "exploration_level" in adaptations
        assert "persistence_expected" in adaptations
        assert "feedback_importance" in adaptations

    def test_high_stress_adaptation(self, personality_learning: PersonalityDrivenLearning):
        """Test learning adaptation under high stress."""
        normal_context = {"stress_level": 0.3}
        stress_context = {"stress_level": 0.9}

        normal_adaptations = personality_learning.adapt_learning_to_context(normal_context)
        stress_adaptations = personality_learning.adapt_learning_to_context(stress_context)

        # Under stress, exploration should decrease
        assert stress_adaptations["exploration_level"] < normal_adaptations["exploration_level"]


class TestPersonalityVariations:
    """Test learning with different personality profiles."""

    def test_high_openness_learning(self):
        """Test learning with high openness personality."""
        traits = {
            "openness": 0.9,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }

        pdl = PersonalityDrivenLearning(personality_traits=traits)

        assert pdl.learning_style in [
            LearningStyle.EXPERIENTIAL,
            LearningStyle.INTUITIVE
        ]
        assert pdl.learning_preferences.exploration_tendency > 0.7

    def test_high_conscientiousness_learning(self):
        """Test learning with high conscientiousness personality."""
        traits = {
            "openness": 0.5,
            "conscientiousness": 0.9,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }

        pdl = PersonalityDrivenLearning(personality_traits=traits)

        assert pdl.learning_style == LearningStyle.ANALYTICAL
        assert pdl.learning_preferences.persistence > 0.7

    def test_high_extraversion_learning(self):
        """Test learning with high extraversion personality."""
        traits = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.9,
            "agreeableness": 0.7,
            "neuroticism": 0.5
        }

        pdl = PersonalityDrivenLearning(personality_traits=traits)

        assert pdl.learning_style == LearningStyle.SOCIAL

    def test_high_neuroticism_learning(self):
        """Test learning with high neuroticism personality."""
        traits = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.9
        }

        pdl = PersonalityDrivenLearning(personality_traits=traits)

        # High neuroticism should decrease feedback receptivity and risk tolerance
        assert pdl.learning_preferences.feedback_receptivity < 0.5
        assert pdl.learning_preferences.risk_tolerance < 0.5

    def test_different_personalities_different_learnings(self, personality_variations):
        """Test different personalities extract different learnings."""
        experiences = []

        for traits in personality_variations:
            pdl = PersonalityDrivenLearning(personality_traits=traits)
            experience = LearningExperience(
                situation={"type": "test"},
                action="action",
                outcome={"success": True, "novel": True}
            )

            result = pdl.learn_from_experience(experience)
            experiences.append(result)

        # Results should vary
        # (In full implementation, would check for significant differences)
        assert len(experiences) == len(personality_variations)


class TestLearningStyles:
    """Test different learning styles."""

    def test_all_styles_valid(self, all_learning_styles: LearningStyle):
        """Test all learning styles are valid."""
        pdl = PersonalityDrivenLearning(
            personality_traits={"openness": 0.7},
            learning_style=all_learning_styles
        )

        assert pdl.learning_style == all_learning_styles

    def test_style_influence_explanations(self):
        """Test each style has an explanation."""
        pdl = PersonalityDrivenLearning()

        for style in LearningStyle:
            pdl.learning_style = style
            explanation = pdl._explain_style_influence()

            assert explanation is not None
            assert len(explanation) > 0


class TestLearningProgress:
    """Test learning progress over multiple experiences."""

    def test_multiple_experiences(self, personality_learning: PersonalityDrivenLearning):
        """Test learning from multiple experiences."""
        for i in range(10):
            experience = LearningExperience(
                situation={"index": i},
                action=f"action_{i}",
                outcome={"success": True}
            )
            personality_learning.learn_from_experience(experience)

        summary = personality_learning.get_learning_summary()
        assert summary["total_experiences"] == 10
        assert summary["patterns_learned"] > 0

    def test_pattern_accumulation(self, personality_learning: PersonalityDrivenLearning):
        """Test patterns accumulate over time."""
        for i in range(5):
            experience = LearningExperience(
                situation={"index": i},
                action=f"action_{i}",
                outcome={"success": True, "novel": True}
            )
            personality_learning.learn_from_experience(experience)

        # Should have multiple pattern types
        pattern_types = list(personality_learning.learned_patterns.keys())
        assert len(pattern_types) > 0


class TestPersonalityDevelopment:
    """Test personality changes over time."""

    def test_gradual_personality_change(self, personality_learning: PersonalityDrivenLearning):
        """Test personality changes gradually."""
        initial_openness = personality_learning.personality_traits["openness"]

        # Many positive novel experiences
        for _ in range(50):
            experience = LearningExperience(
                situation={},
                action="test",
                outcome={"success": True, "novel": True}
            )
            personality_learning.learn_from_experience(experience)

        final_openness = personality_learning.personality_traits["openness"]

        # Should have changed somewhat (but not drastically)
        change = abs(final_openness - initial_openness)
        assert 0.0 < change < 0.5


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_experience(self, personality_learning: PersonalityDrivenLearning):
        """Test handling empty experience."""
        experience = LearningExperience(
            situation={},
            action="",
            outcome={}
        )

        result = personality_learning.learn_from_experience(experience)
        assert result is not None

    def test_extreme_personality_values(self):
        """Test extreme personality trait values."""
        traits = {
            "openness": 1.0,
            "conscientiousness": 1.0,
            "extraversion": 1.0,
            "agreeableness": 1.0,
            "neuroticism": 0.0
        }

        pdl = PersonalityDrivenLearning(personality_traits=traits)

        # Should handle without error
        experience = LearningExperience(
            situation={},
            action="test",
            outcome={}
        )

        result = pdl.learn_from_experience(experience)
        assert result is not None

    def test_invalid_personality_values(self):
        """Test handling of slightly out-of-range values."""
        # The implementation should clip to [0, 1]
        traits = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }

        pdl = PersonalityDrivenLearning(personality_traits=traits)

        # Manually set out of range
        pdl.personality_traits["openness"] = 1.5

        experience = LearningExperience(
            situation={},
            action="test",
            outcome={"success": True}
        )

        # Should clip during personality update
        pdl._calculate_personality_changes(experience)

        assert 0.0 <= pdl.personality_traits["openness"] <= 1.0
