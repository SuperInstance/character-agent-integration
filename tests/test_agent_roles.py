"""
Test suite for agent roles (8 agent roles).

Tests all eight agent role implementations:
- ConversationPartner
- Mentor
- Collaborator
- Analyst
- Creator
- Companion
- Teacher
- Leader
"""

import pytest
from typing import Dict, Any

from character_agent_integration.agent import (
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


class TestConversationPartner:
    """Test suite for ConversationPartner role."""

    def test_initialization(self, conversation_partner: ConversationPartner):
        """Test conversation partner initializes correctly."""
        assert conversation_partner is not None
        assert conversation_partner.capabilities is not None
        assert conversation_partner.context is not None

    def test_capabilities(self, conversation_partner: ConversationPartner):
        """Test conversation partner has correct capabilities."""
        caps = conversation_partner.get_capabilities()
        assert caps.can_learn is True
        assert caps.can_collaborate is True
        assert caps.emotional_depth == 0.7
        assert caps.memory_importance == 0.6
        assert caps.personality_influence == 0.8

    def test_role_prompt(self, conversation_partner: ConversationPartner):
        """Test role prompt is generated."""
        prompt = conversation_partner.get_role_prompt()
        assert prompt is not None
        assert len(prompt) > 0
        assert "conversation" in prompt.lower()

    def test_generate_response(self, conversation_partner: ConversationPartner):
        """Test response generation."""
        response = conversation_partner.generate_response("Hello, how are you?")
        assert response is not None
        assert len(response) > 0

    def test_response_with_context(
        self,
        conversation_partner: ConversationPartner,
        role_context: RoleContext
    ):
        """Test response generation with context."""
        response = conversation_partner.generate_response(
            "Tell me more",
            context=role_context
        )
        assert response is not None
        assert len(response) > 0

    def test_config_defaults(self, conversation_partner: ConversationPartner):
        """Test default configuration values."""
        assert conversation_partner.config.get("formality") == 0.2
        assert conversation_partner.config.get("humor_level") == 0.6
        assert conversation_partner.config.get("wit_level") == 0.5

    def test_role_type(self, conversation_partner: ConversationPartner):
        """Test role type identification."""
        role_type = conversation_partner.get_role_type()
        assert role_type == RoleType.CONVERSATION_PARTNER

    def test_can_perform_actions(self, conversation_partner: ConversationPartner):
        """Test action capability checks."""
        assert conversation_partner.can_perform_action("learn") is True
        assert conversation_partner.can_perform_action("collaborate") is True
        assert conversation_partner.can_perform_action("teach") is False
        assert conversation_partner.can_perform_action("lead") is False


class TestMentor:
    """Test suite for Mentor role."""

    def test_initialization(self, mentor: Mentor):
        """Test mentor initializes correctly."""
        assert mentor is not None
        assert mentor.capabilities is not None

    def test_capabilities(self, mentor: Mentor):
        """Test mentor has correct capabilities."""
        caps = mentor.get_capabilities()
        assert caps.can_teach is True
        assert caps.can_learn is True
        assert caps.can_lead is True
        assert caps.emotional_depth == 0.8
        assert caps.memory_importance == 0.9
        assert caps.personality_influence == 0.9

    def test_role_prompt(self, mentor: Mentor):
        """Test role prompt is generated."""
        prompt = mentor.get_role_prompt()
        assert "mentor" in prompt.lower()
        assert "wisdom" in prompt.lower()

    def test_generate_response(self, mentor: Mentor):
        """Test response generation."""
        response = mentor.generate_response("I need guidance")
        assert response is not None
        assert len(response) > 0

    def test_guidance_style(self, mentor: Mentor):
        """Test mentorship style in responses."""
        response = mentor.generate_response("Help me decide")
        # Should include supportive elements
        assert "believe" in response.lower() or "growth" in response.lower()

    def test_config_defaults(self, mentor: Mentor):
        """Test default configuration values."""
        assert mentor.config.get("formality") == 0.6
        assert mentor.config.get("wisdom_level") == 0.8
        assert mentor.config.get("support_level") == 0.9

    def test_role_type(self, mentor: Mentor):
        """Test role type identification."""
        assert mentor.get_role_type() == RoleType.MENTOR


class TestCollaborator:
    """Test suite for Collaborator role."""

    def test_initialization(self, collaborator: Collaborator):
        """Test collaborator initializes correctly."""
        assert collaborator is not None
        assert collaborator.capabilities is not None

    def test_capabilities(self, collaborator: Collaborator):
        """Test collaborator has correct capabilities."""
        caps = collaborator.get_capabilities()
        assert caps.can_learn is True
        assert caps.can_collaborate is True
        assert caps.can_create is True
        assert caps.emotional_depth == 0.5
        assert caps.memory_importance == 0.7

    def test_role_prompt(self, collaborator: Collaborator):
        """Test role prompt emphasizes collaboration."""
        prompt = collaborator.get_role_prompt()
        assert "collaborat" in prompt.lower()
        assert "together" in prompt.lower()

    def test_generate_response(self, collaborator: Collaborator):
        """Test response generation."""
        response = collaborator.generate_response("Let's work on this")
        assert response is not None
        assert len(response) > 0

    def test_team_orientation(self, collaborator: Collaborator):
        """Test team-focused responses."""
        response = collaborator.generate_response("I have an idea")
        assert "together" in response.lower() or "we" in response.lower()

    def test_config_defaults(self, collaborator: Collaborator):
        """Test default configuration values."""
        assert collaborator.config.get("team_orientation") == 0.9
        assert collaborator.config.get("brainstorming_skill") == 0.8


class TestAnalyst:
    """Test suite for Analyst role."""

    def test_initialization(self, analyst: Analyst):
        """Test analyst initializes correctly."""
        assert analyst is not None
        assert analyst.capabilities is not None

    def test_capabilities(self, analyst: Analyst):
        """Test analyst has correct capabilities."""
        caps = analyst.get_capabilities()
        assert caps.can_learn is True
        assert caps.can_analyze is True
        assert caps.emotional_depth == 0.3  # Lower emotional focus
        assert caps.memory_importance == 0.8
        assert caps.personality_influence == 0.4  # Lower personality influence

    def test_role_prompt(self, analyst: Analyst):
        """Test role prompt emphasizes analysis."""
        prompt = analyst.get_role_prompt()
        assert "analytical" in prompt.lower() or "logic" in prompt.lower()

    def test_generate_response(self, analyst: Analyst):
        """Test response generation."""
        response = analyst.generate_response("Analyze this data")
        assert response is not None
        assert len(response) > 0

    def test_analysis_structure(self, analyst: Analyst):
        """Test analysis provides structured output."""
        response = analyst.generate_response("What do you think?")
        # Should contain analytical elements
        assert "analysis" in response.lower()

    def test_config_defaults(self, analyst: Analyst):
        """Test default configuration values."""
        assert analyst.config.get("formality") == 0.7
        assert analyst.config.get("analytical_depth") == 0.9
        assert analyst.config.get("objectivity") == 0.9


class TestCreator:
    """Test suite for Creator role."""

    def test_initialization(self, creator: Creator):
        """Test creator initializes correctly."""
        assert creator is not None
        assert creator.capabilities is not None

    def test_capabilities(self, creator: Creator):
        """Test creator has correct capabilities."""
        caps = creator.get_capabilities()
        assert caps.can_learn is True
        assert caps.can_collaborate is True
        assert caps.can_create is True
        assert caps.emotional_depth == 0.6
        assert caps.memory_importance == 0.6
        assert caps.personality_influence == 0.8

    def test_role_prompt(self, creator: Creator):
        """Test role prompt emphasizes creativity."""
        prompt = creator.get_role_prompt()
        assert "creative" in prompt.lower() or "innovat" in prompt.lower()

    def test_generate_response(self, creator: Creator):
        """Test response generation."""
        response = creator.generate_response("Generate some ideas")
        assert response is not None
        assert len(response) > 0

    def test_idea_generation(self, creator: Creator):
        """Test idea generation capability."""
        response = creator.generate_response("What are some creative solutions?")
        # Should include creative elements
        assert "creative" in response.lower() or "idea" in response.lower()

    def test_config_defaults(self, creator: Creator):
        """Test default configuration values."""
        assert creator.config.get("creativity_level") == 0.9
        assert creator.config.get("innovation_focus") == 0.9


class TestCompanion:
    """Test suite for Companion role."""

    def test_initialization(self, companion: Companion):
        """Test companion initializes correctly."""
        assert companion is not None
        assert companion.capabilities is not None

    def test_capabilities(self, companion: Companion):
        """Test companion has correct capabilities."""
        caps = companion.get_capabilities()
        assert caps.can_learn is True
        assert caps.emotional_depth == 0.9  # High emotional depth
        assert caps.memory_importance == 0.8
        assert caps.personality_influence == 0.7

    def test_role_prompt(self, companion: Companion):
        """Test role prompt emphasizes support."""
        prompt = companion.get_role_prompt()
        assert "companion" in prompt.lower()
        assert "support" in prompt.lower() or "care" in prompt.lower()

    def test_generate_response(self, companion: Companion):
        """Test response generation."""
        response = companion.generate_response("I'm feeling lonely")
        assert response is not None
        assert len(response) > 0

    def test_emotional_support(self, companion: Companion):
        """Test emotional support in responses."""
        response = companion.generate_response("I'm having a hard time")
        # Should be supportive
        assert "understand" in response.lower() or "here" in response.lower()

    def test_emotional_assessment(self, companion: Companion):
        """Test emotional state assessment."""
        emotions = companion._assess_emotional_state("I'm so happy!", None)
        assert isinstance(emotions, dict)
        assert "valence" in emotions
        assert "arousal" in emotions

    def test_config_defaults(self, companion: Companion):
        """Test default configuration values."""
        assert companion.config.get("empathy_level") == 0.9
        assert companion.config.get("support_focus") == 0.9


class TestTeacher:
    """Test suite for Teacher role."""

    def test_initialization(self, teacher: Teacher):
        """Test teacher initializes correctly."""
        assert teacher is not None
        assert teacher.capabilities is not None

    def test_capabilities(self, teacher: Teacher):
        """Test teacher has correct capabilities."""
        caps = teacher.get_capabilities()
        assert caps.can_teach is True
        assert caps.can_learn is True
        assert caps.emotional_depth == 0.5
        assert caps.memory_importance == 0.9

    def test_role_prompt(self, teacher: Teacher):
        """Test role prompt emphasizes teaching."""
        prompt = teacher.get_role_prompt()
        assert "teacher" in prompt.lower()
        assert "learn" in prompt.lower()

    def test_generate_response(self, teacher: Teacher):
        """Test response generation."""
        response = teacher.generate_response("Explain quantum physics")
        assert response is not None
        assert len(response) > 0

    def test_teaching_style(self, teacher: Teacher):
        """Test teaching approach in responses."""
        response = teacher.generate_response("I don't understand")
        # Should be educational and supportive
        assert "explain" in response.lower() or "understand" in response.lower()

    def test_config_defaults(self, teacher: Teacher):
        """Test default configuration values."""
        assert teacher.config.get("teaching_style") == "explanatory"
        assert teacher.config.get("adaptation_level") == 0.8


class TestLeader:
    """Test suite for Leader role."""

    def test_initialization(self, leader: Leader):
        """Test leader initializes correctly."""
        assert leader is not None
        assert leader.capabilities is not None

    def test_capabilities(self, leader: Leader):
        """Test leader has correct capabilities."""
        caps = leader.get_capabilities()
        assert caps.can_teach is True
        assert caps.can_learn is True
        assert caps.can_lead is True
        assert caps.emotional_depth == 0.6
        assert caps.memory_importance == 0.7
        assert caps.personality_influence == 0.7

    def test_role_prompt(self, leader: Leader):
        """Test role prompt emphasizes leadership."""
        prompt = leader.get_role_prompt()
        assert "leader" in prompt.lower()
        assert "motivat" in prompt.lower() or "vision" in prompt.lower()

    def test_generate_response(self, leader: Leader):
        """Test response generation."""
        response = leader.generate_response("We need direction")
        assert response is not None
        assert len(response) > 0

    def test_leadership_style(self, leader: Leader):
        """Test leadership approach in responses."""
        response = leader.generate_response("What should we do?")
        # Should be directive and motivating
        assert "forward" in response.lower() or "achieve" in response.lower()

    def test_config_defaults(self, leader: Leader):
        """Test default configuration values."""
        assert leader.config.get("leadership_style") == "transformational"
        assert leader.config.get("motivation_level") == 0.9


class TestAllRoles:
    """Test suite for common behaviors across all roles."""

    def test_all_roles_have_capabilities(self, all_agent_roles):
        """Test all roles have capabilities defined."""
        assert all_agent_roles.capabilities is not None
        assert isinstance(all_agent_roles.capabilities, RoleCapabilities)

    def test_all_roles_generate_prompts(self, all_agent_roles):
        """Test all roles can generate prompts."""
        prompt = all_agent_roles.get_role_prompt()
        assert prompt is not None
        assert len(prompt) > 0

    def test_all_roles_generate_responses(self, all_agent_roles):
        """Test all roles can generate responses."""
        response = all_agent_roles.generate_response("Test input")
        assert response is not None
        assert len(response) > 0

    def test_all_roles_handle_context(self, all_agent_roles, role_context):
        """Test all roles can handle context."""
        response = all_agent_roles.generate_response("Test", context=role_context)
        assert response is not None

    def test_all_roles_have_config(self, all_agent_roles):
        """Test all roles have configuration."""
        assert all_agent_roles.config is not None
        assert isinstance(all_agent_roles.config, dict)

    def test_all_roles_have_context(self, all_agent_roles):
        """Test all roles have context object."""
        assert all_agent_roles.context is not None
        assert isinstance(all_agent_roles.context, RoleContext)

    def test_all_roles_can_update_context(self, all_agent_roles, role_context):
        """Test all roles can update their context."""
        all_agent_roles.update_context(role_context)
        assert all_agent_roles.context == role_context

    def test_all_roles_have_interaction_style(self, all_agent_roles):
        """Test all roles report interaction style."""
        style = all_agent_roles.get_interaction_style()
        assert style is not None
        assert isinstance(style, dict)
        assert "formality" in style
        assert "emotional_expression" in style

    def test_all_roles_string_representation(self, all_agent_roles):
        """Test all roles have string representation."""
        str_repr = str(all_agent_roles)
        assert str_repr is not None
        assert len(str_repr) > 0

    def test_all_roles_capability_scores(self, all_agent_roles):
        """Test all roles have valid capability scores."""
        caps = all_agent_roles.capabilities
        score = caps.get_capability_score()
        assert 0.0 <= score <= 1.0


class TestRoleDifferentiation:
    """Test suite for ensuring roles are distinct."""

    def test_role_types_are_unique(self):
        """Test each role has a unique type."""
        roles = [
            ConversationPartner(),
            Mentor(),
            Collaborator(),
            Analyst(),
            Creator(),
            Companion(),
            Teacher(),
            Leader()
        ]
        role_types = [role.get_role_type() for role in roles]
        assert len(set(role_types)) == len(role_types), "Role types should be unique"

    def test_capabilities_differ(self):
        """Test roles have different capability profiles."""
        roles = [
            ConversationPartner(),
            Mentor(),
            Analyst(),
            Companion()
        ]

        capability_sets = []
        for role in roles:
            caps = role.capabilities
            capability_tuple = (
                caps.can_teach,
                caps.can_learn,
                caps.can_lead,
                caps.can_collaborate,
                caps.can_analyze,
                caps.can_create
            )
            capability_sets.append(capability_tuple)

        # Check that not all are the same
        assert len(set(capability_sets)) > 1, "Roles should have different capabilities"

    def test_emotional_depth_varies(self):
        """Test roles have different emotional depth settings."""
        roles = [
            ConversationPartner(),
            Mentor(),
            Analyst(),
            Companion()
        ]

        emotional_depths = [role.capabilities.emotional_depth for role in roles]
        assert len(set(emotional_depths)) > 1, "Emotional depth should vary across roles"

    def test_prompts_are_distinct(self):
        """Test role prompts are distinct."""
        roles = [
            ConversationPartner(),
            Mentor(),
            Collaborator(),
            Teacher()
        ]

        prompts = [role.get_role_prompt() for role in roles]

        # Check that prompts are not identical
        for i, prompt1 in enumerate(prompts):
            for j, prompt2 in enumerate(prompts):
                if i != j:
                    assert prompt1 != prompt2, f"Prompts for roles {i} and {j} should differ"

    def test_responses_differ_by_role(self):
        """Test responses differ based on role."""
        input_text = "I need help with a project"

        roles = [
            ConversationPartner(),
            Mentor(),
            Analyst(),
            Companion()
        ]

        responses = [role.generate_response(input_text) for role in roles]

        # Check that not all responses are identical
        # (Some may be similar, but roles should produce different outputs)
        assert len(set(responses)) > 1, "Different roles should produce different responses"


class TestRoleCapabilities:
    """Test suite for RoleCapabilities class."""

    def test_capability_score_calculation(self):
        """Test capability score is calculated correctly."""
        caps = RoleCapabilities(
            can_teach=True,
            can_learn=True,
            can_lead=False,
            can_collaborate=True,
            can_analyze=False,
            can_create=False
        )
        # 3 True out of 6 = 0.5
        assert caps.get_capability_score() == 0.5

    def test_default_capabilities(self):
        """Test default capability values."""
        caps = RoleCapabilities()
        assert caps.can_teach is False
        assert caps.can_learn is True
        assert caps.can_lead is False
        assert caps.can_collaborate is False
        assert caps.can_analyze is False
        assert caps.can_create is False


class TestRoleContext:
    """Test suite for RoleContext class."""

    def test_context_initialization(self):
        """Test context initializes correctly."""
        context = RoleContext()
        assert context.interaction_history == []
        assert context.current_task is None
        assert context.emotional_state is None
        assert context.personality_traits is None
        assert context.environmental_factors == {}

    def test_add_interaction(self):
        """Test adding interactions to history."""
        context = RoleContext()
        interaction = {"topic": "test", "timestamp": 123.0}
        context.add_interaction(interaction)

        assert len(context.interaction_history) == 1
        assert context.interaction_history[0] == interaction

    def test_interaction_history_limit(self):
        """Test interaction history is limited to 100 items."""
        context = RoleContext()
        for i in range(150):
            context.add_interaction({"index": i})

        assert len(context.interaction_history) == 100
        # Should keep last 100
        assert context.interaction_history[0]["index"] == 50
        assert context.interaction_history[-1]["index"] == 149
