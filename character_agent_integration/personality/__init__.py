"""
Personality-Driven Learning

Integrates personality models into agent learning and behavior.
Enables characters to learn and evolve based on their personality traits.
"""

from .learning import PersonalityDrivenLearning, LearningStyle
from .influence import PersonalityInfluence, InfluenceMode
from .development import CharacterDevelopment, DevelopmentMilestone

__all__ = [
    "PersonalityDrivenLearning",
    "LearningStyle",
    "PersonalityInfluence",
    "InfluenceMode",
    "CharacterDevelopment",
    "DevelopmentMilestone"
]
