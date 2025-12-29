import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from prompts import system_prompt
from call_functions import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("An API is not provided")
    client = genai.Client(api_key=api_key)
    
    try: 
        user_prompt = sys.argv[1]
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        response = client.models.generate_content(
            model = 'gemini-2.0-flash-001',
            contents = messages,
            config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
    except IndexError:
        print("you need to provide a prompt")
        sys.exit(1)

    if response.function_calls is not None:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if function_call_result.parts == [] or None:
                raise Exception(f"function_call_result.parts is {function_call_result.parts}")
            if function_call_result.parts[0].function_response is None:
                raise Exception("function_call_result.parts[0].function_response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("function_call_result.parts[0].function_response.response is None")
            function_results.append(function_call_result.parts[0])
            #print(f"Calling function: {function_call.name}({function_call.args})")
            for arg in sys.argv:
                if arg == "--verbose":
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                    print(f"User prompt: {response.text}")
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
if __name__ == "__main__":
    main()
