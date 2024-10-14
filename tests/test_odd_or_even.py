from social_agents.agents.agent import Agent
import os

name = "Calculator"
persona = "good at judging whether an integer is odd or even"
with open(os.path.join(os.getcwd(), "prompts", "system_prompt.txt"), "r") as file:
    system_prompt = file.read()
with open(os.path.join(os.getcwd(), "prompts", "user_prompt.txt"), "r") as file:
    user_prompt = file.read()

def test_odd_or_even_1():
    agent = Agent(name, persona, system_prompt, user_prompt)
    user_inputs = ["1", "2", "3"]
    responses = [0, 1, 0]
    for user_input, response in zip(user_inputs, responses):
        result = agent.respond(user_input)
        assert result == response

def test_odd_or_even_2():
    agent = Agent(name, persona, system_prompt, user_prompt)
    user_inputs = ["4", "5", "6"]
    responses = [1, 0, 1]
    for user_input, response in zip(user_inputs, responses):
        result = agent.respond(user_input)
        assert result == response

