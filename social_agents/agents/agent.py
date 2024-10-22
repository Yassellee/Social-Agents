from typing import List, Dict
from social_agents.utils.llm_wrapper import json_chat, replace_prompt
from social_agents.utils.type_defs import OddOrEven, EvacuationDiscussion

class Agent:
    def __init__(self, name: str, persona: str, system_prompt: str, user_prompt: str):
        """
        Initialize the agent with a name, persona, system prompt, and user prompt.

        Args:
            name (str): The name of the agent.
            persona (str): The persona of the agent.
            system_prompt (str): The system prompt for the agent.
            user_prompt (str): The user prompt for the agent.

        Returns:
            None
        """
        self.name = name
        self.persona = persona
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

        self.memory = []
        # TODO: Use the name, persona and replace_prompt to fill in the system prompt, estimate 1 line
        
        # TODO: Initialize the agent's memory with the system prompt, estimate 1 line
        # Tip: The memory should be a list of dictionaries, each dictionary should have a "content" key and a "role" key
        

    def respond(self, user_input: str) -> int:
        """
        Respond to a user input.

        Args:
            user_input (str): The user input.

        Returns:
            int: If the response is even, return 1. If the response is odd, return 0.
            # TODO: if using EvacuationDiscussion, return type is dict
        """
        # TODO: Use the user input and replace_prompt to fill in the user prompt, estimate 1 line
        
        # TODO: Add the user prompt to the agent's memory, estimate 1 line
        
        # TODO: Use the memory, OddOrEven and json_chat to do three things:
        # 1. generate a response
        # 2. add the response to the memory
        # 3. return the function
        # estimate 6 lines
        
        # TODO: After you pass the test cases, use EvacuationDiscussion instead, add the response to the memory, return the response, estimate 3 lines
        
        
        