"""
Basic Usage Example for Character-Agent Integration

This example demonstrates the core functionality of creating and using
character-driven AI agents.
"""

from character_agent_integration import create_character_agent


def main():
    """Demonstrate basic character agent usage."""
    print("=" * 60)
    print("Character-Agent Integration: Basic Usage Example")
    print("=" * 60)
    print()

    # Example 1: Create a Mentor Agent
    print("Example 1: Creating a Mentor Agent")
    print("-" * 60)

    mentor = create_character_agent(
        role="mentor",
        personality={
            "openness": 0.8,
            "conscientiousness": 0.9,
            "extraversion": 0.5,
            "agreeableness": 0.8,
            "neuroticism": 0.3
        },
        emotions={
            "joy": 0.5,
            "trust": 0.7,
            "anticipation": 0.4
        }
    )

    # Interact with the mentor
    user_inputs = [
        "I'm struggling with a career decision",
        "What do you think about taking risks?",
        "I feel uncertain about my future"
    ]

    for user_input in user_inputs:
        print(f"\nUser: {user_input}")
        result = mentor.interact(user_input)
        print(f"Mentor: {result.response}")
        print(f"  Emotional State: {result.emotional_state.get_dominant_emotion()[0]}")
        print(f"  Confidence: {result.confidence:.2f}")

    print("\n" + "=" * 60)

    # Example 2: Create a Companion Agent
    print("\nExample 2: Creating a Companion Agent")
    print("-" * 60)

    companion = create_character_agent(
        role="companion",
        personality={
            "openness": 0.7,
            "conscientiousness": 0.6,
            "extraversion": 0.5,
            "agreeableness": 0.9,
            "neuroticism": 0.3
        }
    )

    user_inputs = [
        "I had a really hard day",
        "Sometimes I feel lonely",
        "Thanks for listening to me"
    ]

    for user_input in user_inputs:
        print(f"\nUser: {user_input}")
        result = companion.interact(user_input)
        print(f"Companion: {result.response}")

    print("\n" + "=" * 60)

    # Example 3: Check Agent State
    print("\nExample 3: Checking Agent State")
    print("-" * 60)

    state = mentor.get_agent_state()
    print(f"Personality Traits:")
    for trait, value in state['personality_state'].items():
        print(f"  {trait}: {value:.2f}")

    print(f"\nMemory Statistics:")
    for key, value in state['memory_statistics'].items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
