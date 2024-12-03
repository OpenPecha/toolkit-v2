import json
import os
from contextlib import contextmanager

import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")


@contextmanager
def cwd(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def read_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_text_direction_with_lang(lang):
    # Left-to-Right (LTR) languages
    ltr_languages = [
        "bo",  # Tibetan
        "dz",  # Dzongkha
        "en",  # English
        "es",  # Spanish
        "fr",  # French
        "hi",  # Hindi
        "ja",  # Japanese
        "ko",  # Korean
        "mn",  # Mongolian
        "mr",  # Marathi
        "ms",  # Malay
        "ne",  # Nepali
        "pt",  # Portuguese
        "ru",  # Russian
        "sw",  # Swahili
        "th",  # Thai
        "vi",  # Vietnamese
        "zh",  # Chinese (both Simplified and Traditional)
    ]

    # Right-to-Left (RTL) languages
    rtl_languages = ["ar", "he"]  # Arabic  # Hebrew

    if lang in ltr_languages:
        return "ltr"
    elif lang in rtl_languages:
        return "rtl"
    else:
        # Default to LTR if language is unknown
        return "ltr"


def get_claude_response(prompt: str):
    # Initialize the client with your API key
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Create a message request
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",  # Specify the model version
        max_tokens=1000,  # Set maximum tokens for the response
        temperature=0,  # Adjust randomness of responses (0.0 for deterministic)
        system="You are a helpful assistant.",  # System message for context
        messages=[{"role": "user", "content": prompt}],
    )

    # Print the response content
    return response.content[0].text


def translate_bo_to_en(text: str):
    prompt = f"""You are a professional translator specializing in Tibetan to English translation. Follow these strict guidelines:

    1. Translate the Tibetan text with the highest linguistic accuracy
    2. Preserve the original meaning and nuanced context
    3. Use clear, natural English that sounds like a native speaker
    4. If the text contains cultural or idiomatic expressions, provide a culturally appropriate equivalent
    5. Avoid literal word-for-word translations
    6. Return ONLY the English translation, with no additional commentary or explanation

    Source Tibetan Text:
    {text}

    Translation:"""

    response = get_claude_response(prompt)
    return response.strip()
