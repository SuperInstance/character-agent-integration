"""
Personality-Driven Learning

Enables agents to learn in ways consistent with their personality.
Different personality traits lead to different learning patterns and preferences.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


class LearningStyle(Enum):
    """Learning style preferences based on personality."""
    EXPERIENTIAL = "experiential"  # Learn by doing
    ANALYTICAL = "analytical"  # Learn by analyzing
    SOCIAL = "social"  # Learn from others
    OBSERVATIONAL = "observational"  # Learn by watching
    THEORETICAL = "theoretical"  # Learn by studying
    INTUITIVE = "intuitive"  # Learn by insight


@dataclass
class LearningPreference:
    """Preferences for how a character learns best."""
    style: LearningStyle
    feedback_receptivity: float  # 0.0 to 1.0
    exploration_tendency: float  # 0.0 to 1.0
    persistence: float  # 0.0 to 1.0
    adaptability: float  # 0.0 to 1.0
    risk_tolerance: float  # 0.0 to 1.0


@dataclass
class LearningExperience:
    """A learning experience for the character."""
    situation: Dict[str, Any]
    action: str
    outcome: Dict[str, Any]
    emotional_context: Optional[Dict[str, float]] = None
    personality_context: Optional[Dict[str, float]] = None
    timestamp: float = field(default_factory=lambda: __import__("time").time())


class PersonalityDrivenLearning:
    """
    Manages learning that is influenced by personality traits.

    Characters with different personalities will:
    - Learn different things from the same experiences
    - Have different learning rates and styles
    - Prefer different types of learning experiences
    - Retain and apply knowledge differently
    """

    def __init__(
        self,
        personality_traits: Optional[Dict[str, float]] = None,
        learning_style: Optional[LearningStyle] = None
    ):
        """
        Initialize personality-driven learning.

        Args:
            personality_traits: Big Five personality traits (openness, conscientiousness,
                               extraversion, agreeableness, neuroticism)
            learning_style: Preferred learning style
        """
        self.personality_traits = personality_traits or self._default_personality()
        self.learning_style = learning_style or self._determine_learning_style()
        self.learning_preferences = self._calculate_preferences()
        self.learning_history: List[LearningExperience] = []
        self.learned_patterns: Dict[str, Any] = {}

    def _default_personality(self) -> Dict[str, float]:
        """Get default personality traits (mid-range)."""
        return {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }

    def _determine_learning_style(self) -> LearningStyle:
        """
        Determine learning style from personality traits.

        Returns:
            LearningStyle based on personality
        """
        openness = self.personality_traits.get("openness", 0.5)
        extraversion = self.personality_traits.get("extraversion", 0.5)
        conscientiousness = self.personality_traits.get("conscientiousness", 0.5)

        # High openness + high extraversion = experiential
        if openness > 0.6 and extraversion > 0.6:
            return LearningStyle.EXPERIENTIAL

        # High conscientiousness = analytical
        if conscientiousness > 0.7:
            return LearningStyle.ANALYTICAL

        # High extraversion + high agreeableness = social
        if extraversion > 0.6 and self.personality_traits.get("agreeableness", 0.5) > 0.6:
            return LearningStyle.SOCIAL

        # High openness = intuitive
        if openness > 0.7:
            return LearningStyle.INTUITIVE

        # Default: observational
        return LearningStyle.OBSERVATIONAL

    def _calculate_preferences(self) -> LearningPreference:
        """
        Calculate learning preferences from personality.

        Returns:
            LearningPreference object
        """
        openness = self.personality_traits.get("openness", 0.5)
        conscientiousness = self.personality_traits.get("conscientiousness", 0.5)
        extraversion = self.personality_traits.get("extraversion", 0.5)
        neuroticism = self.personality_traits.get("neuroticism", 0.5)
        agreeableness = self.personality_traits.get("agreeableness", 0.5)

        return LearningPreference(
            style=self.learning_style,
            feedback_receptivity=1.0 - neuroticism,  # Low neuroticism = more receptive
            exploration_tendency=openness,  # High openness = more exploration
            persistence=conscientiousness,  # High conscientiousness = more persistent
            adaptability=openness,  # High openness = more adaptable
            risk_tolerance=1.0 - neuroticism  # Low neuroticism = more risk-tolerant
        )

    def learn_from_experience(
        self,
        experience: LearningExperience
    ) -> Dict[str, Any]:
        """
        Learn from an experience in a personality-driven way.

        Args:
            experience: Learning experience to process

        Returns:
            Learning results and updates
        """
        # Record the experience
        self.learning_history.append(experience)

        # Extract learnings based on personality
        learnings = self._extract_learnings(experience)

        # Update learned patterns
        self._update_patterns(learnings, experience)

        # Determine retention
        retention = self._calculate_retention(experience)

        # Calculate personality changes (characters can grow)
        personality_changes = self._calculate_personality_changes(experience)

        return {
            "learnings": learnings,
            "retention": retention,
            "personality_changes": personality_changes,
            "learning_style_influence": self._explain_style_influence()
        }

    def _extract_learnings(
        self,
        experience: LearningExperience
    ) -> List[Dict[str, Any]]:
        """
        Extract learnings based on personality.

        Args:
            experience: Learning experience

        Returns:
            List of learnings extracted
        """
        learnings = []

        # Different personalities notice different things
        if self.personality_traits.get("openness", 0.5) > 0.6:
            # Open personalities notice novel patterns
            novel_learnings = self._find_novel_patterns(experience)
            learnings.extend(novel_learnings)

        if self.personality_traits.get("conscientiousness", 0.5) > 0.6:
            # Conscientious personalities note cause-effect relationships
            causal_learnings = self._find_causal_patterns(experience)
            learnings.extend(causal_learnings)

        if self.personality_traits.get("agreeableness", 0.5) > 0.6:
            # Agreeable personalities note social dynamics
            social_learnings = self._find_social_patterns(experience)
            learnings.extend(social_learnings)

        return learnings

    def _find_novel_patterns(self, experience: LearningExperience) -> List[Dict[str, Any]]:
        """Find novel patterns in experience."""
        return [{
            "type": "novel",
            "pattern": "new approach discovered",
            "importance": self.personality_traits.get("openness", 0.5)
        }]

    def _find_causal_patterns(self, experience: LearningExperience) -> List[Dict[str, Any]]:
        """Find cause-effect patterns."""
        return [{
            "type": "causal",
            "pattern": "action led to outcome",
            "importance": self.personality_traits.get("conscientiousness", 0.5)
        }]

    def _find_social_patterns(self, experience: LearningExperience) -> List[Dict[str, Any]]:
        """Find social patterns."""
        return [{
            "type": "social",
            "pattern": "interaction dynamics observed",
            "importance": self.personality_traits.get("agreeableness", 0.5)
        }]

    def _update_patterns(
        self,
        learnings: List[Dict[str, Any]],
        experience: LearningExperience
    ) -> None:
        """Update learned patterns."""
        for learning in learnings:
            pattern_type = learning["type"]
            pattern = learning["pattern"]
            importance = learning["importance"]

            if pattern_type not in self.learned_patterns:
                self.learned_patterns[pattern_type] = []

            self.learned_patterns[pattern_type].append({
                "pattern": pattern,
                "importance": importance,
                "timestamp": experience.timestamp,
                "context": experience.situation
            })

    def _calculate_retention(self, experience: LearningExperience) -> float:
        """
        Calculate how well this experience will be retained.

        Args:
            experience: Learning experience

        Returns:
            Retention score from 0.0 to 1.0
        """
        # Base retention
        retention = 0.5

        # Emotional intensity increases retention
        if experience.emotional_context:
            emotional_intensity = sum(
                abs(v) for v in experience.emotional_context.values()
            ) / len(experience.emotional_context)
            retention += emotional_intensity * 0.3

        # Personality influence on retention
        conscientiousness = self.personality_traits.get("conscientiousness", 0.5)
        retention += conscientiousness * 0.2

        return min(1.0, max(0.0, retention))

    def _calculate_personality_changes(
        self,
        experience: LearningExperience
    ) -> Dict[str, float]:
        """
        Calculate subtle personality changes from the experience.

        Characters can grow and evolve through experiences.

        Args:
            experience: Learning experience

        Returns:
            Dictionary of personality trait changes
        """
        changes = {}

        # Success can increase confidence (lower neuroticism)
        if experience.outcome.get("success", False):
            changes["neuroticism"] = -0.01

        # Positive social experiences can increase agreeableness
        if experience.outcome.get("positive_social", False):
            changes["agreeableness"] = 0.01

        # Novel experiences can increase openness
        if experience.outcome.get("novel", False):
            changes["openness"] = 0.01

        # Apply changes with bounds checking
        for trait, change in changes.items():
            current = self.personality_traits.get(trait, 0.5)
            new_value = max(0.0, min(1.0, current + change))
            self.personality_traits[trait] = new_value

        return changes

    def _explain_style_influence(self) -> str:
        """Explain how learning style influenced learning."""
        explanations = {
            LearningStyle.EXPERIENTIAL: "You learn best by diving in and trying things directly.",
            LearningStyle.ANALYTICAL: "You learn by carefully analyzing situations and outcomes.",
            LearningStyle.SOCIAL: "You learn best through interactions with others.",
            LearningStyle.OBSERVATIONAL: "You learn by watching and observing before acting.",
            LearningStyle.THEORETICAL: "You learn by studying underlying principles.",
            LearningStyle.INTUITIVE: "You learn through insights and sudden realizations."
        }
        return explanations.get(self.learning_style, "You learn through a mix of approaches.")

    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress."""
        total_experiences = len(self.learning_history)

        if total_experiences == 0:
            return {
                "total_experiences": 0,
                "patterns_learned": 0,
                "dominant_style": self.learning_style.value
            }

        patterns_learned = sum(
            len(patterns)
            for patterns in self.learned_patterns.values()
        )

        return {
            "total_experiences": total_experiences,
            "patterns_learned": patterns_learned,
            "dominant_style": self.learning_style.value,
            "pattern_types": list(self.learned_patterns.keys()),
            "personality_state": self.personality_traits.copy()
        }

    def get_recommendations(self) -> List[str]:
        """
        Get learning recommendations based on personality.

        Returns:
            List of personalized learning recommendations
        """
        recommendations = []

        # Based on learning style
        if self.learning_style == LearningStyle.EXPERIENTIAL:
            recommendations.append("Try new hands-on experiences to learn effectively.")
        elif self.learning_style == LearningStyle.ANALYTICAL:
            recommendations.append("Take time to analyze situations before acting.")
        elif self.learning_style == LearningStyle.SOCIAL:
            recommendations.append("Seek out collaborative learning opportunities.")

        # Based on traits
        if self.personality_traits.get("openness", 0.5) < 0.4:
            recommendations.append("Consider exploring unfamiliar situations to grow.")

        if self.personality_traits.get("conscientiousness", 0.5) < 0.4:
            recommendations.append("Practice reflecting on cause-and-effect relationships.")

        return recommendations

    def adapt_learning_to_context(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adapt learning approach based on context.

        Args:
            context: Current context

        Returns:
            Adaptation recommendations
        """
        adaptations = {
            "optimal_approach": self.learning_style.value,
            "exploration_level": self.learning_preferences.exploration_tendency,
            "persistence_expected": self.learning_preferences.persistence,
            "feedback_importance": self.learning_preferences.feedback_receptivity
        }

        # Context-specific adaptations
        if context.get("stress_level", 0) > 0.7:
            # Under stress, prefer familiar approaches
            adaptations["exploration_level"] *= 0.5
            adaptations["optimal_approach"] = LearningStyle.OBSERVATIONAL.value

        return adaptations
