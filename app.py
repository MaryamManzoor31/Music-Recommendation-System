from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

print("Starting app...")

app = Flask(__name__)
CORS(app)

# Load dataset locally
df = pd.read_csv("spotify_combined_emotionally_enriched.csv", low_memory=False)

@app.route("/recommend", methods=["POST"])

@app.route("/")
def home():
    return "Music Recommendation API is running!"

def recommend():
    mood = request.json.get("mood")

    if mood is None:
        return jsonify({"error": "No mood provided"}), 400

    # Filter by Mood column (important!)
    filtered = df[df["Mood"].str.lower() == mood.lower()]

    if len(filtered) == 0:
        return jsonify([])

    # Select 5 random songs
    recommendations = filtered.sample(min(5, len(filtered)))

    return jsonify(
        recommendations[["track_name", "artist_name", "genre"]]
        .to_dict(orient="records")
    )

if __name__ == "__main__":
    app.run(debug=True)
