import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions, call_function

def main():
    
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not args:
        print("AI Code Assistant")
        print('Usage: python main.py "<prompt>" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    user_prompt = " ".join(args)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if verbose:
        print("User prompt: ", user_prompt)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for i in range(20):
        if generate_content(client, messages, verbose):
            break


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose and response.usage_metadata is not None:
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        print("Final response:")
        print(response.text)
        return True

    for candidate in response.candidates:
        messages.append(candidate.content)

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("function failed to return a response")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
        messages.append(function_call_result)
    
    if not function_responses:
        raise Exception("no function responses generated, exiting")
            

if __name__ == "__main__":
    main()