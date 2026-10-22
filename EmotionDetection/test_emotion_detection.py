"""Offline unit tests for the Watson emotion detector."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import (
    EMOTION_NAMES,
    MODEL_ID,
    WATSON_EMOTION_URL,
    emotion_detector,
)


def make_response(scores, status_code=200):
    """Build a mock response with the expected Watson response schema."""
    response = Mock()
    response.status_code = status_code
    response.json.return_value = {
        "emotionPredictions": [{"emotion": scores}]
    }
    return response


class TestEmotionDetector(unittest.TestCase):
    def setUp(self):
        self.scores = {
            "anger": 0.1,
            "disgust": 0.05,
            "fear": 0.05,
            "joy": 0.7,
            "sadness": 0.1,
        }

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_returns_all_scores_and_dominant_emotion(self, post):
        post.return_value = make_response(self.scores)

        result = emotion_detector("I am glad this happened")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual({key: result[key] for key in EMOTION_NAMES}, self.scores)
        post.assert_called_once_with(
            WATSON_EMOTION_URL,
            json={"raw_document": {"text": "I am glad this happened"}},
            headers={"grpc-metadata-mm-model-id": MODEL_ID},
            timeout=15,
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_emotion_is_selected_for_each_emotion(self, post):
        for dominant in EMOTION_NAMES:
            with self.subTest(dominant=dominant):
                scores = {name: 0.01 for name in EMOTION_NAMES}
                scores[dominant] = 0.9
                post.return_value = make_response(scores)
                self.assertEqual(
                    emotion_detector("Example sentence")["dominant_emotion"],
                    dominant,
                )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input_does_not_call_service(self, post):
        for value in ("", "  ", None, 123):
            with self.subTest(value=value):
                result = emotion_detector(value)
                self.assertIsNone(result["dominant_emotion"])
                self.assertTrue(all(result[name] is None for name in EMOTION_NAMES))
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_non_200_response_returns_empty_result(self, post):
        post.return_value = make_response({}, status_code=503)
        result = emotion_detector("Some text")
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_network_error_returns_empty_result(self, post):
        post.side_effect = requests.Timeout("service timed out")
        result = emotion_detector("Some text")
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_malformed_response_returns_empty_result(self, post):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {}
        post.return_value = response
        result = emotion_detector("Some text")
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_invalid_json_returns_empty_result(self, post):
        response = Mock()
        response.status_code = 200
        response.json.side_effect = ValueError("invalid JSON")
        post.return_value = response
        result = emotion_detector("Some text")
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
