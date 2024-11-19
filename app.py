import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Hugging Face API URL and Token
API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Predefined categories
categories = {
    "careers": ["Software Engineer", "Artist", "Entrepreneur", "Chef", "Teacher", "Musician"],
    "personality_traits": ["Adventurous", "Creative", "Compassionate", "Outgoing", "Introverted"],
    "interests": ["Cooking", "Traveling", "Fitness", "Music", "Literature", "Technology", "Gaming"],
    "relationship_goals": ["Casual", "Long-term", "Adventurous", "Seeking Deep Connection"]
}

@app.route("/")
def index():
    return render_template("index.html", categories=categories)

@app.route("/generate_bio", methods=["POST"])
def generate_bio():
    data = request.get_json()
    career = data.get("career", "an amazing individual")
    personality = data.get("personality", "unique")
    interests = data.get("interests", "a variety of passions")
    relationship_goal = data.get("relationship_goal", "a meaningful connection")

    # Create prompt
    prompt = (
        f"I am a {personality} {career} who loves {interests}. "
        f"I am seeking {relationship_goal} relationships."
    )

    # Make API request
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    # Parse response
    if response.status_code == 200:
        bio = response.json()[0]['generated_text']
    else:
        bio = "Sorry, the text generation service is currently unavailable."

    return jsonify({"bio": bio})

if __name__ == "__main__":
    app.run(debug=True)
