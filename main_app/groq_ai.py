import os

from groq import Groq

from main_app.app_variables.variables import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)



