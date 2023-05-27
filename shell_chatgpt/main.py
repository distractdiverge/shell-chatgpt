import openai
import os
import re
import json


response_format = """
{
        "files": [
            {
                "type": "directory",
                "name": "<project_name>",
                "files": [
                    {
                        "type": "file",
                        "name": "__init__.py",
                        "contents": ""
                    },
                    {
                        "type": "file",
                        "name": "main.py",
                        "contents": ""
                    }
                ],
                ... Additional Folders or Files
            },
            {
                "type": "file",
                "name": "README.md",
                "contents": "# New Project"
            },
            {
                "type": "file",
                "name": "Pipfile",
                "contents": "[[source]]\nurl = "https://pypi.org/simple"\nverify_ssl = true\nname = "pypi"\n\n[packages]\npytest = "*"\npytest-cov = "*"\n
\n[dev-packages]\n\n[requires]\npython_version = "3.10"\npython_full_version = "3.10.6"\n"
            },
            ... Additional Folders or Files
        ],
        "directions": "<Instructional text>",
        "requirements": "<A list of system requirements, eg. python 3.10 or .net core>",
        "additional-details": "Any additional information"
    }
"""

developer_assistant_prompt = """
    You are an experienced full stack developer. You will be interacting with a user via a chat prompt.
    When asked to provide an example project, you must respond with the following JSON output format.

    Format: """ + response_format

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

def ensure_path_exists(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        print(f"Creation of the directory {path} failed: {error}")
    else:
        print(f"Successfully created the directory {path} or it already existed")

def create_files_from_json(json_obj, parent_dir=''):
    for file_obj in json_obj['files']:
        if file_obj['type'] == 'directory':
            new_dir_path = os.path.join(parent_dir, file_obj['name'])
            ensure_path_exists(new_dir_path)
            create_files_from_json(file_obj, parent_dir=new_dir_path)
        elif file_obj['type'] == 'file':
            file_path = os.path.join(parent_dir, file_obj['name'])
            with open(file_path, 'w') as f:
                f.write(file_obj['contents'])

def ensure_path_exists(path: str):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        print(f"Creation of the directory {path} failed: {error}")
    else:
        print(f"Successfully created the directory {path} or it already existed")


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

        json_content = extract_json(content)

        print("Creating Folders and files")
        create_files_from_json(json_content)


        #files = content["files"]
        #directions = content["directions"]
        #requirements = content["requirements"]
        #additional_details = content["additional-details"]

if __name__ == '__main__':
    chat_with_gpt3()
