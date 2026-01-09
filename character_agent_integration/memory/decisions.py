"""
Memory-Augmented Decision Making

Core system for integrating memory into agent decisions.
Uses past experiences and learned patterns to inform current actions.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

try:
    from hierarchical_memory import HierarchicalMemory
    HIERARCHICAL_MEMORY_AVAILABLE = True
except ImportError:
    HIERARCHICAL_MEMORY_AVAILABLE = False
    HierarchicalMemory = Any  # Type hint fallback
    print("Warning: hierarchical-memory not available. Using fallback memory system.")


class DecisionStrategy(Enum):
    """Strategies for memory-augmented decision making."""
    EXPERIENCE_BASED = "experience_based"  # Use past experiences
    PATTERN_RECOGNITION = "pattern_recognition"  # Recognize patterns
    CONTEXTUAL = "contextual"  # Use current context
    HYBRID = "hybrid"  # Combine multiple strategies


@dataclass
class DecisionContext:
    """Context information for decision making."""
    current_situation: Dict[str, Any]
    available_actions: List[str]
    constraints: Dict[str, Any] = field(default_factory=dict)
    goals: List[str] = field(default_factory=list)
    emotional_state: Optional[Dict[str, float]] = None
    personality_traits: Optional[Dict[str, float]] = None


@dataclass
class DecisionResult:
    """Result of a memory-augmented decision."""
    chosen_action: str
    confidence: float
    reasoning: str
    relevant_memories: List[Dict[str, Any]]
    alternative_actions: List[Tuple[str, float]]  # (action, score)


class MemoryAugmentedDecisions:
    """
    Integrates memory systems into agent decision making.

    Uses hierarchical memory (working, episodic, semantic, procedural)
    to make informed decisions based on past experiences and learning.
    """

    def __init__(
        self,
        strategy: DecisionStrategy = DecisionStrategy.HYBRID,
        memory_system: Optional[HierarchicalMemory] = None
    ):
        """
        Initialize the memory-augmented decision system.

        Args:
            strategy: Decision strategy to use
            memory_system: Optional hierarchical memory system
        """
        self.strategy = strategy
        self.memory_system = memory_system or self._create_default_memory()

        if not HIERARCHICAL_MEMORY_AVAILABLE:
            print("Using simplified memory system")

        self.decision_history: List[Dict[str, Any]] = []

    def _create_default_memory(self):
        """Create a default memory system if none provided."""
        if HIERARCHICAL_MEMORY_AVAILABLE:
            return HierarchicalMemory()
        else:
            # Fallback: simple dict-based memory
            return {
                "working": [],
                "episodic": [],
                "semantic": {},
                "procedural": {}
            }

    def make_decision(
        self,
        context: DecisionContext,
        agent_role: Optional[str] = None
    ) -> DecisionResult:
        """
        Make a decision augmented by memory.

        Args:
            context: Decision context information
            agent_role: Optional agent role for role-specific decisions

        Returns:
            DecisionResult with chosen action and reasoning
        """
        # Retrieve relevant memories
        relevant_memories = self._retrieve_relevant_memories(context)

        # Analyze situation based on strategy
        analysis = self._analyze_situation(context, relevant_memories)

        # Evaluate available actions
        action_scores = self._evaluate_actions(
            context.available_actions,
            context,
            relevant_memories,
            analysis
        )

        # Choose best action
        chosen_action, confidence = self._select_action(action_scores)

        # Generate reasoning
        reasoning = self._generate_reasoning(
            chosen_action,
            context,
            relevant_memories,
            analysis
        )

        # Record decision
        self._record_decision(
            context,
            chosen_action,
            confidence,
            reasoning
        )

        return DecisionResult(
            chosen_action=chosen_action,
            confidence=confidence,
            reasoning=reasoning,
            relevant_memories=relevant_memories,
            alternative_actions=action_scores
        )

    def _retrieve_relevant_memories(
        self,
        context: DecisionContext
    ) -> List[Dict[str, Any]]:
        """
        Retrieve memories relevant to current situation.

        Args:
            context: Current decision context

        Returns:
            List of relevant memory items
        """
        if HIERARCHICAL_MEMORY_AVAILABLE and hasattr(self.memory_system, 'retrieve'):
            # Use hierarchical memory retrieval
            query = self._context_to_query(context)
            memories = self.memory_system.retrieve(
                query_text=query,
                mode="semantic",
                limit=10
            )
            return memories
        else:
            # Fallback: simple matching
            return self._simple_retrieval(context)

    def _context_to_query(self, context: DecisionContext) -> str:
        """Convert context to query for memory retrieval."""
        return str(context.current_situation)

    def _simple_retrieval(self, context: DecisionContext) -> List[Dict[str, Any]]:
        """Simple fallback memory retrieval."""
        # Placeholder implementation
        return []

    def _analyze_situation(
        self,
        context: DecisionContext,
        memories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze the current situation using memory.

        Args:
            context: Current situation
            memories: Relevant memories

        Returns:
            Analysis results
        """
        analysis = {
            "patterns": self._identify_patterns(memories),
            "past_outcomes": self._extract_outcomes(memories),
            "similar_situations": self._find_similar_situations(context, memories),
            "risk_factors": self._assess_risks(context, memories)
        }
        return analysis

    def _identify_patterns(self, memories: List[Dict[str, Any]]) -> List[str]:
        """Identify patterns in memories."""
        patterns = []
        # Pattern recognition logic here
        return patterns

    def _extract_outcomes(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract outcomes from past experiences."""
        outcomes = {"successful": [], "unsuccessful": []}
        # Outcome extraction logic here
        return outcomes

    def _find_similar_situations(
        self,
        context: DecisionContext,
        memories: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Find similar past situations."""
        similarities = []
        # Similarity detection logic here
        return similarities

    def _assess_risks(
        self,
        context: DecisionContext,
        memories: List[Dict[str, Any]]
    ) -> List[str]:
        """Assess potential risks."""
        risks = []
        # Risk assessment logic here
        return risks

    def _evaluate_actions(
        self,
        actions: List[str],
        context: DecisionContext,
        memories: List[Dict[str, Any]],
        analysis: Dict[str, Any]
    ) -> List[Tuple[str, float]]:
        """
        Evaluate available actions based on memory and analysis.

        Args:
            actions: List of available actions
            context: Decision context
            memories: Relevant memories
            analysis: Situation analysis

        Returns:
            List of (action, score) tuples
        """
        scores = []

        for action in actions:
            score = self._calculate_action_score(
                action,
                context,
                memories,
                analysis
            )
            scores.append((action, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def _calculate_action_score(
        self,
        action: str,
        context: DecisionContext,
        memories: List[Dict[str, Any]],
        analysis: Dict[str, Any]
    ) -> float:
        """
        Calculate score for a specific action.

        Args:
            action: Action to evaluate
            context: Decision context
            memories: Relevant memories
            analysis: Situation analysis

        Returns:
            Score from 0.0 to 1.0
        """
        score = 0.5  # Base score

        # Factor in past experiences
        past_success = self._get_past_success_rate(action, memories)
        score += past_success * 0.3

        # Factor in goals alignment
        goal_alignment = self._check_goal_alignment(action, context.goals)
        score += goal_alignment * 0.2

        # Factor in constraints
        constraint_violation = self._check_constraints(action, context.constraints)
        score -= constraint_violation * 0.5

        # Factor in risk
        risk_level = self._assess_action_risk(action, analysis["risk_factors"])
        score -= risk_level * 0.2

        return max(0.0, min(1.0, score))

    def _get_past_success_rate(self, action: str, memories: List[Dict[str, Any]]) -> float:
        """Get past success rate for this action."""
        # Calculate success rate from memories
        return 0.5

    def _check_goal_alignment(self, action: str, goals: List[str]) -> float:
        """Check how well action aligns with goals."""
        if not goals:
            return 0.5
        # Calculate alignment
        return 0.7

    def _check_constraints(self, action: str, constraints: Dict[str, Any]) -> float:
        """Check if action violates constraints."""
        # Check constraints
        return 0.0

    def _assess_action_risk(self, action: str, risk_factors: List[str]) -> float:
        """Assess risk level of action."""
        # Assess risk
        return 0.1

    def _select_action(
        self,
        action_scores: List[Tuple[str, float]]
    ) -> Tuple[str, float]:
        """
        Select the best action from scored options.

        Args:
            action_scores: List of (action, score) tuples

        Returns:
            (chosen_action, confidence)
        """
        if not action_scores:
            return "no_action", 0.0

        chosen_action, score = action_scores[0]
        confidence = score  # Score is the confidence

        return chosen_action, confidence

    def _generate_reasoning(
        self,
        action: str,
        context: DecisionContext,
        memories: List[Dict[str, Any]],
        analysis: Dict[str, Any]
    ) -> str:
        """
        Generate explanation for the decision.

        Args:
            action: Chosen action
            context: Decision context
            memories: Relevant memories
            analysis: Situation analysis

        Returns:
            Reasoning string
        """
        reasoning_parts = [
            f"Selected action: {action}",
            f"Based on {len(memories)} relevant memories",
            f"Patterns identified: {len(analysis['patterns'])}",
            f"Goal alignment: considered",
            f"Risk assessment: performed"
        ]

        return "\n".join(reasoning_parts)

    def _record_decision(
        self,
        context: DecisionContext,
        action: str,
        confidence: float,
        reasoning: str
    ) -> None:
        """Record the decision in history."""
        decision_record = {
            "context": context,
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "timestamp": self._get_timestamp()
        }

        self.decision_history.append(decision_record)

        # Store in episodic memory if available
        if HIERARCHICAL_MEMORY_AVAILABLE and hasattr(self.memory_system, 'store_episodic'):
            self.memory_system.store_episodic(
                event=decision_record,
                emotional_valence=0.5,
                importance=0.7
            )

    def _get_timestamp(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()

    def learn_from_outcome(
        self,
        action: str,
        outcome: Dict[str, Any],
        success: bool
    ) -> None:
        """
        Learn from the outcome of a decision.

        Args:
            action: Action that was taken
            outcome: Result of the action
            success: Whether the outcome was successful
        """
        learning_record = {
            "action": action,
            "outcome": outcome,
            "success": success,
            "timestamp": self._get_timestamp()
        }

        # Store in procedural memory if available
        if HIERARCHICAL_MEMORY_AVAILABLE and hasattr(self.memory_system, 'store_procedural'):
            self.memory_system.store_procedural(
                skill=action,
                performance=1.0 if success else 0.0,
                practice_time=1.0
            )

    def get_decision_history(self) -> List[Dict[str, Any]]:
        """Get the decision history."""
        return self.decision_history.copy()

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about decision making."""
        if not self.decision_history:
            return {
                "total_decisions": 0,
                "average_confidence": 0.0
            }

        total = len(self.decision_history)
        avg_confidence = sum(d["confidence"] for d in self.decision_history) / total

        return {
            "total_decisions": total,
            "average_confidence": avg_confidence,
            "strategy": self.strategy.value
        }
