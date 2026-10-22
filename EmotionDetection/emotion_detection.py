"""Emotion detection using the IBM Skills Network Watson NLP service."""

import requests


WATSON_EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result():
    """Return a consistent result when the service cannot analyze the input."""
    return {
        **{name: None for name in EMOTION_NAMES},
        "dominant_emotion": None,
    }


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the dominant emotion for a text.

    Invalid input, malformed responses, and service failures return None
    values rather than causing the Flask application to crash.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            WATSON_EMOTION_URL,
            json=payload,
            headers=headers,
            timeout=15,
        )
        if response.status_code != 200:
            return _empty_result()

        data = response.json()
        emotions = data["emotionPredictions"][0]["emotion"]
        scores = {name: float(emotions[name]) for name in EMOTION_NAMES}
    except (
        requests.RequestException,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
    ):
        return _empty_result()

    return {
        **scores,
        "dominant_emotion": max(scores, key=scores.get),
    }
