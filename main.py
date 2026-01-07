import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description = "AI Agent to helping with something...")
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    parser.add_argument("--verbose", action = "store_true", help = "Enable verbose output")
    args = parser.parse_args()
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not found")
    
    client = genai.Client(api_key = api_key)
    messages = [types.Content(role = "user", parts = [types.Part(text = args.user_prompt)])]
    
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model = "gemini-2.5-flash",
                contents = messages,
                config = types.GenerateContentConfig(
                    tools = [available_functions],
                    system_instruction = system_prompt,
                ),
            )
        except ConnectionError as e:
            print(f"Network error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        if not response.candidates:
            raise Exception("Gemini API response appears to be malformed")
        
        for candidate in response.candidates:
            messages.append(candidate.content )
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        print("Response:")
        if not response.function_calls:
            print(response.text)
            return
        else:
            function_results_list = []
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception('Function result incomplete: "parts" field empty')
                if not function_call_result.parts[0].function_response:
                    raise Exception('Function result incomplete: "parts[0].function_response" field empty')
                if not function_call_result.parts[0].function_response.response:
                    raise Exception('Function result incomplete: "pparts[0].function_response.response" field empty')
                function_results_list.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        
        messages.append(types.Content(role="user", parts = function_results_list))

    print(f"Agent overuse resources") 
    exit(1)


if __name__ == "__main__":
    main()
