from enum import Enum
from pydantic import BaseModel
from typing import List


# TODO: Implement the response type definition for the number of Rs tool
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
    # TODO: Implement this function, estimate 1 line
    return text.lower().count('r')

# TODO: Implement the type definition for the calculate_number_of_rs tool
tools_calculate_number_of_rs = [
    {
        "type": "function",
        "function": {
            "name": "calculate_number_of_rs",
            "strict": True,
            # TODO: Fill in the description of the function, estimate 1-2 lines
            "description": "Calculate the number of letter r in a given text. Call this whenever you need to know the number of rs in a given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        # TODO: Fill in the type and description of the text parameter, estimate 2 lines
                        "type": "string",
                        "description": "The given text."
                    }
                },
                # TODO: Fill in the required parameters, estimate 1 line
                "required": ["text"],
                "additionalProperties": False
            }
        }
    }
]