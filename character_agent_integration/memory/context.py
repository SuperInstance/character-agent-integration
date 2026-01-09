"""
Contextual Memory Management

Manages contextual information for memory-augmented decision making.
Bridges between memory systems and agent interactions.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MemoryContext:
    """
    Context for memory operations.
    Captures the state and environment for memory storage/retrieval.
    """
    interaction_id: Optional[str] = None
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    emotional_state: Optional[Dict[str, float]] = None
    personality_state: Optional[Dict[str, float]] = None
    environment: Dict[str, Any] = field(default_factory=dict)
    goals: List[str] = field(default_factory=list)
    active_tasks: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "interaction_id": self.interaction_id,
            "timestamp": self.timestamp,
            "emotional_state": self.emotional_state,
            "personality_state": self.personality_state,
            "environment": self.environment,
            "goals": self.goals,
            "active_tasks": self.active_tasks
        }


class ContextualMemory:
    """
    Manages contextual memory for agent interactions.

    Tracks interaction context, emotional states, and environmental factors
    to provide rich context for memory operations.
    """

    def __init__(self, max_contexts: int = 1000):
        """
        Initialize contextual memory.

        Args:
            max_contexts: Maximum number of contexts to store
        """
        self.max_contexts = max_contexts
        self.contexts: List[MemoryContext] = []
        self.current_context: Optional[MemoryContext] = None

    def create_context(
        self,
        interaction_id: Optional[str] = None,
        emotional_state: Optional[Dict[str, float]] = None,
        personality_state: Optional[Dict[str, float]] = None,
        environment: Optional[Dict[str, Any]] = None
    ) -> MemoryContext:
        """
        Create a new memory context.

        Args:
            interaction_id: Optional interaction identifier
            emotional_state: Current emotional state
            personality_state: Current personality state
            environment: Environmental factors

        Returns:
            New MemoryContext object
        """
        context = MemoryContext(
            interaction_id=interaction_id,
            emotional_state=emotional_state,
            personality_state=personality_state,
            environment=environment or {}
        )

        self.current_context = context
        self.contexts.append(context)

        # Trim if necessary
        if len(self.contexts) > self.max_contexts:
            self.contexts = self.contexts[-self.max_contexts:]

        return context

    def update_context(
        self,
        emotional_state: Optional[Dict[str, float]] = None,
        personality_state: Optional[Dict[str, float]] = None,
        environment: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Update the current context.

        Args:
            emotional_state: New emotional state
            personality_state: New personality state
            environment: New environmental factors
        """
        if self.current_context is None:
            self.create_context(
                emotional_state=emotional_state,
                personality_state=personality_state,
                environment=environment
            )
        else:
            if emotional_state is not None:
                self.current_context.emotional_state = emotional_state
            if personality_state is not None:
                self.current_context.personality_state = personality_state
            if environment is not None:
                self.current_context.environment.update(environment)

    def get_current_context(self) -> Optional[MemoryContext]:
        """Get the current context."""
        return self.current_context

    def get_context_history(self, limit: int = 10) -> List[MemoryContext]:
        """
        Get recent context history.

        Args:
            limit: Maximum number of contexts to return

        Returns:
            List of recent contexts
        """
        return self.contexts[-limit:]

    def find_similar_contexts(
        self,
        context: MemoryContext,
        threshold: float = 0.7,
        limit: int = 5
    ) -> List[tuple[MemoryContext, float]]:
        """
        Find contexts similar to the given context.

        Args:
            context: Context to compare against
            threshold: Minimum similarity threshold
            limit: Maximum number of results

        Returns:
            List of (context, similarity_score) tuples
        """
        similar_contexts = []

        for ctx in self.contexts:
            if ctx == context:
                continue

            similarity = self._calculate_similarity(context, ctx)
            if similarity >= threshold:
                similar_contexts.append((ctx, similarity))

        # Sort by similarity descending
        similar_contexts.sort(key=lambda x: x[1], reverse=True)
        return similar_contexts[:limit]

    def _calculate_similarity(
        self,
        context1: MemoryContext,
        context2: MemoryContext
    ) -> float:
        """
        Calculate similarity between two contexts.

        Args:
            context1: First context
            context2: Second context

        Returns:
            Similarity score from 0.0 to 1.0
        """
        similarity = 0.0
        factors = 0

        # Compare emotional states
        if context1.emotional_state and context2.emotional_state:
            emotion_sim = self._compare_emotional_states(
                context1.emotional_state,
                context2.emotional_state
            )
            similarity += emotion_sim
            factors += 1

        # Compare personality states
        if context1.personality_state and context2.personality_state:
            personality_sim = self._compare_personality_states(
                context1.personality_state,
                context2.personality_state
            )
            similarity += personality_sim
            factors += 1

        # Compare environment
        env_sim = self._compare_environments(
            context1.environment,
            context2.environment
        )
        similarity += env_sim
        factors += 1

        return similarity / factors if factors > 0 else 0.0

    def _compare_emotional_states(
        self,
        state1: Dict[str, float],
        state2: Dict[str, float]
    ) -> float:
        """Compare emotional states."""
        if not state1 or not state2:
            return 0.0

        # Get common emotions
        common_emotions = set(state1.keys()) & set(state2.keys())
        if not common_emotions:
            return 0.0

        # Calculate average similarity
        total_diff = 0.0
        for emotion in common_emotions:
            diff = abs(state1[emotion] - state2[emotion])
            total_diff += diff

        avg_diff = total_diff / len(common_emotions)
        similarity = 1.0 - avg_diff
        return max(0.0, min(1.0, similarity))

    def _compare_personality_states(
        self,
        state1: Dict[str, float],
        state2: Dict[str, float]
    ) -> float:
        """Compare personality states."""
        return self._compare_emotional_states(state1, state2)

    def _compare_environments(
        self,
        env1: Dict[str, Any],
        env2: Dict[str, Any]
    ) -> float:
        """Compare environmental factors."""
        if not env1 or not env2:
            return 0.0

        # Check matching keys
        common_keys = set(env1.keys()) & set(env2.keys())
        if not common_keys:
            return 0.0

        matches = sum(1 for key in common_keys if env1[key] == env2[key])
        return matches / len(common_keys)

    def get_context_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored contexts."""
        if not self.contexts:
            return {
                "total_contexts": 0,
                "average_emotional_state": None,
                "most_common_emotions": []
            }

        # Aggregate statistics
        emotional_states = [
            ctx.emotional_state for ctx in self.contexts
            if ctx.emotional_state
        ]

        if emotional_states:
            # Calculate average emotional state
            avg_emotional = {}
            for state in emotional_states:
                for emotion, value in state.items():
                    if emotion not in avg_emotional:
                        avg_emotional[emotion] = []
                    avg_emotional[emotion].append(value)

            for emotion in avg_emotional:
                avg_emotional[emotion] = sum(avg_emotional[emotion]) / len(avg_emotional[emotion])

            # Get most common emotions
            emotion_frequency = {}
            for state in emotional_states:
                for emotion in state.keys():
                    emotion_frequency[emotion] = emotion_frequency.get(emotion, 0) + 1

            most_common = sorted(
                emotion_frequency.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        else:
            avg_emotional = None
            most_common = []

        return {
            "total_contexts": len(self.contexts),
            "average_emotional_state": avg_emotional,
            "most_common_emotions": most_common
        }

    def clear_old_contexts(self, keep_recent: int = 100) -> None:
        """
        Clear old contexts, keeping only recent ones.

        Args:
            keep_recent: Number of recent contexts to keep
        """
        if len(self.contexts) > keep_recent:
            self.contexts = self.contexts[-keep_recent:]
