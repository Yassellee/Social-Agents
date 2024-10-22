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

agent1 = None
agent2 = None
# TODO: Initialize the two agents, estimate 2 liens
agent1 = Agent(agents[0]['name'], agents[0]['persona'], system_prompt, user_prompt)
agent2 = Agent(agents[1]['name'], agents[1]['persona'], system_prompt, user_prompt)

def beautiful_print(agent_name, response):
    print()
    print(f"{agent_name} says:", response['content'])
    if response['make_decision']:
        print(f"{agent_name} makes a decision:", response['decision'])
    else:
        print(f"{agent_name} does not make a decision yet.")
    print()

# Initial question from agent1
agent1_mimic_question = {
    "content": "You have also heard about the fire right?",
    "make_decision": False,
    "decision": "Pending"
}
agent1.memory.append({"content": str(agent1_mimic_question), "role": "assistant"})
agent1_made_decision = False
agent2_made_decision = False
flowing_words = ""
# TODO: Please fill in the flowing_words with something, hints are already in the code, estimate 1 line
flowing_words = agent1_mimic_question['content']

while True:
    # TODO: Get the response from agent2, estimate 1 line
    agent2_response = agent2.respond(flowing_words)
    beautiful_print(agent2.name, agent2_response)
    agent2_made_decision = agent2_response['make_decision']
    if agent1_made_decision and agent2_made_decision:
        break
    if agent2_made_decision:
        flowing_words = f"The other person has made a decision: {agent2_response['decision']} and also left a message: {agent2_response['content']}"
    else:
        flowing_words = agent2_response['content']
    # TODO: Get the response from agent1, estimate 1 line
    agent1_response = agent1.respond(flowing_words)
    beautiful_print(agent1.name, agent1_response)
    agent1_made_decision = agent1_response['make_decision']
    if agent1_made_decision and agent2_made_decision:
        break
    if agent1_made_decision:
        flowing_words = f"The other person has made a decision: {agent1_response['decision']} and also left a message: {agent1_response['content']}"
    else:
        flowing_words = agent1_response['content']
