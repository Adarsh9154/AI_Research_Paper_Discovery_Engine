from groq import Groq

from config import Config


class GroqClient:

    def __init__(self):

        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI research assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_tokens=1024
        )

        return response.choices[0].message.content