from django.test import TestCase
from .utils import calculate_reading_time

class ReadingTimeUtilsTest(TestCase):
    """
    Tests for the core reading time calculator in utils.py.
    Simple and focused.
    """

    def test_empty_text_returns_zero(self):
        """Empty text should take 0 minutes to read."""
        result = calculate_reading_time("")
        # Assert that the 'minutes' in the result is 0
        self.assertEqual(result['minutes'], 0)
        # Also assert word_count is 0
        self.assertEqual(result['word_count'], 0)
        print("Passed: Empty text handled correctly.")

    def test_basic_word_count(self):
        """Tests if the function can count words in a simple string."""
        test_text = "Hello from Nakuru Kenya"
        result = calculate_reading_time(test_text)
        # "Hello from Nakuru Kenya" = 4 words
        self.assertEqual(result['word_count'], 4)
        # 4 words / 250 wpm = 0.016, rounded up = 1 minute
        self.assertEqual(result['minutes'], 1)
        print("Passed: Basic word count and calculation correct.")

    def test_rounding_up_logic(self):
        """Verifies the Medium-style 'round up' logic is working."""
        # 251 words at 250 wpm = 1.004 minutes, must round UP to 2 minutes
        text_with_251_words = "word " * 251  # Creates a string "word word word ...251"
        result = calculate_reading_time(text_with_251_words)
        self.assertEqual(result['minutes'], 2)
        print("Passed: Rounding-up logic works (Medium.com style).")

    def test_custom_words_per_minute(self):
        """Tests if the optional wpm parameter works."""
        # 600 words at 300 wpm = exactly 2 minutes
        text = "x " * 600
        result = calculate_reading_time(text, words_per_minute=300)
        self.assertEqual(result['minutes'], 2)
        self.assertEqual(result['words_per_minute'], 300)
        print("Passed: Custom words-per-minute setting works.")

# Create your tests here.
