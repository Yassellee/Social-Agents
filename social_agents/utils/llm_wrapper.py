from typing import List, Dict
from openai import OpenAI
import numpy as np


client = OpenAI(api_key='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')


def json_chat(messages: List[Dict[str, str]],
              response_format,
              model: str = 'gpt-4o-2024-08-06',
              temperature: float = 0.7,
              enable_print: bool = False) -> str:
    
    def _chat():
        while True:
            try:
                response = client.beta.chat.completions.parse(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    response_format=response_format
                )
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