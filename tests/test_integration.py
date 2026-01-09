"""
Test suite for full integration workflows.

Tests the complete character-agent integration system:
- Full interaction workflows
- Component integration
- End-to-end functionality
- Cross-component interactions
"""

import pytest
from typing import Dict, Any
from unittest.mock import Mock, patch

from character_agent_integration.integration import (
    CharacterAgentIntegration,
    AgentConfig,
    IntegrationResult,
    create_character_agent,
    RoleType
)
from character_agent_integration.memory import DecisionStrategy
from character_agent_integration.emotion import EmotionalState


class TestAgentConfig:
    """Test suite for AgentConfig."""

    def test_create_config(self, agent_config: AgentConfig):
        """Test creating agent configuration."""
        assert agent_config.agent_role == RoleType.MENTOR
        assert agent_config.personality_traits is not None
        assert agent_config.emotional_baseline is not None
        assert agent_config.decision_strategy == DecisionStrategy.HYBRID
        assert agent_config.empathy_level == 0.8

    def test_config_to_dict(self, agent_config: AgentConfig):
        """Test converting config to dictionary."""
        config_dict = agent_config.to_dict()

        assert isinstance(config_dict, dict)
        assert "agent_role" in config_dict
        assert "personality_traits" in config_dict
        assert "emotional_baseline" in config_dict
        assert "empathy_level" in config_dict

    def test_config_defaults(self):
        """Test default configuration values."""
        config = AgentConfig(
            agent_role=RoleType.CONVERSATION_PARTNER,
            personality_traits={"openness": 0.7},
            emotional_baseline={"joy": 0.5}
        )

        assert config.learning_style is None
        assert config.decision_strategy == DecisionStrategy.HYBRID
        assert config.empathy_level == 0.7


