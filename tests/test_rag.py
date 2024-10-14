from social_agents.agents.agent import Agent
import os

name = "Calculator"
persona = "good at judging whether an integer is odd or even"
with open(os.path.join(os.getcwd(), "prompts", "system_prompt.txt"), "r") as file:
    system_prompt = file.read()
with open(os.path.join(os.getcwd(), "prompts", "user_prompt.txt"), "r") as file:
    user_prompt = file.read()

background = [
    "Ocean",
    "Mountain",
    "Desert",
    "Forest",
    "Hamburger"
]

def test_rag_1():
    agent = Agent(name, persona, system_prompt, user_prompt, background)
    user_input = "water"
    result = agent.rag(user_input)
    assert result == "Ocean"

def test_rag_2():
    agent = Agent(name, persona, system_prompt, user_prompt, background)
    user_input = "trees"
    result = agent.rag(user_input)
    assert result == "Forest"

def test_rag_3():
    agent = Agent(name, persona, system_prompt, user_prompt, background)
    user_input = "sand"
    result = agent.rag(user_input)
    assert result == "Desert"

def test_rag_4():
    agent = Agent(name, persona, system_prompt, user_prompt, background)
    user_input = "hill"
    result = agent.rag(user_input)
    assert result == "Mountain"

def test_rag_5():
    agent = Agent(name, persona, system_prompt, user_prompt, background)
    user_input = "food"
    result = agent.rag(user_input)
    assert result == "Hamburger"

