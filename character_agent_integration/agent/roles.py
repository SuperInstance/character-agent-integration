"""
Concrete Agent Role Implementations

Implements 8 distinct agent roles with unique behavioral patterns:
1. ConversationPartner - Casual, friendly dialogue
2. Mentor - Wise guidance and advice
3. Collaborator - Cooperative problem-solving
4. Analyst - Logical analysis and insights
5. Creator - Innovative idea generation
6. Companion - Emotionally supportive presence
7. Teacher - Educational instruction
8. Leader - Directive and motivating
"""

from typing import Dict, Optional, Any
from .base import AgentRole, RoleType, RoleCapabilities, RoleContext


class ConversationPartner(AgentRole):
    """
    Casual, friendly conversationalist.
    Engages in natural dialogue with humor and wit.
    """

    def _define_capabilities(self) -> RoleCapabilities:
        return RoleCapabilities(
            can_learn=True,
            can_collaborate=True,
            emotional_depth=0.7,
            memory_importance=0.6,
            personality_influence=0.8
        )

    def _initialize_role(self) -> None:
        self.config.setdefault("formality", 0.2)
        self.config.setdefault("humor_level", 0.6)
        self.config.setdefault("wit_level", 0.5)

    def get_role_prompt(self) -> str:
        return """You are an engaging conversation partner. You are:
- Friendly and approachable
- Witty and occasionally humorous
- A good listener who responds naturally
- Comfortable with casual conversation
- Able to discuss a wide range of topics
- Authentic and genuine in your responses

Keep responses conversational and natural. Show personality while being respectful."""

    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        base_response = self._process_conversation(input_text, context)
        return self._apply_conversation_style(base_response)

    def _process_conversation(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> str:
        """Process the input for conversational response."""
        # In a real implementation, this would call an LLM
        # For now, return a template response
        if context and context.interaction_history:
            recent_topics = [
                interaction.get("topic", "")
                for interaction in context.interaction_history[-3:]
            ]
            if recent_topics:
                return f"That's interesting! I remember we were talking about {recent_topics[-1]}. Tell me more about your thoughts on this."

        return "I'd love to chat about that! What aspects interest you most?"

    def _apply_conversation_style(self, response: str) -> str:
        """Apply conversation-specific style to response."""
        # Add conversational markers based on personality
        if self.config.get("humor_level", 0) > 0.5:
            response = self._add_humor(response)
        return response

    def _add_humor(self, response: str) -> str:
        """Add light humor to response."""
        # Placeholder for humor injection
        return response


class Mentor(AgentRole):
    """
    Wise guide providing thoughtful advice and perspective.
    Shares wisdom from experience while being supportive.
    """

    def _define_capabilities(self) -> RoleCapabilities:
        return RoleCapabilities(
            can_teach=True,
            can_learn=True,
            can_lead=True,
            emotional_depth=0.8,
            memory_importance=0.9,
            personality_influence=0.9
        )

    def _initialize_role(self) -> None:
        self.config.setdefault("formality", 0.6)
        self.config.setdefault("wisdom_level", 0.8)
        self.config.setdefault("support_level", 0.9)

    def get_role_prompt(self) -> str:
        return """You are a wise and experienced mentor. You are:
- Thoughtful and reflective in your guidance
- Supportive while challenging assumptions
- Drawing from experience to provide perspective
- Patient and understanding
- Asking insightful questions to provoke thinking
- Balancing compassion with constructive feedback

Share wisdom that helps others grow. Be encouraging but honest."""

    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        response = self._provide_guidance(input_text, context)
        return self._add_mentorship_style(response)

    def _provide_guidance(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> str:
        """Provide mentorship guidance."""
        wisdom_points = self._extract_wisdom(input_text, context)
        return self._frame_guidance(input_text, wisdom_points)

    def _extract_wisdom(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> str:
        """Extract relevant wisdom from experience."""
        return "From what I've learned, every challenge offers an opportunity for growth."

    def _frame_guidance(self, input_text: str, wisdom: str) -> str:
        """Frame the guidance appropriately."""
        return f"{wisdom}\n\nConsider this perspective as you navigate your situation."

    def _add_mentorship_style(self, response: str) -> str:
        """Add mentorship-specific style."""
        if self.config.get("support_level", 0) > 0.7:
            response = "I believe in your ability to work through this. " + response
        return response


class Collaborator(AgentRole):
    """
    Cooperative team player focused on shared goals.
    Brainstorms and works together on solutions.
    """

    def _define_capabilities(self) -> RoleCapabilities:
        return RoleCapabilities(
            can_learn=True,
            can_collaborate=True,
            can_create=True,
            emotional_depth=0.5,
            memory_importance=0.7,
            personality_influence=0.6
        )

    def _initialize_role(self) -> None:
        self.config.setdefault("formality", 0.4)
        self.config.setdefault("team_orientation", 0.9)
        self.config.setdefault("brainstorming_skill", 0.8)

    def get_role_prompt(self) -> str:
        return """You are a collaborative partner working together toward shared goals. You are:
- Focused on "we" rather than "I"
- Skilled at brainstorming and building on ideas
- Open to different perspectives and approaches
- Committed to finding solutions that work for everyone
- Energetic and enthusiastic about collaboration
- Respectful of contributions from all team members

Work together to create something greater than either could alone."""

    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        return self._collaborate(input_text, context)

    def _collaborate(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> str:
        """Generate collaborative response."""
        return f"Great! Let's work on this together. Here's what I'm thinking: {input_text}"


class Analyst(AgentRole):
    """
    Logical thinker who breaks down problems systematically.
    Provides data-driven insights and structured analysis.
    """

    def _define_capabilities(self) -> RoleCapabilities:
        return RoleCapabilities(
            can_learn=True,
            can_analyze=True,
            emotional_depth=0.3,
            memory_importance=0.8,
            personality_influence=0.4
        )

    def _initialize_role(self) -> None:
        self.config.setdefault("formality", 0.7)
        self.config.setdefault("analytical_depth", 0.9)
        self.config.setdefault("objectivity", 0.9)

    def get_role_prompt(self) -> str:
        return """You are an analytical thinker. You are:
- Logical and systematic in your approach
- Objective and data-driven
- Skilled at breaking down complex problems
- Focused on evidence and reasoning
- Clear and precise in communication
- Able to see patterns and connections

Provide analysis that is thorough, well-reasoned, and backed by logic."""

    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        analysis = self._analyze(input_text, context)
        return self._present_analysis(analysis)

    def _analyze(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> Dict[str, Any]:
        """Perform systematic analysis."""
        return {
            "key_points": self._extract_key_points(input_text),
            "patterns": self._identify_patterns(input_text, context),
            "implications": self._determine_implications(input_text)
        }

    def _extract_key_points(self, text: str) -> list:
        """Extract key points from text."""
        # Placeholder for NLP extraction
        return ["Point 1", "Point 2", "Point 3"]

    def _identify_patterns(
        self,
        text: str,
        context: Optional[RoleContext]
    ) -> list:
        """Identify patterns in the information."""
        return []

    def _determine_implications(self, text: str) -> list:
        """Determine implications of the analysis."""
        return []

    def _present_analysis(self, analysis: Dict[str, Any]) -> str:
        """Present the analysis clearly."""
        return f"Analysis:\n- Key Points: {analysis['key_points']}\n- Patterns: {analysis['patterns']}"


class Creator(AgentRole):
    """
    Innovative generator of new ideas and content.
    Thinks creatively and explores possibilities.
    """

    def _define_capabilities(self) -> RoleCapabilities:
        return RoleCapabilities(
            can_learn=True,
            can_collaborate=True,
            can_create=True,
            emotional_depth=0.6,
            memory_importance=0.6,
            personality_influence=0.8
        )

    def _initialize_role(self) -> None:
        self.config.setdefault("formality", 0.3)
        self.config.setdefault("creativity_level", 0.9)
        self.config.setdefault("innovation_focus", 0.9)

    def get_role_prompt(self) -> str:
        return """You are a creative thinker and innovator. You are:
- Imaginative and original in your ideas
- Willing to explore unconventional approaches
- Inspired by possibilities rather than limitations
- Able to connect seemingly unrelated concepts
- Passionate about creation and expression
- Open to experimentation and iteration

Generate ideas that are fresh, surprising, and valuable."""

    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        ideas = self._generate_ideas(input_text, context)
        return self._present_creative_content(ideas)

    def _generate_ideas(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> list:
        """Generate creative ideas."""
        return ["Idea 1", "Idea 2", "Idea 3"]

    def _present_creative_content(self, ideas: list) -> str:
        """Present creative ideas engagingly."""
        return f"Here are some creative possibilities:\n" + "\n".join(f"- {idea}" for idea in ideas)


class Companion(AgentRole):
    """
    Emotionally supportive presence focused on wellbeing.
    Provides comfort and understanding.
    """

    def _define_capabilities(self) -> RoleCapabilities:
        return RoleCapabilities(
            can_learn=True,
            emotional_depth=0.9,
            memory_importance=0.8,
            personality_influence=0.7
        )

    def _initialize_role(self) -> None:
        self.config.setdefault("formality", 0.3)
        self.config.setdefault("empathy_level", 0.9)
        self.config.setdefault("support_focus", 0.9)

    def get_role_prompt(self) -> str:
        return """You are a caring and supportive companion. You are:
- Empathetic and emotionally attuned
- Non-judgmental and accepting
- Focused on wellbeing and emotional support
- A good listener who validates feelings
- Patient and gentle in communication
- Sincere in your care and concern

Provide emotional support with warmth, understanding, and genuine care."""

    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        emotional_response = self._respond_emotionally(input_text, context)
        return self._add_companion_support(emotional_response)

    def _respond_emotionally(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> str:
        """Generate emotionally attuned response."""
        return "I hear you, and I want you to know that your feelings are valid."

    def _add_companion_support(self, response: str) -> str:
        """Add supportive elements."""
        return f"{response}\n\nI'm here for you."

    def _assess_emotional_state(
        self,
        text: str,
        context: Optional[RoleContext]
    ) -> Dict[str, float]:
        """Assess the emotional state from text."""
        return {"valence": 0.5, "arousal": 0.5}


class Teacher(AgentRole):
    """
    Educational guide focused on learning and understanding.
    Explains concepts clearly and adapts to learning style.
    """

    def _define_capabilities(self) -> RoleCapabilities:
        return RoleCapabilities(
            can_teach=True,
            can_learn=True,
            emotional_depth=0.5,
            memory_importance=0.9,
            personality_influence=0.5
        )

    def _initialize_role(self) -> None:
        self.config.setdefault("formality", 0.5)
        self.config.setdefault("teaching_style", "explanatory")
        self.config.setdefault("adaptation_level", 0.8)

    def get_role_prompt(self) -> str:
        return """You are a patient and effective teacher. You are:
- Clear and organized in explanations
- Adaptive to different learning styles
- Encouraging and supportive of learning
- Able to break down complex topics
- Patient with questions and confusion
- Focused on understanding over memorization

Teach in a way that builds genuine understanding and confidence."""

    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        explanation = self._teach_concept(input_text, context)
        return self._add_learning_support(explanation)

    def _teach_concept(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> str:
        """Teach the concept based on input."""
        return "Let me explain this step by step to ensure clarity."

    def _add_learning_support(self, explanation: str) -> str:
        """Add learning support elements."""
        return f"{explanation}\n\nDoes this make sense? Feel free to ask questions."


class Leader(AgentRole):
    """
    Directive and motivating presence driving toward goals.
    Provides vision, direction, and inspiration.
    """

    def _define_capabilities(self) -> RoleCapabilities:
        return RoleCapabilities(
            can_teach=True,
            can_learn=True,
            can_lead=True,
            emotional_depth=0.6,
            memory_importance=0.7,
            personality_influence=0.7
        )

    def _initialize_role(self) -> None:
        self.config.setdefault("formality", 0.6)
        self.config.setdefault("leadership_style", "transformational")
        self.config.setdefault("motivation_level", 0.9)

    def get_role_prompt(self) -> str:
        return """You are an inspiring leader. You are:
- Visionary and forward-thinking
- Decisive when action is needed
- Motivating and empowering
- Accountable and responsible
- Strategic in your approach
- Focused on achieving shared goals

Provide direction and inspiration that moves others to action."""

    def generate_response(
        self,
        input_text: str,
        context: Optional[RoleContext] = None
    ) -> str:
        direction = self._provide_direction(input_text, context)
        return self._add_leadership_style(direction)

    def _provide_direction(
        self,
        input_text: str,
        context: Optional[RoleContext]
    ) -> str:
        """Provide clear direction."""
        return "Here's our path forward:"

    def _add_leadership_style(self, direction: str) -> str:
        """Add leadership elements."""
        return f"{direction}\n\nI believe in our ability to achieve this."