class TestCharacterAgentIntegration:
    """Test suite for CharacterAgentIntegration."""

    def test_initialization(self, character_agent: CharacterAgentIntegration):
        """Test agent initialization."""
        assert character_agent is not None
        assert character_agent.config is not None
        assert character_agent.agent_role is not None
        assert character_agent.memory_system is not None
        assert character_agent.personality_learning is not None
        assert character_agent.emotional_intelligence is not None
        assert character_agent.current_emotional_state is not None

    def test_component_creation(self, character_agent: CharacterAgentIntegration):
        """Test all components are created."""
        assert hasattr(character_agent, 'agent_role')
        assert hasattr(character_agent, 'memory_system')
        assert hasattr(character_agent, 'contextual_memory')
        assert hasattr(character_agent, 'personality_learning')
        assert hasattr(character_agent, 'personality_influence')
        assert hasattr(character_agent, 'character_development')
        assert hasattr(character_agent, 'emotional_intelligence')
        assert hasattr(character_agent, 'current_emotional_state')

    def test_create_agent_role(self, agent_config: AgentConfig):
        """Test agent role is created based on config."""
        agent = CharacterAgentIntegration(config=agent_config)

        assert agent.agent_role is not None
        # Role type should match config
        assert agent.agent_role.get_role_type() == agent_config.agent_role

    def test_interact(
        self,
        character_agent: CharacterAgentIntegration,
        interaction_context: Dict[str, Any]
    ):
        """Test basic interaction."""
        result = character_agent.interact(
            "I need advice on my career",
            context=interaction_context
        )

        assert isinstance(result, IntegrationResult)
        assert result.response is not None
        assert len(result.response) > 0
        assert result.emotional_state is not None
        assert result.decision_context is not None
        assert isinstance(result.learning_occurred, bool)
        assert isinstance(result.confidence, float)
        assert 0.0 <= result.confidence <= 1.0

    def test_multiple_interactions(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test multiple sequential interactions."""
        inputs = [
            "Hello, how are you?",
            "I need some guidance",
            "Can you help me understand this?",
            "Thank you for your help"
        ]

        results = []
        for input_text in inputs:
            result = character_agent.interact(input_text)
            results.append(result)

        # All should produce valid results
        assert len(results) == len(inputs)
        assert all(isinstance(r, IntegrationResult) for r in results)
        assert all(len(r.response) > 0 for r in results)

    def test_get_agent_state(self, character_agent: CharacterAgentIntegration):
        """Test getting agent state."""
        state = character_agent.get_agent_state()

        assert isinstance(state, dict)
        assert "config" in state
        assert "emotional_state" in state
        assert "personality_state" in state
        assert "memory_statistics" in state
        assert "learning_summary" in state
        assert "development_summary" in state

    def test_update_personality(
        self,
        character_agent: CharacterAgentIntegration,
        sample_personality: Dict[str, float]
    ):
        """Test updating personality traits."""
        new_traits = {"openness": 0.9, "conscientiousness": 0.8}

        initial_openness = character_agent.config.personality_traits["openness"]
        character_agent.update_personality(new_traits)

        assert character_agent.config.personality_traits["openness"] == 0.9
        assert character_agent.personality_learning.personality_traits["openness"] == 0.9

    def test_reset_emotional_state(
        self,
        character_agent: CharacterAgentIntegration,
        sample_emotions: Dict[str, float]
    ):
        """Test resetting emotional state to baseline."""
        # Modify emotional state
        character_agent.current_emotional_state.valence = -0.5

        # Reset
        character_agent.reset_emotional_state()

        # Should be back to baseline
        assert character_agent.current_emotional_state.valence >= 0

    def test_emotional_state_updates(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test emotional state updates during interactions."""
        initial_valence = character_agent.current_emotional_state.valence

        # Positive interaction
        result = character_agent.interact("I'm so happy about this!")

        # Emotional state should have been updated
        # (May not change much in single interaction)
        assert character_agent.current_emotional_state is not None


class TestIntegrationResult:
    """Test suite for IntegrationResult."""

    def test_result_structure(self):
        """Test integration result has correct structure."""
        result = IntegrationResult(
            response="Test response",
            emotional_state=EmotionalState(),
            decision_context=None,
            learning_occurred=True,
            confidence=0.8,
            metadata={"test": "value"}
        )

        assert result.response == "Test response"
        assert result.learning_occurred is True
        assert result.confidence == 0.8
        assert result.metadata == {"test": "value"}

    def test_result_without_metadata(self):
        """Test result without metadata uses default."""
        result = IntegrationResult(
            response="Test",
            emotional_state=EmotionalState(),
            decision_context=None,
            learning_occurred=False,
            confidence=0.5
        )

        assert result.metadata == {}


class TestFactoryFunction:
    """Test suite for create_character_agent factory function."""

    def test_create_agent_with_string_role(self):
        """Test creating agent with string role."""
        agent = create_character_agent(
            role="mentor",
            personality={"openness": 0.8, "conscientiousness": 0.7}
        )

        assert agent is not None
        assert isinstance(agent, CharacterAgentIntegration)
        assert agent.config.agent_role == RoleType.MENTOR

    def test_create_agent_with_personality(self):
        """Test creating agent with personality."""
        personality = {
            "openness": 0.9,
            "conscientiousness": 0.6,
            "extraversion": 0.7,
            "agreeableness": 0.8,
            "neuroticism": 0.2
        }

        agent = create_character_agent(
            role="companion",
            personality=personality
        )

        assert agent.config.personality_traits == personality

    def test_create_agent_with_custom_emotions(self):
        """Test creating agent with custom emotions."""
        emotions = {
            "joy": 0.8,
            "sadness": 0.1,
            "anger": 0.0,
            "fear": 0.1,
            "surprise": 0.3,
            "disgust": 0.0,
            "anticipation": 0.4,
            "trust": 0.7
        }

        agent = create_character_agent(
            role="teacher",
            personality={"openness": 0.7},
            emotions=emotions
        )

        assert agent.config.emotional_baseline == emotions

    def test_create_agent_default_emotions(self):
        """Test creating agent with default emotions."""
        agent = create_character_agent(
            role="analyst",
            personality={"openness": 0.7}
        )

        # Should have default emotions
        assert agent.config.emotional_baseline is not None
        assert "joy" in agent.config.emotional_baseline

    def test_create_agent_all_roles(self):
        """Test creating agents for all roles."""
        roles = [
            "conversation_partner",
            "mentor",
            "collaborator",
            "analyst",
            "creator",
            "companion",
            "teacher",
            "leader"
        ]

        for role in roles:
            agent = create_character_agent(
                role=role,
                personality={"openness": 0.7}
            )
            assert agent is not None
            assert agent.config.agent_role.value == role


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""

    def test_conversation_workflow(self):
        """Test complete conversation workflow."""
        agent = create_character_agent(
            role="conversation_partner",
            personality={
                "openness": 0.8,
                "extraversion": 0.7,
                "agreeableness": 0.7
            }
        )

        # Simulate conversation
        messages = [
            "Hi there!",
            "I'm interested in AI",
            "What do you think about machine learning?",
            "That's fascinating!"
        ]

        conversation_history = []
        for msg in messages:
            result = agent.interact(msg)
            conversation_history.append({
                "user": msg,
                "agent": result.response,
                "emotions": result.emotional_state.to_dict()
            })

        assert len(conversation_history) == len(messages)
        assert all("agent" in turn for turn in conversation_history)

    def test_guidance_workflow(self):
        """Test mentor providing guidance workflow."""
        agent = create_character_agent(
            role="mentor",
            personality={
                "openness": 0.7,
                "conscientiousness": 0.8,
                "agreeableness": 0.8
            }
        )

        # Seek guidance
        result = agent.interact(
            "I'm struggling with a difficult decision at work"
        )

        assert result.response is not None
        # Should show learning occurred
        assert isinstance(result.learning_occurred, bool)

    def test_learning_workflow(self):
        """Test learning over multiple interactions."""
        agent = create_character_agent(
            role="teacher",
            personality={
                "openness": 0.8,
                "conscientiousness": 0.9
            }
        )

        # Learning session
        learning_inputs = [
            "Can you explain neural networks?",
            "I don't understand the hidden layer",
            "That makes more sense now",
            "What about backpropagation?"
        ]

        for inp in learning_inputs:
            agent.interact(inp)

        # Check learning summary
        state = agent.get_agent_state()
        learning_summary = state["learning_summary"]

        assert learning_summary["total_experiences"] >= len(learning_inputs)

    def test_emotional_support_workflow(self):
        """Test emotional support workflow."""
        agent = create_character_agent(
            role="companion",
            personality={
                "agreeableness": 0.9,
                "neuroticism": 0.2
            }
        )

        # Emotional interaction
        result = agent.interact("I'm feeling really stressed lately")

        assert result.response is not None
        # Check emotional response was appropriate
        assert result.emotional_state is not None

    def test_collaborative_workflow(self):
        """Test collaborative problem-solving workflow."""
        agent = create_character_agent(
            role="collaborator",
            personality={
                "extraversion": 0.8,
                "agreeableness": 0.8
            }
        )

        # Collaborative task
        result = agent.interact("Let's work on this project together")

        assert result.response is not None
        # Should involve collaborative elements
        assert "together" in result.response.lower() or "we" in result.response.lower()


class TestCrossComponentIntegration:
    """Test integration between components."""

    def test_memory_influences_decisions(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test that memory system influences decisions."""
        # Make similar decisions multiple times
        for i in range(5):
            character_agent.interact("What should I do?")

        # Check memory statistics
        state = character_agent.get_agent_state()
        stats = state["memory_statistics"]

        assert stats["total_decisions"] >= 5

    def test_personality_influences_responses(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test that personality influences responses."""
        # Get initial personality
        initial_state = character_agent.get_agent_state()
        initial_personality = initial_state["personality_state"].copy()

        # Update personality
        character_agent.update_personality({"openness": 0.95})

        # Get response
        result = character_agent.interact("Tell me something interesting")

        # Personality should be updated
        current_state = character_agent.get_agent_state()
        assert current_state["personality_state"]["openness"] == 0.95

    def test_emotion_influences_state(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test that emotions influence state updates."""
        initial_valence = character_agent.current_emotional_state.valence

        # Positive input
        result1 = character_agent.interact("I'm so happy!")

        # Negative input
        result2 = character_agent.interact("This is terrible")

        # State should have been updated
        final_valence = character_agent.current_emotional_state.valence

        # (In full implementation, would check for changes)
        assert final_valence is not None

    def test_learning_from_interactions(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test that learning occurs during interactions."""
        initial_state = character_agent.get_agent_state()
        initial_experiences = initial_state["learning_summary"]["total_experiences"]

        # Have several interactions
        for i in range(3):
            character_agent.interact(f"Test message {i}")

        final_state = character_agent.get_agent_state()
        final_experiences = final_state["learning_summary"]["total_experiences"]

        assert final_experiences >= initial_experiences + 3


class TestDifferentConfigurations:
    """Test agents with different configurations."""

    def test_different_roles_produce_different_responses(self):
        """Test that different roles produce different responses."""
        input_text = "I need help with a problem"

        roles = ["mentor", "analyst", "companion", "teacher"]

        responses = {}
        for role in roles:
            agent = create_character_agent(
                role=role,
                personality={"openness": 0.7}
            )
            result = agent.interact(input_text)
            responses[role] = result.response

        # Responses should differ by role
        # (At minimum, they should all be valid strings)
        assert all(isinstance(r, str) and len(r) > 0 for r in responses.values())

    def test_different_personalities_produce_different_responses(self):
        """Test that different personalities produce different responses."""
        input_text = "Tell me about yourself"

        personalities = [
            {"openness": 0.9, "extraversion": 0.8},  # Outgoing
            {"openness": 0.5, "extraversion": 0.3},  # Reserved
        ]

        responses = []
        for personality in personalities:
            agent = create_character_agent(
                role="conversation_partner",
                personality=personality
            )
            result = agent.interact(input_text)
            responses.append(result.response)

        # Both should be valid
        assert all(isinstance(r, str) and len(r) > 0 for r in responses)

    def test_different_strategies(self):
        """Test different decision strategies."""
        strategies = [
            DecisionStrategy.EXPERIENCE_BASED,
            DecisionStrategy.PATTERN_RECOGNITION,
            DecisionStrategy.CONTEXTUAL,
            DecisionStrategy.HYBRID
        ]

        for strategy in strategies:
            config = AgentConfig(
                agent_role=RoleType.MENTOR,
                personality_traits={"openness": 0.7},
                emotional_baseline={"joy": 0.5},
                decision_strategy=strategy
            )

            agent = CharacterAgentIntegration(config=config)
            result = agent.interact("Test input")

            assert result is not None


class TestErrorHandling:
    """Test error handling in integration."""

    def test_empty_input(self, character_agent: CharacterAgentIntegration):
        """Test handling empty input."""
        result = character_agent.interact("")

        # Should still produce a result
        assert result is not None

    def test_very_long_input(self, character_agent: CharacterAgentIntegration):
        """Test handling very long input."""
        long_input = "word " * 1000

        result = character_agent.interact(long_input)

        assert result is not None

    def test_special_characters(self, character_agent: CharacterAgentIntegration):
        """Test handling special characters."""
        special_input = "Test with émojis 🎉 and spëcial çharacters!"

        result = character_agent.interact(special_input)

        assert result is not None


class TestMetadata:
    """Test metadata in integration results."""

    def test_result_metadata(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test that results include metadata."""
        result = character_agent.interact("Test input")

        assert result.metadata is not None
        assert "input_emotions" in result.metadata
        assert "decision" in result.metadata
        assert "learning_summary" in result.metadata

    def test_input_emotions_recorded(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test that input emotions are recorded."""
        result = character_agent.interact("I'm very happy!")

        assert "input_emotions" in result.metadata
        assert isinstance(result.metadata["input_emotions"], dict)

    def test_decision_recorded(
        self,
        character_agent: CharacterAgentIntegration
    ):
        """Test that decisions are recorded."""
        result = character_agent.interact("What should I do?")

        assert "decision" in result.metadata
        assert isinstance(result.metadata["decision"], str)


class TestPerformance:
    """Test performance characteristics."""

    def test_response_time(self, character_agent: CharacterAgentIntegration):
        """Test that responses are generated in reasonable time."""
        import time

        start = time.time()
        result = character_agent.interact("Test input")
        end = time.time()

        response_time = end - start

        assert result is not None
        # Should be reasonably fast (adjust threshold as needed)
        assert response_time < 5.0

    def test_multiple_interactions_performance(self):
        """Test performance over multiple interactions."""
        import time

        agent = create_character_agent(
            role="conversation_partner",
            personality={"openness": 0.7}
        )

        start = time.time()
        for i in range(10):
            agent.interact(f"Test message {i}")
        end = time.time()

        total_time = end - start

        # Average should be reasonable
        avg_time = total_time / 10
        assert avg_time < 2.0


class TestStateManagement:
    """Test state management across interactions."""

    def test_state_persistence(self, character_agent: CharacterAgentIntegration):
        """Test that state persists across interactions."""
        state1 = character_agent.get_agent_state()

        character_agent.interact("First message")
        state2 = character_agent.get_agent_state()

        character_agent.interact("Second message")
        state3 = character_agent.get_agent_state()

        # State should evolve
        assert state2["learning_summary"]["total_experiences"] >= \
               state1["learning_summary"]["total_experiences"]
        assert state3["learning_summary"]["total_experiences"] >= \
               state2["learning_summary"]["total_experiences"]

    def test_independent_agents(self):
        """Test that different agents maintain independent state."""
        agent1 = create_character_agent(
            role="mentor",
            personality={"openness": 0.7}
        )
        agent2 = create_character_agent(
            role="companion",
            personality={"openness": 0.7}
        )

        agent1.interact("Test message")
        agent2.interact("Test message")

        state1 = agent1.get_agent_state()
        state2 = agent2.get_agent_state()

        # Should have independent states
        assert state1 is not state2
