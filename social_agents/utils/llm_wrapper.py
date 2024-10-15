from typing import List, Dict
from openai import OpenAI
import numpy as np
import json

client = OpenAI(api_key='')

def json_chat(messages: List[Dict[str, str]],
              response_format,
              model: str = 'gpt-4o-2024-08-06',
              temperature: float = 0.7,
              enable_print: bool = False,
              tools: List[dict] = []):
    
    def _chat():
        while True:
            try:
                response = None
                if len(tools) == 0:
                    response = client.beta.chat.completions.parse(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        response_format=response_format
                    )
                else:
                    response = client.beta.chat.completions.parse(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        response_format=response_format,
                        tools=tools
                    )

                if response.choices[0].finish_reason == 'stop':
                    result = response.choices[0].message.content
                    
                    def extract_json(input_string):
                        stack = []
                        json_start_positions = []

                        for pos, char in enumerate(input_string):
                            if char in '{[':
                                stack.append(char)
                                if len(stack) == 1:
                                    json_start_positions.append(pos)
                            elif char in '}]':
                                if len(stack) == 0:
                                    raise ValueError("unexpected {} at position {}".format(pos, char))
                                last_open = stack.pop()
                                if (last_open == '{' and char != '}') or (last_open == '[' and char != ']'):
                                    raise ValueError("mismatched brackets {} and {} at position {}".format(last_open, char, pos))
                                if len(stack) == 0:
                                    return input_string[json_start_positions.pop():pos+1]
                        return None
                    
                    result = extract_json(result)
                    result = eval(result, {'true': True, 'false': False, 'null': None})
                    
                    if enable_print:
                        print(result)             
                    return result
                elif response.choices[0].finish_reason == 'tool_calls':
                    tool_call = response.choices[0].message.tool_calls[0]
                    arguments = tool_call.function.parsed_arguments
                    return {
                        "role": "tool",
                        "arguments": arguments,
                        "id": tool_call.id,
                        "message": response.choices[0].message
                    }
            
            except Exception as e:
                print(f"Error in json_chat: {e}")
                continue
    
    response = _chat()
    return response

def replace_prompt(raw_prompt: str, information: Dict[str, str]) -> str:
    for key, value in information.items():
        raw_prompt = raw_prompt.replace(f"%{key}%", value)

    return raw_prompt

def vectorize(text: str):
    embedding = np.array(client.embeddings.create(input = [text], model='text-embedding-3-small').data[0].embedding)
    return embedding


if __name__ == "__main__":
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate_number_of_rs",
                "strict": True,
                "description": "Calculate the number of letter r in a given text. Call this whenever you need to know the number of rs in a given text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The given text."
                        }
                    },
                    "required": ["text"],
                    "additionalProperties": False
                }
            }
        }
    ]
    from pydantic import BaseModel
    class NumberOfRs(BaseModel):
        number: int

    def calculate_number_of_rs(text: str) -> int:
        """
        Calculate the number of occurrences of the substring 'r' in the input text.

        Args:
            text (str): The input text.

        Returns:
            int: The number of occurrences of the substring 'r'.
        """
        return text.lower().count('r')
    
    system_prompt = "Calculate the number of 'r's in the text given by the user."
    user_prompt = "Strawberry"
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    response = json_chat(messages, response_format=NumberOfRs, tools=tools)
    if response.get('role') == 'tool':
        arguments = response.get('arguments')
        number_of_rs = calculate_number_of_rs(arguments['text'])
        messages.append(response.get('message'))
        function_call_result_message = {
            "role": "tool",
            "content": json.dumps({
                "number": number_of_rs
            }),
            "tool_call_id": response.get('id')
        }
        messages.append(function_call_result_message)
        response = json_chat(messages, response_format=NumberOfRs)
        print(response)
    else:
        print("Error in response")
