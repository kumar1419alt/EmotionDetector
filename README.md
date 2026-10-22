# Emotion Detector

A Python/Flask web application that analyzes a text statement with the IBM Skills Network Watson NLP emotion service and reports the five emotion scores plus the dominant emotion.

## Emotions returned

- Anger
- Disgust
- Fear
- Joy
- Sadness
- Dominant emotion (the emotion with the highest score)

## Project structure

```text
EmotionDetector/
├── EmotionDetection/
│   ├── __init__.py
│   ├── emotion_detection.py
│   └── test_emotion_detection.py
├── templates/
│   └── index.html
├── server.py
├── requirements.txt
└── README.md
```

## Run locally

Python 3.10+ is recommended.

1. Clone the repository and enter the project directory.
   ```bash
   git clone https://github.com/kumar1419alt/EmotionDetector.git
   cd EmotionDetector
   ```
2. Create and activate a virtual environment (recommended).
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   ```
3. Install dependencies.
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Start Flask.
   ```bash
   python server.py
   ```
5. Open http://127.0.0.1:5000 in your browser. Enter an English statement and select **Analyze**.

The analysis route is `/emotionDetector?textToAnalyze=I%20am%20happy`. The Watson NLP service requires network access. If the service is unavailable or returns an invalid response, the detector returns `None` values rather than crashing.

## Tests

The test module includes examples for each dominant emotion. Run it from the project root:

```bash
python -m unittest EmotionDetection.test_emotion_detection -v
```

These tests call the remote Watson service, so they require network access and may fail if that service is temporarily unavailable.

## Implementation notes

- Uses the required Watson model ID `emotion_aggregated-workflow_lang_en_stock`.
- Sends input as `raw_document.text`.
- Uses a request timeout and handles HTTP, network, and malformed-response errors.
- Does not require API credentials for the Skills Network lab endpoint; availability is controlled by the service.
