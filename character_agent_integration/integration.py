"""
Character-Agent Integration Main Module

Integrates all components into a cohesive system for character-driven AI agents.
Connects agent roles, memory, personality, and emotion into a unified framework.
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field

from .agent import AgentRole, RoleType
from .memory import (
    MemoryAugmentedDecisions,
    DecisionContext,
    DecisionStrategy,
    ContextualMemory
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


@dataclass
class AgentConfig:
    """Configuration for a character agent."""
    agent_role: RoleType
    personality_traits: Dict[str, float]
    emotional_baseline: Dict[str, float]
    learning_style: Optional[str] = None
    decision_strategy: DecisionStrategy = DecisionStrategy.HYBRID
    empathy_level: float = 0.7

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_role": self.agent_role.value,
            "personality_traits": self.personality_traits,
            "emotional_baseline": self.emotional_baseline,
            "learning_style": self.learning_style,
            "decision_strategy": self.decision_strategy.value,
            "empathy_level": self.empathy_level
        }


@dataclass
class IntegrationResult:
    """Result from a character-agent interaction."""
    response: str
    emotional_state: EmotionalState
    decision_context: Optional[DecisionContext]
    learning_occurred: bool
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class CharacterAgentIntegration:
    """
    Main integration system for character-driven AI agents.

    Combines:
    - Agent roles (behavioral patterns)
    - Memory-augmented decision making
    - Personality-driven learning
    - Emotional intelligence

    This is the primary interface for creating and using character agents.
    """

    def __init__(
        self,
        config: AgentConfig,
        memory_system: Optional[Any] = None
    ):
        """
        Initialize the character-agent integration system.

        Args:
            config: Agent configuration
            memory_system: Optional hierarchical memory system
        """
        self.config = config

        # Initialize components
        self.agent_role = self._create_agent_role()
        self.memory_system = MemoryAugmentedDecisions(
            strategy=config.decision_strategy,
            memory_system=memory_system
        )
        self.contextual_memory = ContextualMemory()

        self.personality_learning = PersonalityDrivenLearning(
            personality_traits=config.personality_traits,
            learning_style=None  # Will be determined from traits
        )

        self.personality_influence = PersonalityInfluence(
            personality_traits=config.personality_traits
        )

        self.character_development = CharacterDevelopment(
            initial_personality=config.personality_traits.copy()
        )

        self.emotional_intelligence = EmotionalIntelligence(
            empathy_level=config.empathy_level
        )

        self.current_emotional_state = EmotionalState.from_dict(
            config.emotional_baseline
        )

    def _create_agent_role(self) -> AgentRole:
        """Create agent role based on config."""
        from .agent.roles import (
            ConversationPartner,
            Mentor,
            Collaborator,
            Analyst,
            Creator,
            Companion,
            Teacher,
            Leader
        )

        role_classes = {
            RoleType.CONVERSATION_PARTNER: ConversationPartner,
            RoleType.MENTOR: Mentor,
            RoleType.COLLABORATOR: Collaborator,
            RoleType.ANALYST: Analyst,
            RoleType.CREATOR: Creator,
            RoleType.COMPANION: Companion,
            RoleType.TEACHER: Teacher,
            RoleType.LEADER: Leader
        }

        role_class = role_classes.get(self.config.agent_role, ConversationPartner)
        return role_class()

    def interact(
        self,
        input_text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntegrationResult:
        """
        Process an interaction through the integrated character-agent system.

        This is the main method for using character agents. It:
        1. Recognizes emotions in input
        2. Updates emotional state
        3. Makes memory-augmented decisions
        4. Generates personality-influenced responses
        5. Learns from the interaction

        Args:
            input_text: User input text
            context: Optional interaction context

        Returns:
            IntegrationResult with response and metadata
        """
        # Step 1: Recognize emotions
        input_emotions = self.emotional_intelligence.recognize_emotion(
            input_text,
            context
        )

        # Step 2: Update emotional state
        self._update_emotional_state(input_emotions)

        # Step 3: Create decision context
        decision_context = self._create_decision_context(
            input_text,
            context
        )

        # Step 4: Make decision
        decision = self.memory_system.make_decision(decision_context)

        # Step 5: Generate base response from role
        base_response = self.agent_role.generate_response(
            input_text,
            self.agent_role.context
        )

        # Step 6: Apply personality influence
        personality_influenced = self.personality_influence.influence_response(
            base_response,
            context or {}
        )

        # Step 7: Apply emotional intelligence
        emotional_context = self.emotional_intelligence.understand_emotional_context(
            input_text,
            input_emotions,
            context
        )

        final_response = self.emotional_intelligence.generate_emotional_response(
            emotional_context,
            self.config.personality_traits
        )

        # Combine responses
        combined_response = self._combine_responses(
            personality_influenced,
            final_response
        )

        # Step 8: Learn from interaction
        learning_result = self._learn_from_interaction(
            input_text,
            combined_response,
            decision
        )

        return IntegrationResult(
            response=combined_response,
            emotional_state=self.current_emotional_state,
            decision_context=decision_context,
            learning_occurred=learning_result["learned"],
            confidence=decision.confidence,
            metadata={
                "input_emotions": input_emotions,
                "decision": decision.chosen_action,
                "learning_summary": learning_result["summary"]
            }
        )

    def _update_emotional_state(self, input_emotions: Dict[str, float]) -> None:
        """Update current emotional state based on input."""
        # Blend current state with input emotions
        input_state = EmotionalState()
        input_state.specific_emotions = input_emotions
        input_state.update_from_specific_emotions()

        # Blend with weight 0.3 (gradual change)
        self.current_emotional_state = self.current_emotional_state.blend_with(
            input_state,
            weight=0.3
        )

    def _create_decision_context(
        self,
        input_text: str,
        context: Optional[Dict[str, Any]]
    ) -> DecisionContext:
        """Create decision context for memory system."""
        return DecisionContext(
            current_situation={
                "input": input_text,
                "emotional_state": self.current_emotional_state.to_dict(),
                "personality": self.config.personality_traits
            },
            available_actions=self._get_available_actions(),
            constraints=context.get("constraints", {}) if context else {},
            goals=context.get("goals", []) if context else [],
            emotional_state=self.current_emotional_state.to_dict(),
            personality_traits=self.config.personality_traits
        )

    def _get_available_actions(self) -> List[str]:
        """Get available actions for current role."""
        return [
            "respond_helpfully",
            "ask_clarifying_question",
            "provide_information",
            "express_empathy",
            "maintain_conversation"
        ]

    def _combine_responses(
        self,
        personality_response: str,
        emotional_response: str
    ) -> str:
        """Combine personality-influenced and emotional responses."""
        # Simple concatenation with smoothing
        if personality_response == emotional_response:
            return personality_response

        # Blend them
        return f"{emotional_response} {personality_response}"

    def _learn_from_interaction(
        self,
        input_text: str,
        response: str,
        decision: Any
    ) -> Dict[str, Any]:
        """Learn from the interaction."""
        from .personality.learning import LearningExperience

        # Create learning experience
        experience = LearningExperience(
            situation={"input": input_text},
            action=response,
            outcome={"decision": decision.chosen_action},
            emotional_context=self.current_emotional_state.specific_emotions,
            personality_context=self.config.personality_traits
        )

        # Learn from it
        learning_result = self.personality_learning.learn_from_experience(
            experience
        )

        return {
            "learned": True,
            "summary": learning_result
        }

    def get_agent_state(self) -> Dict[str, Any]:
        """Get current agent state."""
        return {
            "config": self.config.to_dict(),
            "emotional_state": self.current_emotional_state.to_dict(),
            "personality_state": self.personality_learning.personality_traits,
            "memory_statistics": self.memory_system.get_statistics(),
            "learning_summary": self.personality_learning.get_learning_summary(),
            "development_summary": self.character_development.get_development_summary()
        }

    def update_personality(
        self,
        new_traits: Dict[str, float]
    ) -> None:
        """
        Update personality traits.

        Args:
            new_traits: New personality trait values
        """
        for trait, value in new_traits.items():
            self.config.personality_traits[trait] = value
            self.personality_learning.personality_traits[trait] = value
            self.personality_influence.personality_traits[trait] = value

    def reset_emotional_state(self) -> None:
        """Reset emotional state to baseline."""
        self.current_emotional_state = EmotionalState.from_dict(
            self.config.emotional_baseline
        )


def create_character_agent(
    role: str,
    personality: Dict[str, float],
    emotions: Optional[Dict[str, float]] = None,
    **kwargs
) -> CharacterAgentIntegration:
    """
    Factory function to create a character agent.

    Args:
        role: Agent role name (e.g., "mentor", "companion")
        personality: Personality traits (Big Five)
        emotions: Optional baseline emotional state
        **kwargs: Additional configuration options

    Returns:
        Configured CharacterAgentIntegration instance

    Example:
        >>> agent = create_character_agent(
        ...     role="mentor",
        ...     personality={"openness": 0.8, "conscientiousness": 0.7}
        ... )
        >>> result = agent.interact("I need advice on my career")
        >>> print(result.response)
    """
    role_type = RoleType(role.lower())

    if emotions is None:
        emotions = {
            "joy": 0.3,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "disgust": 0.0,
            "anticipation": 0.2,
            "trust": 0.5
        }

    config = AgentConfig(
        agent_role=role_type,
        personality_traits=personality,
        emotional_baseline=emotions,
        **kwargs
    )

    return CharacterAgentIntegration(config)
