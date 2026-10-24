"""Flask web interface for the Watson NLP emotion detector."""

from flask import Flask, jsonify, render_template, request

from EmotionDetection import emotion_detector

# Static analysis: python -m pylint server.py EmotionDetection

app = Flask(__name__)


@app.get("/")
def index():
    """Render the detector page."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Return emotion scores for the supplied text."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return jsonify({"error": "Please enter text to analyze."}), 400
    try:
        result = emotion_detector(text_to_analyze)
    except (ValueError, TypeError):
        return jsonify({"error": "The text could not be analyzed."}), 502
    if result is None or result.get("dominant_emotion") is None:
        return jsonify({"error": "Emotion analysis is unavailable for this input."}), 502
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
