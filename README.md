# Emotion Detector

A Python/Flask web application that uses the IBM Skills Network Watson NLP emotion service to estimate the emotional tone of an English statement.

## Features

- Detects **anger, disgust, fear, joy, and sadness** and selects the dominant emotion.
- Responsive browser interface with asynchronous submission and accessible status messages.
- Handles blank input, non-success HTTP responses, network timeouts, and malformed Watson responses.
- Includes a health endpoint at `/health`.
- Offline unit and Flask route tests; the test suite does not need a live Watson endpoint.
- GitHub Actions workflow runs tests on Python 3.11 and 3.12.

## Project structure

```text
EmotionDetector/
├── EmotionDetection/
│   ├── __init__.py
│   ├── emotion_detection.py
│   └── test_emotion_detection.py
├── static/
│   └── mywebscript.js
├── templates/
│   └── index.html
├── tests/
│   ├── __init__.py
│   └── test_server.py
├── .github/workflows/tests.yml
├── server.py
├── requirements.txt
└── README.md
```

## Run locally

Python 3.11 or 3.12 is recommended.

1. Clone the repository and enter the project directory:
   ```bash
   git clone https://github.com/kumar1419alt/EmotionDetector.git
   cd EmotionDetector
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python server.py
   ```
5. Open http://127.0.0.1:5000 and enter a statement.

## Test and verify

Run all offline tests from the project root:

```bash
python -m compileall -q EmotionDetection tests server.py
python -m unittest EmotionDetection.test_emotion_detection tests.test_server -v
```

The emotion-detector tests mock the Watson HTTP request and verify request formatting, all five possible dominant emotions, blank input, HTTP errors, timeouts, and malformed responses. Flask route tests cover the home page, health endpoint, invalid input, successful analysis, and unavailable-service handling. These tests are deterministic and do not require external network access.

The live Watson service is still required for real text analysis. The application uses model ID `emotion_aggregated-workflow_lang_en_stock` and sends text using the `raw_document.text` payload field. The lab endpoint may be temporarily unavailable.

## Endpoints

- `GET /` — browser interface
- `GET /health` — returns `{"status":"ok"}`
- `GET /emotionDetector?textToAnalyze=I%20am%20happy` — returns emotion scores and the dominant emotion as plain text

## Troubleshooting

- If dependency installation fails, check your Python version and internet connection.
- If the app returns a 502 response, the Watson endpoint may be unavailable; try again later.
- Keep the input in English and avoid sending an empty statement.
