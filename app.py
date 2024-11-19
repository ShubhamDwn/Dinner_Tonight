from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

# Load Hugging Face model
generator = pipeline("text-generation", model="distilgpt2")

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

    # Generate bio using Hugging Face model
    prompt = (
        f"I am a {personality} {career} who loves {interests}. "
        f"I am seeking {relationship_goal} relationships."
    )
    result = generator(prompt, max_length=100, num_return_sequences=1)
    bio = result[0]['generated_text']

    return jsonify({"bio": bio})

if __name__ == "__main__":
    app.run(debug=True)
