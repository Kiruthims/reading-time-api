# apps/reading_time/utils.py
"""
Reading Time Calculator Utility
Follows Medium.com style: Always rounds UP to nearest minute
"""
import re
from math import ceil

def calculate_reading_time(text, words_per_minute=250):
    """
    Calculate reading time in minutes (rounded up).
    
    Args:
        text (str): The content to analyze
        words_per_minute (int): Reading speed (default 250)
    
    Returns:
        dict: {
            'minutes': int,      # Reading time (always rounded UP)
            'word_count': int,   # Number of words
            'words_per_minute': int,  # WPM used
            'display': str       # Human-readable format
        }
    
    Raises:
        ValueError: If text is not string or wpm is invalid
    
    Examples:
        >>> calculate_reading_time("Hello world")
        {'minutes': 1, 'word_count': 2, 'words_per_minute': 250, 'display': '1 min'}
        
        >>> calculate_reading_time("word " * 500)
        {'minutes': 2, 'word_count': 500, 'words_per_minute': 250, 'display': '2 min'}
    """
    # ===== 1. VALIDATION =====
    # Guard against wrong input types
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    
    if not isinstance(words_per_minute, int):
        raise ValueError("Words per minute must be an integer")
    
    if words_per_minute <= 0:
        raise ValueError("Words per minute must be positive (greater than 0)")
    
    # ===== 2. HANDLE EMPTY/WHITESPACE TEXT =====
    # If text is empty or only spaces/tabs/newlines
    if not text or text.isspace():
        return {
            'minutes': 0,
            'word_count': 0,
            'words_per_minute': words_per_minute,
            'display': '0 min'
        }
    
    # ===== 3. COUNT WORDS PROPERLY =====
    # Regex explanation: \b = word boundary, \w+ = one or more word characters
    # This handles: "word-word" as 1 word, "hello.world" as 2 words
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    
    # ===== 4. CALCULATE READING TIME =====
    # Always round UP to nearest minute (Medium.com style)
    # Example: 251 words at 250 wpm = 1.004 → ceil → 2 minutes
    minutes = ceil(word_count / words_per_minute)
    
    # ===== 5. FORMAT DISPLAY STRING =====
    # "1 min" for singular, "X min" for plural
    display_text = "1 min" if minutes == 1 else f"{minutes} min"
    
    # ===== 6. RETURN CLEAN RESULTS =====
    return {
        'minutes': minutes,
        'word_count': word_count,
        'words_per_minute': words_per_minute,
        'display': display_text
    }


# ===== BONUS: HELPER FUNCTION FOR FILES =====
def calculate_reading_time_from_file(file_content, words_per_minute=250):
    """
    Calculate reading time from file-like content.
    Useful for handling uploaded files in the future.
    
    Args:
        file_content: Can be file object or string
        words_per_minute: Reading speed
    
    Returns:
        Same as calculate_reading_time()
    """
    # If it's a file object (has .read() method), read it
    if hasattr(file_content, 'read'):
        text = file_content.read().decode('utf-8', errors='ignore')
    else:
        text = str(file_content)
    
    return calculate_reading_time(text, words_per_minute)