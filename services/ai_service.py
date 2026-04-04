import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_ai_response(user_input, intent=None):
    history = "\n".join(chat_history)

    prompt = f"""
    You are a professional food delivery support agent.

    Rules:
    - Always apologize first when there is a problem
    - Answer clearly and politely
    - If user asks follow-up questions, continue naturally
    - If user asks about refund → explain timeline (3-5 days)

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

    chat_history[:] = chat_history[-6:] #limit memory 

    return reply
