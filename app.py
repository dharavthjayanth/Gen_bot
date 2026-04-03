from flask import Flask, render_template, request, jsonify, session
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # change this in real projects

# Load Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Answer user questions clearly, simply, and politely. "
    "Keep answers easy to understand."
)

@app.route("/")
def home():
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Get previous history
        history = session.get("chat_history", [])

        # Build prompt with basic memory
        conversation_text = SYSTEM_PROMPT + "\n\nConversation so far:\n"

        for item in history[-6:]:  # last 6 messages only
            conversation_text += f"{item['role']}: {item['text']}\n"

        conversation_text += f"user: {user_message}\nassistant:"

        # Send to Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation_text
        )

        bot_reply = response.text if response.text else "Sorry, I could not generate a response."

        # Save history
        history.append({"role": "user", "text": user_message})
        history.append({"role": "assistant", "text": bot_reply})
        session["chat_history"] = history

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500

@app.route("/clear", methods=["POST"])
def clear_chat():
    session["chat_history"] = []
    return jsonify({"message": "Chat cleared successfully"})

if __name__ == "__main__":
    app.run(debug=True)