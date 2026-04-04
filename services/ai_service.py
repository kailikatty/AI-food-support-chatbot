import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

chat_history = []

def generate_ai_response(user_input, intent=None):
    history = "\n".join(chat_history)

    prompt = f"""
You are a professional food delivery support agent.

Rules:
- Always be polite
- Always apologize first if there is a problem
- Then provide solution clearly
- Keep answer short and natural

Conversation:
{history}

Customer: {user_input}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    reply = response.text

    # save memory
    chat_history.append(f"Customer: {user_input}")
    chat_history.append(f"Agent: {reply}")

    return reply
