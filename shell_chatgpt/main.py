import openai
import re
import json

developer_assistant_prompt = """
    You are an experienced full stack developer. You will be interacting with a user via a chat prompt.
    When asked to provide an example project, you must respond with the following JSON output format:
    
    {
        "files": [
            {
                "type": "file",
                "name": "main.py",
                "contents": "print('hello world')"
            },
            <Additional Files>
        ],
        "directions": "<Instructional text>",
        "requirements": "<A list of system requirements, eg. python 3.10 or .net core>",
        "additional-details": "Any additional information"
    }
"""

def extract_json(input_text):
      # Regex pattern to extract content between '```'
    pattern = '```(.*?)```'
    
    # Find all matches in the input text
    matches = re.findall(pattern, input_text, re.DOTALL)
    
    # If there's at least one match, attempt to parse the first one as JSON
    if matches:
        try:
            json_obj = json.loads(matches[0])
            return json_obj
        except json.JSONDecodeError:
            print('Could not parse the extracted content as JSON.')
            return None

def chat_with_gpt3():
    while True:
        prompt = input('> ')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": developer_assistant_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        #print(response)
        #content = json.loads(response['choices'][0]['message']['content'])
        content = response['choices'][0]['message']['content']
        print(content)

        print(extract_json(content))

        #files = content["files"]
        #directions = content["directions"]
        #requirements = content["requirements"]
        #additional_details = content["additional-details"]

if __name__ == '__main__':
    chat_with_gpt3()
