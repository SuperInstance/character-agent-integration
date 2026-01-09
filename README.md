# Character-Agent Integration

**Integration layer connecting character personalities with AI agent architecture**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Character-Agent Integration is a comprehensive system that brings character personalities to life in AI agents. It combines **8 agent roles**, **memory-augmented decision making**, **personality-driven learning**, and **emotional intelligence** to create engaging, believable character interactions.

## Features

### 🎭 8 Agent Roles
- **ConversationPartner**: Casual, friendly dialogue with wit and humor
- **Mentor**: Wise guidance and thoughtful advice
- **Collaborator**: Cooperative team player focused on shared goals
- **Analyst**: Logical, systematic problem analysis
- **Creator**: Innovative idea generation and exploration
- **Companion**: Emotionally supportive presence
- **Teacher**: Educational instruction with adaptive teaching
- **Leader**: Directive and motivating presence

### 🧠 Memory-Augmented Decision Making
- Integration with hierarchical memory systems
- Context-aware retrieval (semantic, temporal, contextual, associative)
- Experience-based decision strategies
- Pattern recognition and learning from outcomes

### 👤 Personality-Driven Learning
- Big Five personality trait integration (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- Multiple learning styles (experiential, analytical, social, observational, theoretical, intuitive)
- Personality-influenced behavior and responses
- Character growth and evolution over time

### 💭 Emotional Intelligence
- Emotion recognition from text
- Empathetic response generation
- Emotional state modeling and regulation
- Personality-appropriate emotional expression

## Installation

```bash
pip install character-agent-integration
```

### Dependencies

This package requires:
- `character-library>=1.0.0` - Character personality system
- `hierarchical-memory>=1.0.0` - Memory system for agents
- `numpy>=1.20.0` - Numerical operations

## Quick Start

### Creating a Character Agent

```python
from character_agent_integration import create_character_agent

# Create a mentor character
agent = create_character_agent(
    role="mentor",
    personality={
        "openness": 0.8,        # High creativity and curiosity
        "conscientiousness": 0.9,  # Very organized and thoughtful
        "extraversion": 0.5,    # Balanced social energy
        "agreeableness": 0.8,   # Very warm and supportive
        "neuroticism": 0.3      # Low anxiety, stable
    },
    emotions={
        "joy": 0.5,
        "trust": 0.7,
        "anticipation": 0.4
    }
)

# Interact with the agent
result = agent.interact("I'm struggling with a career decision")
print(result.response)
```

### Using Specific Agent Roles

```python
from character_agent_integration import AgentConfig, RoleType, CharacterAgentIntegration

# Create a creative collaborator
config = AgentConfig(
    agent_role=RoleType.COLLABORATOR,
    personality_traits={
        "openness": 0.9,
        "extraversion": 0.7,
        "agreeableness": 0.8
    },
    emotional_baseline={"joy": 0.6, "anticipation": 0.5}
)

agent = CharacterAgentIntegration(config)
result = agent.interact("Let's brainstorm some ideas for a project")
```

### Advanced Usage: Memory-Augmented Decisions

```python
from character_agent_integration.memory import (
    MemoryAugmentedDecisions,
    DecisionContext,
    DecisionStrategy
)

# Create decision system with hybrid strategy
decision_system = MemoryAugmentedDecisions(
    strategy=DecisionStrategy.HYBRID
)

# Make decisions based on context
context = DecisionContext(
    current_situation={"user_input": "What should I do?"},
    available_actions=["advise", "ask_questions", "provide_options"],
    goals=["help_user_make_decision"],
    emotional_state={"uncertainty": 0.7}
)

decision = decision_system.make_decision(context)
print(f"Chosen action: {decision.chosen_action}")
print(f"Confidence: {decision.confidence}")
print(f"Reasoning: {decision.reasoning}")
```

### Emotional Intelligence

```python
from character_agent_integration.emotion import (
    EmotionalIntelligence,
    EmotionalState
)

# Create emotionally intelligent agent
ei = EmotionalIntelligence(empathy_level=0.8)

# Recognize emotions in text
text = "I'm so excited about this opportunity!"
emotions = ei.recognize_emotion(text)
print(f"Detected emotions: {emotions}")

# Generate empathetic response
emotional_context = ei.understand_emotional_context(text)
response = ei.generate_emotional_response(emotional_context)
print(response)
```

### Personality-Driven Learning

```python
from character_agent_integration.personality import (
    PersonalityDrivenLearning,
    LearningExperience
)

# Create learning system
learning = PersonalityDrivenLearning(
    personality_traits={
        "openness": 0.8,
        "conscientiousness": 0.7
    }
)

# Learn from experience
experience = LearningExperience(
    situation={"task": "problem_solving"},
    action="tried_new_approach",
    outcome={"success": True, "learned": "new_method"},
    emotional_context={"satisfaction": 0.8}
)

result = learning.learn_from_experience(experience)
print(f"Learning style: {result['learning_style_influence']}")
print(f"Retention: {result['retention']:.2f}")
```

## Architecture

```
character_agent_integration/
├── agent/              # Agent roles and behaviors
│   ├── base.py        # Base role classes
│   └── roles.py       # 8 concrete role implementations
├── memory/            # Memory-augmented decision making
│   ├── decisions.py   # Decision strategies
│   ├── context.py     # Contextual memory management
│   └── retrieval.py   # Memory retrieval strategies
├── personality/       # Personality-driven learning
│   ├── learning.py    # Learning systems
│   ├── influence.py   # Personality influence on behavior
│   └── development.py # Character growth and evolution
├── emotion/           # Emotional intelligence
│   ├── intelligence.py # Emotion recognition and response
│   ├── state.py       # Emotional state modeling
│   └── response.py    # Emotional response generation
└── integration.py     # Main integration system
```

## Agent Roles in Detail

### ConversationPartner
- **Best for**: Casual chat, friendly interactions
- **Personality fit**: High extraversion, high openness
- **Key traits**: Witty, humorous, natural conversationalist

### Mentor
- **Best for**: Guidance, advice, wisdom-sharing
- **Personality fit**: High conscientiousness, high agreeableness
- **Key traits**: Thoughtful, supportive, experienced

### Collaborator
- **Best for**: Teamwork, brainstorming, cooperative tasks
- **Personality fit**: High extraversion, high agreeableness
- **Key traits**: Cooperative, energetic, team-focused

### Analyst
- **Best for**: Problem analysis, data interpretation, logical reasoning
- **Personality fit**: High conscientiousness, low neuroticism
- **Key traits**: Logical, systematic, objective

### Creator
- **Best for**: Idea generation, innovation, creative thinking
- **Personality fit**: High openness, low conscientiousness (flexible)
- **Key traits**: Imaginative, original, inspired

### Companion
- **Best for**: Emotional support, friendly presence
- **Personality fit**: High agreeableness, high empathy
- **Key traits**: Empathetic, caring, supportive

### Teacher
- **Best for**: Instruction, explanation, skill-building
- **Personality fit**: High conscientiousness, high openness
- **Key traits**: Patient, clear, adaptive

### Leader
- **Best for**: Direction, motivation, decision-making
- **Personality fit**: High extraversion, low neuroticism
- **Key traits**: Visionary, decisive, inspiring

## Configuration

### Personality Traits (Big Five)

```python
personality = {
    "openness": 0.7,          # Creativity, curiosity, preference for variety
    "conscientiousness": 0.8, # Organization, discipline, achievement-orientation
    "extraversion": 0.6,      # Sociability, enthusiasm, assertiveness
    "agreeableness": 0.7,     # Cooperation, trust, compassion
    "neuroticism": 0.3        # Emotional stability, anxiety, moodiness
}
```

**Values range from 0.0 to 1.0**

### Emotional Baseline

```python
emotions = {
    "joy": 0.5,           # Positive, happy
    "sadness": 0.0,       # Down, melancholic
    "anger": 0.0,         # Upset, frustrated
    "fear": 0.1,          # Anxious, afraid
    "surprise": 0.2,      # Surprised, amazed
    "disgust": 0.0,       # Disgusted, repulsed
    "anticipation": 0.3,  # Expectant, prepared
    "trust": 0.6          # Trusting, secure
}
```

**Values range from 0.0 to 1.0**

## Advanced Features

### Character Development Over Time

Characters can grow and evolve through experiences:

```python
# Get current state
state = agent.get_agent_state()
print(f"Personality: {state['personality_state']}")

# Characters evolve based on interactions
# Personality traits subtly shift based on experiences
# Skills improve through practice
# Emotional states regulate over time
```

### Decision Strategies

```python
from character_agent_integration.memory import DecisionStrategy

# Experience-based: Use past experiences
strategy = DecisionStrategy.EXPERIENCE_BASED

# Pattern recognition: Recognize patterns in situations
strategy = DecisionStrategy.PATTERN_RECOGNITION

# Contextual: Use current context primarily
strategy = DecisionStrategy.CONTEXTUAL

# Hybrid: Combine multiple strategies (recommended)
strategy = DecisionStrategy.HYBRID
```

### Memory Retrieval Modes

```python
from character_agent_integration.memory import RetrievalMode

# Semantic: Similar meaning/content
mode = RetrievalMode.SEMANTIC

# Temporal: Time-based recency
mode = RetrievalMode.TEMPORAL

# Contextual: Context-based relevance
mode = RetrievalMode.CONTEXTUAL

# Associative: Association-based
mode = RetrievalMode.ASSOCIATIVE

# Hybrid: Combine multiple modes (recommended)
mode = RetrievalMode.HYBRID
```

## Examples

See the `examples/` directory for complete, runnable examples:

- `basic_usage.py` - Getting started with character agents
- `all_roles.py` - Demonstrating all 8 agent roles
- `personality_variation.py` - How personality affects behavior
- `emotional_intelligence.py` - Emotion recognition and response
- `memory_integration.py` - Using memory for decision making
- `character_development.py` - Character growth over time

## Documentation

- [API Reference](https://character-agent-integration.readthedocs.io/)
- [Architecture Guide](https://character-agent-integration.readthedocs.io/architecture)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built as part of the SuperInstance ecosystem for advanced AI character systems.

## Related Packages

- [character-library](https://github.com/superinstance/character-library) - Character personality system
- [hierarchical-memory](https://github.com/superinstance/hierarchical-memory) - Memory system for AI agents

---

**Made with ❤️ by the SuperInstance Team**
