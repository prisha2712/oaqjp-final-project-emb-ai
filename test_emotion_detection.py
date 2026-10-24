"""Unit tests for Watson emotion response handling."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Test formatted scores, dominant emotion, and error handling."""

    def analyze_with_scores(self, dominant):
        scores = {key: 0.01 for key in ("anger", "disgust", "fear", "joy", "sadness")}
        scores[dominant] = 0.95
        response = Mock(status_code=200)
        response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}
        with patch("EmotionDetection.emotion_detection.requests.post", return_value=response):
            return emotion_detector("Test input")

    def test_anger_is_dominant(self):
        self.assertEqual(self.analyze_with_scores("anger")["dominant_emotion"], "anger")

    def test_disgust_is_dominant(self):
        self.assertEqual(self.analyze_with_scores("disgust")["dominant_emotion"], "disgust")

    def test_fear_is_dominant(self):
        self.assertEqual(self.analyze_with_scores("fear")["dominant_emotion"], "fear")

    def test_joy_is_dominant_and_output_is_formatted(self):
        result = self.analyze_with_scores("joy")
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(set(result), {"anger", "disgust", "fear", "joy", "sadness",
                                       "dominant_emotion"})

    def test_sadness_is_dominant(self):
        self.assertEqual(self.analyze_with_scores("sadness")["dominant_emotion"], "sadness")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_status_400_returns_none(self, post):
        post.return_value = Mock(status_code=400)
        self.assertIsNone(emotion_detector("invalid"))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input_skips_request(self, post):
        self.assertIsNone(emotion_detector("  \n"))
        post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
