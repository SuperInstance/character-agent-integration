"""
Character Development

Manages character growth and evolution over time.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class DevelopmentMilestone:
    """A milestone in character development."""
    milestone_type: str
    description: str
    timestamp: float
    personality_changes: Dict[str, float]
    skill_improvements: Dict[str, float]


class CharacterDevelopment:
    """Manages character growth and evolution."""

    def __init__(self, initial_personality: Dict[str, float]):
        """
        Initialize character development system.

        Args:
            initial_personality: Starting personality traits
        """
        self.personality = initial_personality.copy()
        self.milestones: List[DevelopmentMilestone] = []
        self.development_history: List[Dict[str, Any]] = []

    def add_milestone(
        self,
        milestone_type: str,
        description: str,
        personality_changes: Dict[str, float],
        skill_improvements: Optional[Dict[str, float]] = None
    ) -> None:
        """Add a development milestone."""
        milestone = DevelopmentMilestone(
            milestone_type=milestone_type,
            description=description,
            timestamp=field(default=lambda: __import__("time").time()),
            personality_changes=personality_changes,
            skill_improvements=skill_improvements or {}
        )

        self.milestones.append(milestone)
        self._apply_personality_changes(personality_changes)

    def _apply_personality_changes(self, changes: Dict[str, float]) -> None:
        """Apply personality changes."""
        for trait, change in changes.items():
            current = self.personality.get(trait, 0.5)
            new_value = max(0.0, min(1.0, current + change))
            self.personality[trait] = new_value

    def get_development_summary(self) -> Dict[str, Any]:
        """Get summary of character development."""
        return {
            "current_personality": self.personality,
            "total_milestones": len(self.milestones),
            "recent_milestones": self.milestones[-5:]
        }
