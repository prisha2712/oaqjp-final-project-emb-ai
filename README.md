# Final Project: Emotion Detector

A Flask web application that analyzes text with the IBM Watson NLP emotion prediction service.

## Features

- Detects anger, disgust, fear, joy, and sadness.
- Returns all emotion scores and the dominant emotion.
- Handles empty input and service errors.
- Includes unit tests with a mocked Watson service.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python server.py
```

Open <http://127.0.0.1:5000> in a browser. The Watson NLP endpoint is configured in `EmotionDetection/emotion_detection.py`.

## Test and lint

```powershell
python -m unittest test_emotion_detection.py
pylint server.py EmotionDetection
```

## Repository

This repository contains the final project for the IBM Skills Network Emotion Detector assignment.

