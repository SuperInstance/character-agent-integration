"""
Pytest configuration and fixtures for character-agent-integration tests.
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import Mock, MagicMock

from character_agent_integration.agent import (
    AgentRole,
    RoleType,
    RoleCapabilities,
    RoleContext
)
from character_agent_integration.agent.roles import (
    ConversationPartner,
    Mentor,
    Collaborator,
    Analyst,
    Creator,
    Companion,
    Teacher,
    Leader
)
from character_agent_integration.memory import (
    MemoryAugmentedDecisions,
    DecisionContext,
    DecisionStrategy
)
from character_agent_integration.personality import (
    PersonalityDrivenLearning,
    LearningStyle,
    LearningExperience
)
from character_agent_integration.emotion import (
    EmotionalIntelligence,
    EmotionalState,
    EmotionalContext
)
from character_agent_integration.integration import (
    CharacterAgentIntegration,
    AgentConfig,
    create_character_agent
)


# =============================================================================
# Agent Role Fixtures
# =============================================================================

@pytest.fixture
def sample_personality() -> Dict[str, float]:
    """Sample personality traits (Big Five)."""
    return {
        "openness": 0.8,
        "conscientiousness": 0.7,
        "extraversion": 0.6,
        "agreeableness": 0.7,
        "neuroticism": 0.3
    }


@pytest.fixture
def sample_emotions() -> Dict[str, float]:
    """Sample emotional baseline."""
    return {
        "joy": 0.5,
        "sadness": 0.1,
        "anger": 0.1,
        "fear": 0.1,
        "surprise": 0.2,
        "disgust": 0.0,
        "anticipation": 0.3,
        "trust": 0.6
    }


@pytest.fixture
def conversation_partner() -> ConversationPartner:
    """Conversation partner agent role."""
    return ConversationPartner()


@pytest.fixture
def mentor() -> Mentor:
    """Mentor agent role."""
    return Mentor()


@pytest.fixture
def collaborator() -> Collaborator:
    """Collaborator agent role."""
    return Collaborator()


@pytest.fixture
def analyst() -> Analyst:
    """Analyst agent role."""
    return Analyst()


@pytest.fixture
def creator() -> Creator:
    """Creator agent role."""
    return Creator()


@pytest.fixture
def companion() -> Companion:
    """Companion agent role."""
    return Companion()


@pytest.fixture
def teacher() -> Teacher:
    """Teacher agent role."""
    return Teacher()


@pytest.fixture
def leader() -> Leader:
    """Leader agent role."""
    return Leader()


@pytest.fixture(params=[
    "conversation_partner",
    "mentor",
    "collaborator",
    "analyst",
    "creator",
    "companion",
    "teacher",
    "leader"
])
def all_agent_roles(request) -> AgentRole:
    """Parametrized fixture for all agent roles."""
    role_instances = {
        "conversation_partner": ConversationPartner(),
        "mentor": Mentor(),
        "collaborator": Collaborator(),
        "analyst": Analyst(),
        "creator": Creator(),
        "companion": Companion(),
        "teacher": Teacher(),
        "leader": Leader()
    }
    return role_instances[request.param]


@pytest.fixture
def role_context() -> RoleContext:
    """Sample role context."""
    context = RoleContext()
    context.add_interaction({
        "topic": "test topic",
        "timestamp": 1234567890.0
    })
    context.current_task = "Complete testing"
    context.emotional_state = {"joy": 0.7}
    context.personality_traits = {"openness": 0.8}
    context.environmental_factors = {"setting": "laboratory"}
    return context


# =============================================================================
# Memory System Fixtures
# =============================================================================

@pytest.fixture
def decision_context() -> DecisionContext:
    """Sample decision context."""
    return DecisionContext(
        current_situation={
            "input": "test input",
            "context": "testing scenario"
        },
        available_actions=[
            "respond_helpfully",
            "ask_clarifying_question",
            "provide_information"
        ],
        constraints={"time_limit": 60},
        goals=["assist_user", "provide_value"],
        emotional_state={"joy": 0.5},
        personality_traits={"openness": 0.7}
    )


@pytest.fixture
def mock_memory_system():
    """Mock hierarchical memory system."""
    mock_memory = Mock()
    mock_memory.retrieve = Mock(return_value=[
        {
            "content": "past experience",
            "importance": 0.8,
            "timestamp": 1234567890.0
        }
    ])
    mock_memory.store_episodic = Mock()
    mock_memory.store_procedural = Mock()
    mock_memory.store_semantic = Mock()
    return mock_memory


@pytest.fixture
def memory_decisions(mock_memory_system) -> MemoryAugmentedDecisions:
    """Memory-augmented decision system."""
    return MemoryAugmentedDecisions(
        strategy=DecisionStrategy.HYBRID,
        memory_system=mock_memory_system
    )


@pytest.fixture(params=[
    DecisionStrategy.EXPERIENCE_BASED,
    DecisionStrategy.PATTERN_RECOGNITION,
    DecisionStrategy.CONTEXTUAL,
    DecisionStrategy.HYBRID
])
def all_decision_strategies(request) -> DecisionStrategy:
    """Parametrized fixture for all decision strategies."""
    return request.param


# =============================================================================
# Personality Fixtures
# =============================================================================

@pytest.fixture
def learning_experience() -> LearningExperience:
    """Sample learning experience."""
    return LearningExperience(
        situation={"type": "conversation", "topic": "AI"},
        action="provided_helpful_response",
        outcome={"success": True, "positive_social": True, "novel": True},
        emotional_context={"joy": 0.7, "anticipation": 0.5},
        personality_context={"openness": 0.8, "agreeableness": 0.7}
    )


@pytest.fixture(params=[
    LearningStyle.EXPERIENTIAL,
    LearningStyle.ANALYTICAL,
    LearningStyle.SOCIAL,
    LearningStyle.OBSERVATIONAL,
    LearningStyle.THEORETICAL,
    LearningStyle.INTUITIVE
])
def all_learning_styles(request) -> LearningStyle:
    """Parametrized fixture for all learning styles."""
    return request.param


@pytest.fixture
def personality_learning(sample_personality) -> PersonalityDrivenLearning:
    """Personality-driven learning system."""
    return PersonalityDrivenLearning(
        personality_traits=sample_personality,
        learning_style=LearningStyle.EXPERIENTIAL
    )


@pytest.fixture
def personality_variations() -> List[Dict[str, float]]:
    """Various personality profiles for testing."""
    return [
        {"openness": 0.9, "conscientiousness": 0.5, "extraversion": 0.5,
         "agreeableness": 0.5, "neuroticism": 0.5},  # High openness
        {"openness": 0.5, "conscientiousness": 0.9, "extraversion": 0.5,
         "agreeableness": 0.5, "neuroticism": 0.5},  # High conscientiousness
        {"openness": 0.5, "conscientiousness": 0.5, "extraversion": 0.9,
         "agreeableness": 0.5, "neuroticism": 0.5},  # High extraversion
        {"openness": 0.5, "conscientiousness": 0.5, "extraversion": 0.5,
         "agreeableness": 0.9, "neuroticism": 0.5},  # High agreeableness
        {"openness": 0.5, "conscientiousness": 0.5, "extraversion": 0.5,
         "agreeableness": 0.5, "neuroticism": 0.9},  # High neuroticism
    ]


# =============================================================================
# Emotional Intelligence Fixtures
# =============================================================================

@pytest.fixture
def emotional_intelligence() -> EmotionalIntelligence:
    """Emotional intelligence system."""
    return EmotionalIntelligence(empathy_level=0.8)


@pytest.fixture
def emotional_context() -> EmotionalContext:
    """Sample emotional context."""
    return EmotionalContext(
        speaker_emotion={"joy": 0.7, "anticipation": 0.5},
        content_emotion={"joy": 0.6, "trust": 0.5},
        situational_emotion={"joy": 0.4},
        relationship_context={"closeness": 0.8}
    )


@pytest.fixture
def emotional_state() -> EmotionalState:
    """Sample emotional state."""
    state = EmotionalState()
    state.specific_emotions = {"joy": 0.7, "anticipation": 0.5}
    state.update_from_specific_emotions()
    return state


# =============================================================================
# Integration Fixtures
# =============================================================================

@pytest.fixture
def agent_config(sample_personality, sample_emotions) -> AgentConfig:
    """Sample agent configuration."""
    return AgentConfig(
        agent_role=RoleType.MENTOR,
        personality_traits=sample_personality,
        emotional_baseline=sample_emotions,
        decision_strategy=DecisionStrategy.HYBRID,
        empathy_level=0.8
    )


@pytest.fixture
def character_agent(agent_config, mock_memory_system) -> CharacterAgentIntegration:
    """Fully configured character agent."""
    return CharacterAgentIntegration(
        config=agent_config,
        memory_system=mock_memory_system
    )


@pytest.fixture
def interaction_context() -> Dict[str, Any]:
    """Sample interaction context."""
    return {
        "user_id": "test_user_123",
        "session_id": "test_session_456",
        "timestamp": 1234567890.0,
        "topic": "career_advice",
        "constraints": {"time_limit": 300},
        "goals": ["provide_guidance", "be_supportive"]
    }


# =============================================================================
# Mock Dependencies
# =============================================================================

@pytest.fixture
def mock_character_library():
    """Mock character-library dependency."""
    mock_char = Mock()
    mock_char.get_personality = Mock(return_value={
        "openness": 0.7,
        "conscientiousness": 0.7,
        "extraversion": 0.6,
        "agreeableness": 0.7,
        "neuroticism": 0.3
    })
    mock_char.get_emotions = Mock(return_value={
        "joy": 0.5, "sadness": 0.1, "anger": 0.1, "fear": 0.1,
        "surprise": 0.2, "disgust": 0.0, "anticipation": 0.3, "trust": 0.6
    })
    return mock_char


@pytest.fixture
def mock_hierarchical_memory():
    """Mock hierarchical-memory dependency."""
    mock_memory = Mock()
    mock_memory.retrieve = Mock(return_value=[])
    mock_memory.store_episodic = Mock()
    mock_memory.store_semantic = Mock()
    mock_memory.store_procedural = Mock()
    mock_memory.store_working = Mock()
    mock_memory.get_episodic = Mock(return_value=[])
    mock_memory.get_semantic = Mock(return_value={})
    mock_memory.get_procedural = Mock(return_value={})
    return mock_memory


# =============================================================================
# Test Data Fixtures
# =============================================================================

@pytest.fixture
def sample_inputs() -> List[str]:
    """Sample user inputs for testing."""
    return [
        "I need advice on my career path",
        "Can you help me understand this concept?",
        "I'm feeling overwhelmed with my workload",
        "Let's work together on this project",
        "What do you think about this idea?",
        "I'm so happy about my promotion!",
        "This situation makes me really angry",
        "I'm worried about the upcoming deadline"
    ]


@pytest.fixture
def sample_outputs() -> List[str]:
    """Sample expected response patterns."""
    return [
        "guidance",
        "explanation",
        "support",
        "collaboration",
        "creative",
        "enthusiasm",
        "understanding",
        "reassurance"
    ]


# =============================================================================
# Performance Fixtures
# =============================================================================

@pytest.fixture
def performance_config() -> Dict[str, Any]:
    """Configuration for performance testing."""
    return {
        "num_interactions": 100,
        "max_response_time": 1.0,  # seconds
        "max_memory_usage": 100 * 1024 * 1024  # 100 MB
    }
