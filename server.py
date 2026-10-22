"""Flask web application for the Watson emotion detector."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector


app = Flask(__name__)


@app.get("/")
def render_index_page():
    """Render the emotion detector user interface."""
    return render_template("index.html")


@app.get("/health")
def health_check():
    """Lightweight health endpoint for local checks and hosting platforms."""
    return {"status": "ok"}, 200


@app.get("/emotionDetector")
def emotion_detector_route():
    """Analyze the supplied text and return a human-readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    if not text_to_analyze.strip():
        return "Invalid input! Please enter a statement.", 400

    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        return (
            "Emotion analysis is temporarily unavailable. Please try again.",
            502,
        )

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    ), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
