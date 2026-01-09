"""
Personality Variation Example

Demonstrates how different personality traits affect agent behavior.
"""

from character_agent_integration import create_character_agent


def create_agent_with_personality(name: str, traits: dict):
    """Create an agent with specific personality traits."""
    return create_character_agent(
        role="conversation_partner",
        personality=traits
    )


def main():
    """Demonstrate personality variations."""
    print("=" * 70)
    print("Character-Agent Integration: Personality Variation Example")
    print("=" * 70)
    print()

    # Define different personality profiles
    personalities = {
        "Highly Creative": {
            "openness": 0.95,
            "conscientiousness": 0.4,
            "extraversion": 0.6,
            "agreeableness": 0.7,
            "neuroticism": 0.3
        },
        "Very Organized": {
            "openness": 0.5,
            "conscientiousness": 0.95,
            "extraversion": 0.5,
            "agreeableness": 0.6,
            "neuroticism": 0.2
        },
        "Highly Social": {
            "openness": 0.7,
            "conscientiousness": 0.6,
            "extraversion": 0.95,
            "agreeableness": 0.8,
            "neuroticism": 0.3
        },
        "Very Agreeable": {
            "openness": 0.6,
            "conscientiousness": 0.6,
            "extraversion": 0.5,
            "agreeableness": 0.95,
            "neuroticism": 0.2
        },
        "Balanced": {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }
    }

    # Test input
    test_input = "I'm thinking about trying something new and different"

    # Create and test each personality
    agents = {}
    for name, traits in personalities.items():
        print(f"\n{'=' * 70}")
        print(f"Personality: {name}")
        print('-' * 70)
        print("Traits:")
        for trait, value in traits.items():
            print(f"  {trait.capitalize()}: {value:.2f}")
        print()

        agent = create_agent_with_personality(name, traits)
        agents[name] = agent

        result = agent.interact(test_input)
        print(f"\nUser: {test_input}")
        print(f"{name}: {result.response}")

    # Compare responses
    print("\n" + "=" * 70)
    print("Summary: How Personality Affects Responses")
    print("=" * 70)

    print("""
Key Observations:
- High Openness: More enthusiastic about novelty and exploration
- High Conscientiousness: More structured and analytical responses
- High Extraversion: More energetic and socially engaged
- High Agreeableness: More supportive and empathetic
- Balanced Personality: Moderate, well-rounded responses

Personality traits influence:
1. Word choice and phrasing
2. Emotional expression
3. Decision-making style
4. Learning approach
5. Response patterns
    """)

    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
