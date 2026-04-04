from flask import Blueprint, request, jsonify
from services.intent_service import detect_intent
from services.order_service import process_issue
from services.ai_service import generate_ai_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").lower()

    intent = detect_intent(user_input)

    # 🧠 detect follow-up (สำคัญมาก)
    follow_up_keywords = ["refund", "how", "when", "why", "where", "can i", "what"]

    is_follow_up = any(word in user_input for word in follow_up_keywords)

    if intent == "others" or intent == "unknown":
        reply = generate_ai_response(user_input, None)

    elif intent != "unknown" and is_follow_up:
        reply = generate_ai_response(user_input, intent)
        

    # 🧠 rule-based (เฉพาะเคสหลัก)
    elif any(word in user_input for word in ["delivery man", "rider", "driver", "courier"]):
        reply = "We're really sorry about your experience with the delivery staff. We will report this issue immediately and take appropriate action."
        
    elif intent == "delivery_delay":
        reply = "Your order 001 is still on the way. It should arrive shortly. If the delay continues, we can offer a discount for your next order."

    elif intent == "wrong_order":
        reply = (
        "We're really sorry about the wrong order 🙏\n\n"
        "Could you please upload a photo of your receipt or the items you received?\n"
        "This will help us verify the issue quickly.\n\n"
        "Once confirmed, we will process your refund right away."
    )

    # 🔥 STEP 1: ถ้ามี keyword → ไปขั้น refund
    elif intent == "food_issue" and (
        "insect" in user_input or 
        "spoiled" in user_input or 
        "bad" in user_input or 
        "cold" in user_input
    ):
        reply = (
        "We're really sorry to hear that 🙏\n\n"
        "Could you please upload a photo so we can verify the issue?\n\n"
        "Once confirmed, we will proceed with a refund."
    )

    # 🔥 STEP 2: ปกติ → ถาม + ขอรูป
    elif intent == "food_issue":
        reply = (
        "We're really sorry about your food issue 🙏\n\n"
        "Could you please describe what was wrong with the food?\n"
        "(e.g. cold, spoiled, missing items)\n\n"
        "Also, please upload a photo so we can verify the issue."
    )

    elif intent == "food_issue" and ("cold" in user_input or "spoiled" in user_input):
        reply = "Thank you for the details 🙏 Based on your description, we will proceed with a refund."

    elif intent == "not_received":
        reply = "We’re checking your order now. If it was not delivered, you will receive a full refund."

    elif intent == "cancel_order":
        reply = "Your order has been cancelled. If payment was completed, the refund will be processed shortly."


    # 🤖 default → AI
    else:
        reply = generate_ai_response(user_input, intent)

    return jsonify({
        "reply": reply,
        "intent": intent
    })
    
