from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions

def generate_response(client, messages):
    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    return response