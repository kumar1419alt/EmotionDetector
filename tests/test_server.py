"""Flask route tests with Watson isolated from the network."""

import unittest
from unittest.mock import patch

from server import app


class TestEmotionDetectorRoutes(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_home_page_renders_form(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emotion Detector", response.data)
        self.assertIn(b"textToAnalyze", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_blank_text_returns_400(self):
        for query in ("", "?textToAnalyze=%20%20"):
            with self.subTest(query=query):
                response = self.client.get("/emotionDetector" + query)
                self.assertEqual(response.status_code, 400)
                self.assertIn(b"Invalid input", response.data)

    @patch("server.emotion_detector")
    def test_successful_analysis_returns_scores(self, detector):
        detector.return_value = {
            "anger": 0.1,
            "disgust": 0.05,
            "fear": 0.05,
            "joy": 0.7,
            "sadness": 0.1,
            "dominant_emotion": "joy",
        }
        response = self.client.get("/emotionDetector?textToAnalyze=happy")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"'joy': 0.7", response.data)
        self.assertIn(b"dominant emotion is joy", response.data)
        detector.assert_called_once_with("happy")

    @patch("server.emotion_detector")
    def test_unavailable_analysis_returns_502(self, detector):
        detector.return_value = {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }
        response = self.client.get("/emotionDetector?textToAnalyze=hello")
        self.assertEqual(response.status_code, 502)
        self.assertIn(b"temporarily unavailable", response.data)


if __name__ == "__main__":
    unittest.main()
