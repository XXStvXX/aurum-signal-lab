import unittest

from scripts.common import classify_event, tokenize


class ClassificationTest(unittest.TestCase):
    def test_war_signal(self):
        result = classify_event("Middle East missile attack raises escalation risk for gold")
        self.assertEqual(result["category"], "war")
        self.assertEqual(result["direction"], "bullish_gold")

    def test_fed_signal(self):
        result = classify_event("Federal Reserve rate hike sends Treasury yields higher")
        self.assertEqual(result["category"], "fed_policy")
        self.assertEqual(result["direction"], "context_dependent")

    def test_tokenize_removes_stopwords(self):
        tokens = tokenize("Gold and the Federal Reserve dollar story")
        self.assertNotIn("gold", tokens)
        self.assertIn("federal", tokens)


if __name__ == "__main__":
    unittest.main()
