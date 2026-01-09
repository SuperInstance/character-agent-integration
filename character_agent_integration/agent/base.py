"""
Base Agent Role Definition

Provides the foundational abstract class for all agent roles.
Defines the interface and common functionality for role-specific behavior.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


class RoleType(Enum):
    """Enumeration of available agent roles."""
    CONVERSATION_PARTNER = "conversation_partner"
    MENTOR = "mentor"
    COLLABORATOR = "collaborator"
    ANALYST = "analyst"
    CREATOR = "creator"
    COMPANION = "companion"
    TEACHER = "teacher"
    LEADER = "leader"


@dataclass
class RoleCapabilities:
    """Defines the capabilities and constraints of an agent role."""
    can_teach: bool = False
    can_learn: bool = True
    can_lead: bool = False
    can_collaborate: bool = False
    can_analyze: bool = False
    can_create: bool = False
    emotional_depth: float = 0.5  # 0.0 to 1.0
    memory_importance: float = 0.5  # 0.0 to 1.0
    personality_influence: float = 0.5  # 0.0 to 1.0

    def get_capability_score(self) -> float:
        """Calculate overall capability score."""
        capabilities = [
            self.can_teach, self.can_learn, self.can_lead,
            self.can_collaborate, self.can_analyze, self.can_create
        ]
        return sum(capabilities) / len(capabilities)


@dataclass
class RoleContext:
    """Context information for agent role execution."""
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    current_task: Optional[str] = None
    emotional_state: Optional[Dict[str, float]] = None
    personality_traits: Optional[Dict[str, float]] = None
    environmental_factors: Dict[str, Any] = field(default_factory=dict)

    def add_interaction(self, interaction: Dict[str, Any]) -> None:
        """Add an interaction to the history."""
        self.interaction_history.append(interaction)
        # Keep only last 100 interactions
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]


class AgentRole(ABC):
    """
    Abstract base class for all agent roles.

    Each role defines specific behaviors, response patterns, and interaction styles
    that guide how an AI agent engages with users and other agents.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent role.

        Args:
            config: Optional configuration dictionary for role customization
        """
        self.config = config or {}
        self.capabilities = self._define_capabilities()
        self.context = RoleContext()
        self._initialize_role()

    @abstractmethod
    def _define_capabilities(self) -> RoleCapabilities:
        """
        Define the capabilities for this specific role.

        Returns:
            RoleCapabilities object describing what this role can do
        """
        pass

    @abstractmethod
    def _initialize_role(self) -> None:
        """
        Initialize role-specific settings and parameters.
        Called during construction.
        """
        pass

    @abstractmethod
    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        """
        Generate a response appropriate for this role.

        Args:
            input_text: The input text to respond to
            context: Optional context information

        Returns:
            Role-appropriate response text
        """
        pass

    @abstractmethod
    def get_role_prompt(self) -> str:
        """
        Get the system prompt that defines this role's behavior.

        Returns:
            System prompt string
        """
        pass

    def update_context(self, context: RoleContext) -> None:
        """
        Update the role's context with new information.

        Args:
            context: New context information
        """
        self.context = context

    def get_capabilities(self) -> RoleCapabilities:
        """
        Get the capabilities of this role.

        Returns:
            RoleCapabilities object
        """
        return self.capabilities

    def get_role_type(self) -> RoleType:
        """
        Get the type identifier for this role.

        Returns:
            RoleType enum value
        """
        return RoleType(self.__class__.__name__.upper())

    def can_perform_action(self, action: str) -> bool:
        """
        Check if this role can perform a specific action.

        Args:
            action: The action to check

        Returns:
            True if the role can perform the action
        """
        action_mapping = {
            "teach": self.capabilities.can_teach,
            "learn": self.capabilities.can_learn,
            "lead": self.capabilities.can_lead,
            "collaborate": self.capabilities.can_collaborate,
            "analyze": self.capabilities.can_analyze,
            "create": self.capabilities.can_create
        }
        return action_mapping.get(action.lower(), False)

    def get_interaction_style(self) -> Dict[str, Any]:
        """
        Get the interaction style preferences for this role.

        Returns:
            Dictionary containing style parameters
        """
        return {
            "formality": self.config.get("formality", 0.5),
            "verbosity": self.config.get("verbosity", 0.5),
            "emotional_expression": self.capabilities.emotional_depth,
            "personality_influence": self.capabilities.personality_influence,
            "memory_usage": self.capabilities.memory_importance
        }

    def __repr__(self) -> str:
        """String representation of the role."""
        return f"{self.__class__.__name__}(capabilities={self.capabilities.get_capability_score():.2f})"
