"""
Test suite for memory-augmented decision making.

Tests the memory system's ability to:
- Retrieve relevant memories
- Analyze situations
- Evaluate actions
- Make decisions based on past experiences
- Learn from outcomes
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import Mock, patch

from character_agent_integration.memory import (
    MemoryAugmentedDecisions,
    DecisionContext,
    DecisionResult,
    DecisionStrategy
)


class TestDecisionContext:
    """Test suite for DecisionContext."""

    def test_initialization(self, decision_context: DecisionContext):
        """Test decision context initializes correctly."""
        assert decision_context.current_situation is not None
        assert decision_context.available_actions is not None
        assert isinstance(decision_context.available_actions, list)

    def test_default_values(self):
        """Test default values for optional fields."""
        context = DecisionContext(
            current_situation={"test": "value"},
            available_actions=["action1", "action2"]
        )
        assert context.constraints == {}
        assert context.goals == []
        assert context.emotional_state is None
        assert context.personality_traits is None

    def test_full_initialization(self):
        """Test initialization with all fields."""
        context = DecisionContext(
            current_situation={"input": "test"},
            available_actions=["action1"],
            constraints={"time": 60},
            goals=["help_user"],
            emotional_state={"joy": 0.5},
            personality_traits={"openness": 0.7}
        )
        assert context.constraints == {"time": 60}
        assert context.goals == ["help_user"]
        assert context.emotional_state == {"joy": 0.5}
        assert context.personality_traits == {"openness": 0.7}


class TestMemoryAugmentedDecisions:
    """Test suite for MemoryAugmentedDecisions."""

    def test_initialization(self, memory_decisions: MemoryAugmentedDecisions):
        """Test initialization."""
        assert memory_decisions is not None
        assert memory_decisions.strategy == DecisionStrategy.HYBRID
        assert memory_decisions.memory_system is not None
        assert memory_decisions.decision_history == []

    def test_initialization_with_strategies(self):
        """Test initialization with different strategies."""
        for strategy in [
            DecisionStrategy.EXPERIENCE_BASED,
            DecisionStrategy.PATTERN_RECOGNITION,
            DecisionStrategy.CONTEXTUAL,
            DecisionStrategy.HYBRID
        ]:
            mad = MemoryAugmentedDecisions(strategy=strategy)
            assert mad.strategy == strategy

    def test_default_memory_creation(self):
        """Test default memory system is created."""
        mad = MemoryAugmentedDecisions()
        assert mad.memory_system is not None

    def test_make_decision(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test making a decision."""
        result = memory_decisions.make_decision(decision_context)

        assert isinstance(result, DecisionResult)
        assert result.chosen_action is not None
        assert isinstance(result.confidence, float)
        assert 0.0 <= result.confidence <= 1.0
        assert result.reasoning is not None
        assert isinstance(result.relevant_memories, list)
        assert isinstance(result.alternative_actions, list)

    def test_decision_without_actions(self):
        """Test decision making when no actions available."""
        context = DecisionContext(
            current_situation={"test": "value"},
            available_actions=[]
        )

        mad = MemoryAugmentedDecisions()
        result = mad.make_decision(context)

        assert result.chosen_action == "no_action"
        assert result.confidence == 0.0

    def test_decision_recording(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test that decisions are recorded."""
        initial_history_len = len(memory_decisions.decision_history)

        memory_decisions.make_decision(decision_context)

        assert len(memory_decisions.decision_history) == initial_history_len + 1

    def test_decision_history_structure(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test decision history has correct structure."""
        memory_decisions.make_decision(decision_context)

        record = memory_decisions.decision_history[-1]
        assert "context" in record
        assert "action" in record
        assert "confidence" in record
        assert "reasoning" in record
        assert "timestamp" in record

    def test_retrieve_relevant_memories(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test memory retrieval."""
        memories = memory_decisions._retrieve_relevant_memories(decision_context)

        assert isinstance(memories, list)

    def test_analyze_situation(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test situation analysis."""
        memories = []
        analysis = memory_decisions._analyze_situation(decision_context, memories)

        assert "patterns" in analysis
        assert "past_outcomes" in analysis
        assert "similar_situations" in analysis
        assert "risk_factors" in analysis

    def test_evaluate_actions(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test action evaluation."""
        memories = []
        analysis = {"patterns": [], "past_outcomes": {}, "similar_situations": [], "risk_factors": []}

        scores = memory_decisions._evaluate_actions(
            decision_context.available_actions,
            decision_context,
            memories,
            analysis
        )

        assert isinstance(scores, list)
        assert len(scores) == len(decision_context.available_actions)
        assert all(isinstance(score, tuple) and len(score) == 2 for score in scores)

        # Should be sorted by score descending
        if len(scores) > 1:
            assert scores[0][1] >= scores[1][1]

    def test_action_scoring_range(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test action scores are in valid range."""
        memories = []
        analysis = {"patterns": [], "past_outcomes": {}, "similar_situations": [], "risk_factors": []}

        scores = memory_decisions._evaluate_actions(
            decision_context.available_actions,
            decision_context,
            memories,
            analysis
        )

        for action, score in scores:
            assert 0.0 <= score <= 1.0, f"Score {score} for {action} not in range [0, 1]"

    def test_select_action(self, memory_decisions: MemoryAugmentedDecisions):
        """Test action selection."""
        action_scores = [
            ("action1", 0.8),
            ("action2", 0.6),
            ("action3", 0.9)
        ]

        action, confidence = memory_decisions._select_action(action_scores)

        assert action == "action3"  # Highest score
        assert confidence == 0.9

    def test_select_empty_actions(self, memory_decisions: MemoryAugmentedDecisions):
        """Test action selection with empty list."""
        action, confidence = memory_decisions._select_action([])

        assert action == "no_action"
        assert confidence == 0.0

    def test_reasoning_generation(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test reasoning generation."""
        memories = [{"content": "test"}]
        analysis = {
            "patterns": ["pattern1"],
            "past_outcomes": {"successful": []},
            "similar_situations": [],
            "risk_factors": []
        }

        reasoning = memory_decisions._generate_reasoning(
            "test_action",
            decision_context,
            memories,
            analysis
        )

        assert reasoning is not None
        assert len(reasoning) > 0
        assert "test_action" in reasoning

    def test_learn_from_outcome(self, memory_decisions: MemoryAugmentedDecisions):
        """Test learning from outcomes."""
        outcome = {"result": "success", "value": 10}

        memory_decisions.learn_from_outcome(
            action="test_action",
            outcome=outcome,
            success=True
        )

        # Should not raise an error
        # In full implementation, would update procedural memory

    def test_learn_from_failure(self, memory_decisions: MemoryAugmentedDecisions):
        """Test learning from failures."""
        outcome = {"result": "failure", "error": "invalid action"}

        memory_decisions.learn_from_outcome(
            action="bad_action",
            outcome=outcome,
            success=False
        )

        # Should not raise an error

    def test_get_decision_history(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test retrieving decision history."""
        memory_decisions.make_decision(decision_context)
        memory_decisions.make_decision(decision_context)

        history = memory_decisions.get_decision_history()

        assert isinstance(history, list)
        assert len(history) >= 2

        # Should be a copy, not the same object
        assert history is not memory_decisions.decision_history

    def test_get_statistics_empty(self):
        """Test statistics with no decisions."""
        mad = MemoryAugmentedDecisions()
        stats = mad.get_statistics()

        assert stats["total_decisions"] == 0
        assert stats["average_confidence"] == 0.0
        assert "strategy" in stats

    def test_get_statistics_with_decisions(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test statistics after making decisions."""
        # Make multiple decisions
        for _ in range(5):
            memory_decisions.make_decision(decision_context)

        stats = memory_decisions.get_statistics()

        assert stats["total_decisions"] == 5
        assert 0.0 <= stats["average_confidence"] <= 1.0


class TestDecisionStrategies:
    """Test different decision strategies."""

    def test_experience_based_strategy(self, decision_context: DecisionContext):
        """Test experience-based decision making."""
        mad = MemoryAugmentedDecisions(strategy=DecisionStrategy.EXPERIENCE_BASED)
        result = mad.make_decision(decision_context)

        assert result.chosen_action is not None

    def test_pattern_recognition_strategy(self, decision_context: DecisionContext):
        """Test pattern recognition strategy."""
        mad = MemoryAugmentedDecisions(strategy=DecisionStrategy.PATTERN_RECOGNITION)
        result = mad.make_decision(decision_context)

        assert result.chosen_action is not None

    def test_contextual_strategy(self, decision_context: DecisionContext):
        """Test contextual strategy."""
        mad = MemoryAugmentedDecisions(strategy=DecisionStrategy.CONTEXTUAL)
        result = mad.make_decision(decision_context)

        assert result.chosen_action is not None

    def test_hybrid_strategy(self, decision_context: DecisionContext):
        """Test hybrid strategy."""
        mad = MemoryAugmentedDecisions(strategy=DecisionStrategy.HYBRID)
        result = mad.make_decision(decision_context)

        assert result.chosen_action is not None

    def test_strategies_produce_results(
        self,
        all_decision_strategies: DecisionStrategy,
        decision_context: DecisionContext
    ):
        """Test all strategies produce valid results."""
        mad = MemoryAugmentedDecisions(strategy=all_decision_strategies)
        result = mad.make_decision(decision_context)

        assert isinstance(result, DecisionResult)
        assert result.chosen_action is not None


class TestMemoryIntegration:
    """Test integration with memory systems."""

    def test_memory_system_storage(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext,
        mock_memory_system
    ):
        """Test that decisions are stored in memory."""
        memory_decisions.make_decision(decision_context)

        # Check that episodic storage was called
        assert mock_memory_system.store_episodic.called

    def test_procedural_memory_update(self, memory_decisions: MemoryAugmentedDecisions):
        """Test procedural memory is updated."""
        outcome = {"result": "success"}

        memory_decisions.learn_from_outcome(
            action="test_action",
            outcome=outcome,
            success=True
        )

        # In full implementation, would update procedural memory
        # For now, just ensure no errors

    def test_memory_retrieval_used(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext,
        mock_memory_system
    ):
        """Test that memory retrieval is used during decision making."""
        memory_decisions.make_decision(decision_context)

        # Check that retrieve was called
        assert mock_memory_system.retrieve.called


class TestDecisionContextConversion:
    """Test context to query conversion."""

    def test_context_to_query(self, memory_decisions: MemoryAugmentedDecisions):
        """Test converting context to query."""
        context = DecisionContext(
            current_situation={
                "input": "test input",
                "user": "test_user"
            },
            available_actions=["action1"]
        )

        query = memory_decisions._context_to_query(context)

        assert isinstance(query, str)
        assert len(query) > 0


class TestActionScoring:
    """Test action scoring logic."""

    def test_score_calculation_components(
        self,
        memory_decisions: MemoryAugmentedDecisions,
        decision_context: DecisionContext
    ):
        """Test individual components of score calculation."""
        action = "test_action"
        memories = []
        analysis = {"risk_factors": []}

        # Test base score
        score = memory_decisions._calculate_action_score(
            action,
            decision_context,
            memories,
            analysis
        )

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_goal_alignment_scoring(self, memory_decisions: MemoryAugmentedDecisions):
        """Test goal alignment in scoring."""
        context = DecisionContext(
            current_situation={},
            available_actions=["helpful_action"],
            goals=["assist_user"]
        )

        alignment = memory_decisions._check_goal_alignment(
            "helpful_action",
            context.goals
        )

        assert isinstance(alignment, float)
        assert 0.0 <= alignment <= 1.0

    def test_constraint_violation_scoring(self, memory_decisions: MemoryAugmentedDecisions):
        """Test constraint violation in scoring."""
        constraints = {"max_time": 60}

        violation = memory_decisions._check_constraints(
            "quick_action",
            constraints
        )

        assert isinstance(violation, float)
        assert violation >= 0.0

    def test_risk_assessment_scoring(self, memory_decisions: MemoryAugmentedDecisions):
        """Test risk assessment in scoring."""
        risk_factors = ["high_complexity", "low_resources"]

        risk = memory_decisions._assess_action_risk(
            "risky_action",
            risk_factors
        )

        assert isinstance(risk, float)
        assert risk >= 0.0


class TestDecisionResult:
    """Test DecisionResult dataclass."""

    def test_decision_result_creation(self):
        """Test creating a decision result."""
        result = DecisionResult(
            chosen_action="test_action",
            confidence=0.8,
            reasoning="Test reasoning",
            relevant_memories=[],
            alternative_actions=[("action1", 0.7), ("action2", 0.5)]
        )

        assert result.chosen_action == "test_action"
        assert result.confidence == 0.8
        assert result.reasoning == "Test reasoning"
        assert result.relevant_memories == []
        assert len(result.alternative_actions) == 2


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_situation(self):
        """Test decision with empty situation."""
        context = DecisionContext(
            current_situation={},
            available_actions=["action1"]
        )

        mad = MemoryAugmentedDecisions()
        result = mad.make_decision(context)

        assert result is not None

    def test_single_action(self):
        """Test decision with single action."""
        context = DecisionContext(
            current_situation={"test": "value"},
            available_actions=["only_action"]
        )

        mad = MemoryAugmentedDecisions()
        result = mad.make_decision(context)

        assert result.chosen_action == "only_action"

    def test_many_actions(self):
        """Test decision with many available actions."""
        actions = [f"action_{i}" for i in range(100)]

        context = DecisionContext(
            current_situation={"test": "value"},
            available_actions=actions
        )

        mad = MemoryAugmentedDecisions()
        result = mad.make_decision(context)

        assert result.chosen_action in actions

    def test_extreme_confidence_values(self):
        """Test handling of extreme confidence values."""
        context = DecisionContext(
            current_situation={"test": "value"},
            available_actions=["action1"]
        )

        mad = MemoryAugmentedDecisions()

        # Make many decisions to test confidence ranges
        confidences = []
        for _ in range(10):
            result = mad.make_decision(context)
            confidences.append(result.confidence)

        # All should be in valid range
        assert all(0.0 <= c <= 1.0 for c in confidences)


class TestMemoryFallback:
    """Test fallback behavior when memory is unavailable."""

    @patch('character_agent_integration.memory.decisions.HIERARCHICAL_MEMORY_AVAILABLE', False)
    def test_fallback_memory_system(self):
        """Test fallback to simple memory system."""
        mad = MemoryAugmentedDecisions()

        context = DecisionContext(
            current_situation={"test": "value"},
            available_actions=["action1"]
        )

        # Should still work with fallback
        result = mad.make_decision(context)
        assert result is not None

    def test_simple_retrieval(self, memory_decisions: MemoryAugmentedDecisions):
        """Test simple memory retrieval fallback."""
        context = DecisionContext(
            current_situation={"test": "value"},
            available_actions=["action1"]
        )

        memories = memory_decisions._simple_retrieval(context)

        assert isinstance(memories, list)
