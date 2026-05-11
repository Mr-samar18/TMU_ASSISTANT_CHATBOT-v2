from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, os
from ai_helper import ask_llama

print("APP STARTING...")
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data():
    path = os.path.join(BASE_DIR, "data", "tmu_data.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            return data[0]
        return data

tmu_data = load_data()

def get_relevant_context(question, data, max_intents=6):
    """Find the most relevant intents for the question instead of sending all data."""
    question_lower = question.lower()
    scored = []

    for intent in data["intents"]:
        score = 0
        tag = intent["tag"].lower()

        # score by tag match
        if any(word in question_lower for word in tag.split("_")):
            score += 3

        # score by pattern match
        for pattern in intent.get("patterns", []):
            if any(word in question_lower for word in pattern.lower().split()):
                score += 1

        # score by response keyword match
        response_text = " ".join(intent["responses"]).lower()
        for word in question_lower.split():
            if len(word) > 3 and word in response_text:
                score += 1

        if score > 0:
            scored.append((score, intent))

    # sort by score, take top N
    scored.sort(key=lambda x: x[0], reverse=True)
    top_intents = [item[1] for item in scored[:max_intents]]

    # if nothing matched, send general TMU info
    if not top_intents:
        top_intents = [i for i in data["intents"]
                      if i["tag"] in ["tmu_info", "courses", "fees_scholarship"]][:3]

    # build context string
    lines = ["=== TMU Knowledge Base (Relevant Sections) ===\n"]
    for intent in top_intents:
        tag = intent["tag"].upper().replace("_", " ")
        response = intent["responses"][0]
        lines.append(f"[{tag}]\n{response}\n")

    return "\n".join(lines)

# Keep full context for general fallback
def build_full_context(data):
    lines = ["=== TMU University Complete Information ===\n"]
    for intent in data["intents"]:
        tag = intent["tag"].upper().replace("_", " ")
        response = intent["responses"][0]
        lines.append(f"[{tag}]: {response}\n")
    return "\n".join(lines)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data_req = request.get_json(silent=True) or {}
        user_question = data_req.get("question", "").strip()
        timestamp = datetime.now().strftime("%H:%M")

        if not user_question:
            return jsonify({
                "answer": "Please type a question.",
                "timestamp": timestamp
            })

        # send only relevant context, not entire JSON
        context = get_relevant_context(user_question, tmu_data)
        answer = ask_llama(user_question, context)

        return jsonify({
            "answer": answer,
            "timestamp": timestamp
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "answer": "Server error. Please try again.",
            "timestamp": datetime.now().strftime("%H:%M")
        })

if __name__ == "__main__":
    app.run(debug=True)