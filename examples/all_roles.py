"""
All Agent Roles Example

Demonstrates all 8 available agent roles with their unique characteristics.
"""

from character_agent_integration import create_character_agent


def demonstrate_role(role_name: str, description: str, example_input: str):
    """Demonstrate a specific agent role."""
    print(f"\n{'=' * 70}")
    print(f"Role: {role_name}")
    print(f"Description: {description}")
    print('=' * 70)

    agent = create_character_agent(
        role=role_name.lower(),
        personality={
            "openness": 0.7,
            "conscientiousness": 0.7,
            "extraversion": 0.6,
            "agreeableness": 0.7,
            "neuroticism": 0.3
        }
    )

    print(f"\nUser: {example_input}")
    result = agent.interact(example_input)
    print(f"{role_name}: {result.response}\n")


def main():
    """Demonstrate all agent roles."""
    print("=" * 70)
    print("Character-Agent Integration: All 8 Agent Roles")
    print("=" * 70)

    # 1. Conversation Partner
    demonstrate_role(
        "ConversationPartner",
        "Casual, friendly conversationalist with wit and humor",
        "Hey! How's your day going?"
    )

    # 2. Mentor
    demonstrate_role(
        "Mentor",
        "Wise guide providing thoughtful advice and perspective",
        "I'm at a crossroads in my career and need guidance"
    )

    # 3. Collaborator
    demonstrate_role(
        "Collaborator",
        "Cooperative team player focused on shared goals",
        "Let's work together to solve this problem"
    )

    # 4. Analyst
    demonstrate_role(
        "Analyst",
        "Logical thinker who breaks down problems systematically",
        "Can you analyze this situation for me?"
    )

    # 5. Creator
    demonstrate_role(
        "Creator",
        "Innovative generator of new ideas and content",
        "I need some creative ideas for a project"
    )

    # 6. Companion
    demonstrate_role(
        "Companion",
        "Emotionally supportive presence focused on wellbeing",
        "I'm feeling a bit down today"
    )

    # 7. Teacher
    demonstrate_role(
        "Teacher",
        "Educational guide focused on learning and understanding",
        "Can you explain how this works?"
    )

    # 8. Leader
    demonstrate_role(
        "Leader",
        "Directive and motivating presence driving toward goals",
        "We need to get started on this initiative"
    )

    print("\n" + "=" * 70)
    print("All roles demonstrated!")
    print("=" * 70)


if __name__ == "__main__":
    main()
