from typing import List, Dict
from social_agents.utils.llm_wrapper import json_chat, replace_prompt, vectorize
from social_agents.utils.type_defs import NumberOfRs, calculate_number_of_rs, tools_calculate_number_of_rs
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

class Agent:
    def __init__(self, name: str, persona: str, system_prompt: str, user_prompt: str, background: List[str]):
        """
        Initialize the agent with a name, persona, system prompt, and user prompt.

        Args:
            name (str): The name of the agent.
            persona (str): The persona of the agent.
            system_prompt (str): The system prompt for the agent.
            user_prompt (str): The user prompt for the agent.
            background (List[str]): The background information for the agent.

        Returns:
            None
        """
        self.name = name
        self.persona = persona
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.background = background

        self.memory = []
        # Use the name, persona and replace_prompt to fill in the system prompt, estimate 1 line
        self.system_prompt = replace_prompt(self.system_prompt, {"name": self.name, "persona": self.persona})
        # Initialize the agent's memory with the system prompt, estimate 1 line
        self.memory.append({"role": "system", "content": self.system_prompt})

        # Use the background and vectorize to vectorize the background information, estimate 3 lines
        self.background_vectors = []
        for background_line in background:
            self.background_vectors.append(vectorize(background_line))

    def rag(self, user_input: str) -> str:
        """
        Perform Retrieval-Augmented Generation (RAG) by retrieving relevant background information
        based on the user input using cosine similarity.

        Args:
            user_input (str): The user input to base the retrieval on.

        Returns:
            str: The most relevant background information.
        """
        user_input_vector = vectorize(user_input).reshape(1, -1)

        # Use cosine_similarity to calculate the similarities between the user input vector and the background vectors
        # Tip: Use flatten() to convert the result to a 1D array, estimate 1 line
        similarities = cosine_similarity(user_input_vector, self.background_vectors).flatten()
        
        # Get the index of the most similar background entry
        # Tip: Use np.argmax to get the index of the maximum value, estimate 1 line
        most_similar_index = np.argmax(similarities)
        
        # Retrieve and return the most relevant background information, estimate 1 line
        return self.background[most_similar_index]

    def respond(self, user_input: str) -> int:
        """
        Respond to a user input.

        Args:
            user_input (str): The user input.

        Returns:
            int: Number of Rs in the user input.
        """
        # TODO: Append the user input to the agent's memory, estimate 1 line
        self.memory.append({"role": "user", "content": user_input})

        # TODO: Use json_chat, memory, response format, and the tools definition to get a response, estimate 1 line
        response = json_chat(self.memory, response_format=NumberOfRs, tools=tools_calculate_number_of_rs)
        if response.get('role') == 'tool':
            arguments = response.get('arguments')
            # TODO: Use calculate_number_of_rs and arguments['text'] to calculate the number of Rs, estimate 1 line
            number_of_rs = calculate_number_of_rs(arguments['text'])
            self.memory.append(response.get('message'))
            function_call_result_message = {
                "role": "tool",
                "content": json.dumps({
                    "number": number_of_rs
                }),
                "tool_call_id": response.get('id')
            }
            self.memory.append(function_call_result_message)
            # TODO: Use json_chat to get the final response, no need to use the tools definition here, estimate 1 line
            response = json_chat(self.memory, response_format=NumberOfRs)
            return response['number']
        else:
            return -1
        