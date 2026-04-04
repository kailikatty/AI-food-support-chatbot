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

    follow_up_keywords = ["refund", "how", "when", "why", "where", "can i", "what"]
    is_follow_up = any(word in user_input for word in follow_up_keywords)

    # 🔥 OTHERS → AI
    if intent == "others" or intent == "unknown":
        reply = generate_ai_response(user_input, None)

    # 🔥 DELIVERY STAFF COMPLAINT
    elif any(word in user_input for word in ["delivery man", "rider", "driver", "courier"]):
        reply = "We're really sorry about your experience with the delivery staff. We will report this issue immediately and take appropriate action."

    # 🔥 WRONG ORDER
    elif intent == "wrong_order":
        reply = (
            "We're really sorry about the wrong order 🙏\n\n"
            "Could you please upload a photo of your receipt or the items you received?\n"
            "This will help us verify the issue quickly.\n\n"
            "Once confirmed, we will process your refund right away."
        )

    # 🔥 FOOD ISSUE (STEP 1 → มีรายละเอียดแล้ว)
    elif intent == "food_issue" and any(word in user_input for word in ["insect", "spoiled", "bad", "cold"]):
        reply = (
            "We're really sorry to hear that 🙏\n\n"
            "Please upload a photo so we can verify the issue.\n\n"
            "Once confirmed, we will proceed with a refund."
        )

    # 🔥 FOOD ISSUE (STEP 2 → ยังไม่มีรายละเอียด)
    elif intent == "food_issue" or "food" in user_input:
        reply = (
            "We're really sorry about your food issue 🙏\n\n"
            "Could you please describe what was wrong with the food?\n"
            "(e.g. cold, spoiled, missing items)\n\n"
            "Also, please upload a photo so we can verify the issue."
        )

    # 🔥 DELIVERY DELAY
    elif intent == "delivery_delay":
        reply = "Your order is still on the way. It should arrive shortly. If the delay continues, we can offer a discount for your next order."

    # 🔥 NOT RECEIVED
    elif intent == "not_received":
        reply = "We’re checking your order now. If it was not delivered, you will receive a full refund."

    # 🔥 CANCEL ORDER
    elif intent == "cancel_order":
        reply = "Your order has been cancelled. If payment was completed, the refund will be processed shortly."

    # 🤖 FOLLOW-UP → AI (ต้องอยู่ท้าย!)
    elif is_follow_up:
        reply = generate_ai_response(user_input, intent)

    # 🤖 DEFAULT
    else:
        reply = generate_ai_response(user_input, intent)

    return jsonify({
        "reply": reply,
        "intent": intent
    })
