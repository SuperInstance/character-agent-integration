"""
Character-Agent Integration System

A comprehensive integration layer connecting character personalities with AI agent architecture.
Provides memory-augmented decision making, personality-driven learning, and emotional intelligence.

Author: SuperInstance Team
Version: 1.0.0
License: MIT
"""

from .agent import (
    AgentRole,
    ConversationPartner,
    Mentor,
    Collaborator,
    Analyst,
    Creator,
    Companion,
    Teacher,
    Leader
)

from .memory import (
    MemoryAugmentedDecisions,
    DecisionStrategy,
    ContextualMemory,
    MemoryRetrievalStrategy
)

from .personality import (
    PersonalityDrivenLearning,
    PersonalityInfluence,
    CharacterDevelopment
)

from .emotion import (
    EmotionalIntelligence,
    EmotionalState,
    EmotionalResponse
)

from .integration import (
    CharacterAgentIntegration,
    AgentConfig,
    IntegrationResult,
    create_character_agent,
    RoleType
)

__version__ = "1.0.0"
__all__ = [
    # Factory function
    "create_character_agent",
    # Agent Roles
    "AgentRole",
    "RoleType",
    "ConversationPartner",
    "Mentor",
    "Collaborator",
    "Analyst",
    "Creator",
    "Companion",
    "Teacher",
    "Leader",
    # Memory
    "MemoryAugmentedDecisions",
    "DecisionStrategy",
    "ContextualMemory",
    "MemoryRetrievalStrategy",
    # Personality
    "PersonalityDrivenLearning",
    "PersonalityInfluence",
    "CharacterDevelopment",
    # Emotion
    "EmotionalIntelligence",
    "EmotionalState",
    "EmotionalResponse",
    # Integration
    "CharacterAgentIntegration",
    "AgentConfig",
    "IntegrationResult"
]
