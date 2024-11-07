import sys
import os

# Get the absolute path of the root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the root directory to the sys.path
sys.path.append(root_dir)

from social_agents.agents.agent import Agent
import json

with open('system_prompt.txt', 'r') as file:
    system_prompt = file.read()

with open('user_prompt.txt', 'r') as file:
    user_prompt = file.read()

with open('agents.json', 'r') as file:
    agents = json.load(file)

# Initialize the three agents
agent1 = Agent(agents[0]['name'], agents[0]['persona'], system_prompt, user_prompt)
agent2 = Agent(agents[1]['name'], agents[1]['persona'], system_prompt, user_prompt)
agent3 = Agent(agents[2]['name'], agents[2]['persona'], system_prompt, user_prompt)

def beautiful_print(agent_name, response):
    print()
    print(f"{agent_name} says:", response['content'])
    if response['make_decision']:
        print(f"{agent_name} makes a decision:", response['decision'])
    else:
        print(f"{agent_name} does not make a decision yet.")
    print()

# Initial messages from agents
agent1_response = {
    "content": "You have also heard about the fire right?",
    "make_decision": False,
    "decision": "Pending"
}
agent1.memory.append({"content": str(agent1_response), "role": "assistant"})

agent2_response = {
    "content": "Yes, I have heard about the fire.",
    "make_decision": False,
    "decision": "Pending"
}
agent2.memory.append({"content": str(agent1_response), "role": "user"})
agent2.memory.append({"content": str(agent2_response), "role": "assistant"})

# Agent 3 has not responded yet
agent3_response = None

agent1_made_decision = agent1_response['make_decision']
agent2_made_decision = agent2_response['make_decision']
agent3_made_decision = False  # Agent 3 has not made any decision yet

def build_flowing_words(agent1_response, agent2_response, agent3_response):
    flowing_words = {}
    # For agent1
    messages = []
    if agent2_response:
        if agent2_response['make_decision']:
            messages.append(f"Person 2 has made a decision: {agent2_response['decision']} and said: {agent2_response['content']}")
        else:
            messages.append(f"Person 2 said: {agent2_response['content']}")
    if agent3_response:
        if agent3_response['make_decision']:
            messages.append(f"Person 3 has made a decision: {agent3_response['decision']} and said: {agent3_response['content']}")
        else:
            messages.append(f"Person 3 said: {agent3_response['content']}")
    flowing_words['agent1'] = '\n'.join(messages)

    # For agent2
    messages = []
    if agent1_response:
        if agent1_response['make_decision']:
            messages.append(f"Person 1 has made a decision: {agent1_response['decision']} and said: {agent1_response['content']}")
        else:
            messages.append(f"Person 1 said: {agent1_response['content']}")
    if agent3_response:
        if agent3_response['make_decision']:
            messages.append(f"Person 3 has made a decision: {agent3_response['decision']} and said: {agent3_response['content']}")
        else:
            messages.append(f"Person 3 said: {agent3_response['content']}")
    flowing_words['agent2'] = '\n'.join(messages)

    # For agent3
    messages = []
    if agent1_response:
        if agent1_response['make_decision']:
            messages.append(f"Person 1 has made a decision: {agent1_response['decision']} and said: {agent1_response['content']}")
        else:
            messages.append(f"Person 1 said: {agent1_response['content']}")
    if agent2_response:
        if agent2_response['make_decision']:
            messages.append(f"Person 2 has made a decision: {agent2_response['decision']} and said: {agent2_response['content']}")
        else:
            messages.append(f"Person 2 said: {agent2_response['content']}")
    flowing_words['agent3'] = '\n'.join(messages)

    return flowing_words

# Build initial flowing words
flowing_words = build_flowing_words(agent1_response, agent2_response, agent3_response)

while True:
    # Agent 3's turn
    agent3_response = agent3.respond(flowing_words['agent3'])
    beautiful_print(agent3.name, agent3_response)
    agent3_made_decision = agent3_response['make_decision']
    if agent1_made_decision and agent2_made_decision and agent3_made_decision:
        break

    # Update flowing words after Agent 3's response
    flowing_words = build_flowing_words(agent1_response, agent2_response, agent3_response)

    # Agent 1's turn
    agent1_response = agent1.respond(flowing_words['agent1'])
    beautiful_print(agent1.name, agent1_response)
    agent1_made_decision = agent1_response['make_decision']
    if agent1_made_decision and agent2_made_decision and agent3_made_decision:
        break

    # Update flowing words after Agent 1's response
    flowing_words = build_flowing_words(agent1_response, agent2_response, agent3_response)

    # Agent 2's turn
    agent2_response = agent2.respond(flowing_words['agent2'])
    beautiful_print(agent2.name, agent2_response)
    agent2_made_decision = agent2_response['make_decision']
    if agent1_made_decision and agent2_made_decision and agent3_made_decision:
        break

    # Update flowing words after Agent 2's response
    flowing_words = build_flowing_words(agent1_response, agent2_response, agent3_response)