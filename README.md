@'
# Emotion Detector

## Project Description

This project is an Emotion Detection application developed using Python, Flask, and the IBM Watson Natural Language Processing service.

The application analyzes a text statement and identifies the following emotions:

- Anger
- Disgust
- Fear
- Joy
- Sadness

It also determines the dominant emotion expressed in the given statement.

## Project Structure

```text
EmotionDetector/
├── EmotionDetection/
│   ├── __init__.py
│   ├── emotion_detection.py
│   └── test_emotion_detection.py
├── templates/
│   └── index.html
├── server.py
└── README.md