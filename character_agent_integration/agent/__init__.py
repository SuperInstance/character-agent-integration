"""
Agent Role System

Defines 8 distinct agent roles with unique behavioral patterns and response styles.
Each role has specialized capabilities for different interaction scenarios.
"""

from .base import AgentRole, RoleType, RoleCapabilities
from .roles import (
    ConversationPartner,
    Mentor,
    Collaborator,
    Analyst,
    Creator,
    Companion,
    Teacher,
    Leader
)

__all__ = [
    "AgentRole",
    "RoleType",
    "RoleCapabilities",
    "ConversationPartner",
    "Mentor",
    "Collaborator",
    "Analyst",
    "Creator",
    "Companion",
    "Teacher",
    "Leader"
]
