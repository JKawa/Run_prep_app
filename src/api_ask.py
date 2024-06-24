from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
print("trutu", os.getenv("OPENAI_API_KEY"))


class OpenIAmessage:
    def __init__(self, user_message):
        self.user_message = user_message
        self.answer = ""
        self.client = OpenAI()  # Initialize your OpenAI client properly

    def generate_response(self):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a weather analyser, temperature always be in Celsius.",
                    },
                    {"role": "user", "content": self.user_message},
                ],
            )
            self.answer = completion.choices[0].message.content
            print(self.answer)
        except Exception as e:
            print(f"An error occurred: {e}")
