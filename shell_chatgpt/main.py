import openai

developer_assistant_prompt = """
    You are an experienced full stack developer. You will be interacting with a user via a chat prompt.
    When asked to provide an example project, you must respond in the following format:


    {
        "files": ["<List of files and extensions>"],
        "directions": "<Instructional text>",
        "requirements": "<A list of system requirements, eg. python 3.10 or .net core>",
        "additional-details": "Any additional information"
    }
"""


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
        print(response)
        print(response['choices'][0]['message']['content'])

if __name__ == '__main__':
    chat_with_gpt3()
