from social_agents.agents.agent import Agent
import os

name = "Calculator"
persona = "good at calculating number of letter 'r' in a given text"
with open(os.path.join(os.getcwd(), "prompts", "system_prompt.txt"), "r") as file:
    system_prompt = file.read()
with open(os.path.join(os.getcwd(), "prompts", "user_prompt.txt"), "r") as file:
    user_prompt = file.read()

def test_rs_1():
    agent = Agent(name, persona, system_prompt, user_prompt, [])
    user_input = "Strawberry"
    response = agent.respond(user_input)
    assert response == 3

def test_rs_2():
    agent = Agent(name, persona, system_prompt, user_prompt, [])
    user_input = "Strawberrry"
    response = agent.respond(user_input)
    assert response == 4

def test_rs_3():
    agent = Agent(name, persona, system_prompt, user_prompt, [])
    user_input = "Strawberrrrrrrrrrrrrrrry"
    response = agent.respond(user_input)
    assert response == 17

def test_rs_4():
    agent = Agent(name, persona, system_prompt, user_prompt, [])
    user_input = "Strawbey"
    response = agent.respond(user_input)
    assert response == 1

def test_rs_5():
    agent = Agent(name, persona, system_prompt, user_prompt, [])
    user_input = "Stawbey"
    response = agent.respond(user_input)
    assert response == 0
