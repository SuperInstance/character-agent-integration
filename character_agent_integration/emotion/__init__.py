"""
Emotional Intelligence

Provides emotional awareness and response capabilities for agents.
Enables emotionally intelligent interactions and responses.
"""

from .intelligence import EmotionalIntelligence
from .state import EmotionalState
from .response import EmotionalResponse

__all__ = [
    "EmotionalIntelligence",
    "EmotionalState",
    "EmotionalResponse"
]
