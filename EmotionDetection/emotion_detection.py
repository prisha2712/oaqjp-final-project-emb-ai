"""Call the Watson NLP emotion prediction service."""

from typing import Any

import requests

WATSON_EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze: str) -> dict[str, Any] | None:
    """Analyze text and return emotion scores, or None for invalid input."""
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return None

    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(WATSON_EMOTION_URL, headers=headers, json=payload, timeout=15)
    except requests.RequestException:
        return None

    if response.status_code == 400:
        return None
    response.raise_for_status()

    body = response.json()
    predictions = body.get("emotionPredictions") or body.get("emotion_predictions") or []
    if not predictions:
        return None

    raw_scores = predictions[0].get("emotion", {})
    scores = {key: raw_scores.get(key) for key in EMOTION_KEYS}
    valid_scores = {key: value for key, value in scores.items() if isinstance(value, (int, float))}
    scores["dominant_emotion"] = max(valid_scores, key=valid_scores.get) if valid_scores else None
    return scores

