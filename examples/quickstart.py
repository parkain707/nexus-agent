"""
Quickstart Example: Running Nexus-Agent in 5 lines of code.
"""

from nexus_agent import NexusAgent
from nexus_agent.core.schema import AgentConfig

# 1. Configure the agent (Uses offline Deterministic Mock by default for instant zero-key testing)
config = AgentConfig(provider="mock", max_iterations=10)

# 2. Initialize the agent
agent = NexusAgent(config=config)

# 3. Define the goal
goal = "Create a python file math_sample.py with a function to calculate fibonacci numbers and verify it."

# 4. Run autonomously
state = agent.run(goal)

# 5. Inspect final result
print(f"Status: {state.status}")
print(f"Summary: {state.final_output}")
