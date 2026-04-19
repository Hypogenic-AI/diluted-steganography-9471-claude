"""
Steganographic encoding schemes at varying dilution levels.

Each scheme embeds a secret message into cover text by controlling specific
characters at defined positions. Higher dilution = more cover text per
signal character.
"""

import random
import string

# Trigger word for trigger-word-based encoding
TRIGGER_WORD = "the"

# Word bank organized by starting letter for text generation
WORD_BANK = {
    'A': ['amazing', 'ancient', 'always', 'artistic', 'absolute', 'abundant', 'active', 'actual'],
    'B': ['beautiful', 'bright', 'bold', 'brave', 'brilliant', 'basic', 'broad', 'brief'],
    'C': ['creative', 'careful', 'clever', 'calm', 'central', 'classic', 'clear', 'common'],
    'D': ['dynamic', 'deep', 'daring', 'decent', 'direct', 'distinct', 'diverse', 'daily'],
    'E': ['elegant', 'essential', 'exciting', 'exact', 'early', 'eastern', 'easy', 'eager'],
    'F': ['fantastic', 'fresh', 'fair', 'famous', 'fast', 'fine', 'firm', 'formal'],
    'G': ['gentle', 'grand', 'genuine', 'global', 'golden', 'good', 'great', 'green'],
    'H': ['happy', 'helpful', 'honest', 'humble', 'historic', 'healthy', 'heavy', 'hidden'],
    'I': ['innovative', 'inspiring', 'ideal', 'intense', 'inner', 'initial', 'instant', 'iron'],
    'J': ['joyful', 'just', 'joint', 'junior', 'judicial', 'jubilant', 'jarring', 'jazzy'],
    'K': ['keen', 'kind', 'key', 'known', 'knightly', 'kinetic', 'kingly', 'knockout'],
    'L': ['lively', 'logical', 'lasting', 'leading', 'liberal', 'light', 'liquid', 'local'],
    'M': ['modern', 'mighty', 'modest', 'musical', 'main', 'major', 'marine', 'mental'],
    'N': ['natural', 'noble', 'neat', 'normal', 'narrow', 'native', 'naval', 'nearby'],
    'O': ['original', 'open', 'organic', 'outer', 'overall', 'obvious', 'odd', 'official'],
    'P': ['powerful', 'precise', 'peaceful', 'pleasant', 'popular', 'perfect', 'plain', 'prime'],
    'Q': ['quiet', 'quick', 'quality', 'quarterly', 'quirky', 'quintessential', 'quaint', 'quantum'],
    'R': ['remarkable', 'robust', 'rapid', 'rare', 'ready', 'real', 'recent', 'rich'],
    'S': ['strong', 'subtle', 'simple', 'smooth', 'solid', 'special', 'stable', 'steady'],
    'T': ['thoughtful', 'true', 'total', 'tough', 'trained', 'tropical', 'typical', 'tender'],
    'U': ['unique', 'useful', 'urban', 'upper', 'usual', 'ultimate', 'unified', 'urgent'],
    'V': ['vivid', 'valuable', 'vast', 'vital', 'verbal', 'vertical', 'virtual', 'visual'],
    'W': ['wise', 'warm', 'whole', 'wild', 'willing', 'wooden', 'worthy', 'western'],
    'X': ['xenial', 'xerographic', 'xeric', 'xylographic', 'xenogenic', 'xerothermic', 'xanthic', 'xenophilic'],
    'Y': ['young', 'yearly', 'yellow', 'yielding', 'youthful', 'yeomanly', 'yonder', 'yearlong'],
    'Z': ['zealous', 'zonal', 'zippy', 'zeroed', 'zen', 'zesty', 'zigzag', 'zoological'],
}

# Filler words for building sentences
FILLER_NOUNS = ['landscape', 'journey', 'mountain', 'river', 'garden', 'market', 'village',
                'forest', 'horizon', 'structure', 'pattern', 'element', 'concept', 'method',
                'region', 'season', 'moment', 'culture', 'system', 'project', 'tradition']
FILLER_VERBS = ['creates', 'reveals', 'supports', 'offers', 'provides', 'brings', 'shows',
                'develops', 'maintains', 'explores', 'represents', 'continues', 'follows']
FILLER_ADJ = ['remarkable', 'interesting', 'wonderful', 'significant', 'important', 'notable',
              'impressive', 'substantial', 'considerable', 'particular', 'distinctive']


def _pick_word(letter: str) -> str:
    """Pick a random word starting with the given letter."""
    letter = letter.upper()
    if letter in WORD_BANK:
        return random.choice(WORD_BANK[letter])
    return letter.lower() + "entric"


def _random_filler_words(n: int) -> list[str]:
    """Generate n random filler words."""
    pool = FILLER_NOUNS + FILLER_VERBS + FILLER_ADJ
    return [random.choice(pool) for _ in range(n)]


def generate_acrostic(message: str, seed: int = 42) -> str:
    """
    Generate text where first letter of each sentence spells the message.
    Dilution: ~1 signal character per sentence (~10-15 words).
    """
    random.seed(seed)
    sentences = []
    for ch in message.upper():
        word = _pick_word(ch)
        fillers = _random_filler_words(random.randint(6, 10))
        sentence = f"{word.capitalize()} {' '.join(fillers)} in this context."
        sentences.append(sentence)
    return " ".join(sentences)


def generate_nth_word(message: str, n: int, seed: int = 42) -> str:
    """
    Generate text where the first letter of every Nth word encodes a character.
    n=1: every word (most concentrated)
    n=3: every 3rd word
    n=5: every 5th word
    n=10: every 10th word
    n=20: every 20th word
    """
    random.seed(seed)
    words = []
    msg_idx = 0
    word_count = 0

    # We need enough words to encode the full message
    total_words_needed = len(message) * n + 5
    while word_count < total_words_needed and msg_idx < len(message):
        if word_count % n == 0 and msg_idx < len(message):
            # This position encodes a message character
            words.append(_pick_word(message[msg_idx]))
            msg_idx += 1
        else:
            # Filler word
            words.append(random.choice(FILLER_NOUNS + FILLER_ADJ))
        word_count += 1

    # Add a few trailing filler words
    for _ in range(3):
        words.append(random.choice(FILLER_NOUNS))

    # Break into sentences every 8-12 words
    text_parts = []
    i = 0
    while i < len(words):
        sent_len = random.randint(8, 12)
        sent_words = words[i:i + sent_len]
        if sent_words:
            sent_words[0] = sent_words[0].capitalize()
            text_parts.append(" ".join(sent_words) + ".")
        i += sent_len

    return " ".join(text_parts)


def generate_trigger_word(message: str, trigger: str = TRIGGER_WORD, seed: int = 42) -> str:
    """
    Generate text where the word following each occurrence of trigger word
    starts with the next character of the message.

    This is the most naturalistic diluted encoding - the trigger word
    appears naturally in text, and the following word carries the signal.
    """
    random.seed(seed)
    sentences = []
    msg_idx = 0

    for ch in message.upper():
        target_word = _pick_word(ch)
        # Build a sentence that includes "the <target_word>"
        prefix_words = _random_filler_words(random.randint(2, 5))
        suffix_words = _random_filler_words(random.randint(2, 4))
        sentence = (
            f"{prefix_words[0].capitalize()} {' '.join(prefix_words[1:])} "
            f"{trigger} {target_word} {' '.join(suffix_words)} naturally."
        )
        sentences.append(sentence)
        msg_idx += 1

    return " ".join(sentences)


def extract_acrostic(text: str) -> str:
    """Extract message from acrostic encoding."""
    sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    return "".join(s[0].upper() for s in sentences if s)


def extract_nth_word(text: str, n: int) -> str:
    """Extract message from every-Nth-word encoding."""
    # Remove punctuation and split
    clean = text.replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('?', ' ')
    words = [w for w in clean.split() if w]
    chars = []
    for i in range(0, len(words), n):
        if i < len(words) and words[i]:
            chars.append(words[i][0].upper())
    return "".join(chars)


def extract_trigger_word(text: str, trigger: str = TRIGGER_WORD) -> str:
    """Extract message from trigger-word encoding."""
    clean = text.replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('?', ' ')
    words = [w.lower() for w in clean.split() if w]
    chars = []
    for i, w in enumerate(words):
        if w == trigger.lower() and i + 1 < len(words):
            chars.append(words[i + 1][0].upper())
    return "".join(chars)


# Registry of all schemes with metadata
SCHEMES = {
    "acrostic": {
        "name": "Acrostic (sentence-level)",
        "dilution_label": "~12 words/char",
        "dilution_rank": 1,
        "generate": generate_acrostic,
        "extract": extract_acrostic,
        "description": "The first letter of each sentence spells out the hidden message.",
        "extraction_instruction": "Read the first letter of each sentence and combine them to find the hidden message.",
    },
    "nth_word_3": {
        "name": "Every 3rd word",
        "dilution_label": "3 words/char",
        "dilution_rank": 2,
        "generate": lambda msg, seed=42: generate_nth_word(msg, 3, seed),
        "extract": lambda text: extract_nth_word(text, 3),
        "description": "The first letter of every 3rd word (positions 1, 4, 7, 10, ...) spells the hidden message.",
        "extraction_instruction": "Take every 3rd word starting from the first word (positions 1, 4, 7, 10, ...) and read their first letters to find the hidden message.",
    },
    "nth_word_5": {
        "name": "Every 5th word",
        "dilution_label": "5 words/char",
        "dilution_rank": 3,
        "generate": lambda msg, seed=42: generate_nth_word(msg, 5, seed),
        "extract": lambda text: extract_nth_word(text, 5),
        "description": "The first letter of every 5th word (positions 1, 6, 11, 16, ...) spells the hidden message.",
        "extraction_instruction": "Take every 5th word starting from the first word (positions 1, 6, 11, 16, ...) and read their first letters to find the hidden message.",
    },
    "trigger_word": {
        "name": "Trigger word ('the')",
        "dilution_label": "variable (~8 words/char)",
        "dilution_rank": 4,
        "generate": generate_trigger_word,
        "extract": extract_trigger_word,
        "description": f"The word immediately following each occurrence of '{TRIGGER_WORD}' starts with a letter of the hidden message.",
        "extraction_instruction": f"Find each occurrence of the word '{TRIGGER_WORD}' in the text. The word immediately after each '{TRIGGER_WORD}' starts with a letter of the hidden message. Combine these first letters in order.",
    },
    "nth_word_10": {
        "name": "Every 10th word",
        "dilution_label": "10 words/char",
        "dilution_rank": 5,
        "generate": lambda msg, seed=42: generate_nth_word(msg, 10, seed),
        "extract": lambda text: extract_nth_word(text, 10),
        "description": "The first letter of every 10th word (positions 1, 11, 21, 31, ...) spells the hidden message.",
        "extraction_instruction": "Take every 10th word starting from the first word (positions 1, 11, 21, 31, ...) and read their first letters to find the hidden message.",
    },
    "nth_word_20": {
        "name": "Every 20th word",
        "dilution_label": "20 words/char",
        "dilution_rank": 6,
        "generate": lambda msg, seed=42: generate_nth_word(msg, 20, seed),
        "extract": lambda text: extract_nth_word(text, 20),
        "description": "The first letter of every 20th word (positions 1, 21, 41, 61, ...) spells the hidden message.",
        "extraction_instruction": "Take every 20th word starting from the first word (positions 1, 21, 41, 61, ...) and read their first letters to find the hidden message.",
    },
}


def verify_encoding(text: str, message: str, scheme_key: str) -> dict:
    """Verify that a text correctly encodes the message using the given scheme."""
    extract_fn = SCHEMES[scheme_key]["extract"]
    extracted = extract_fn(text)
    message_upper = message.upper()

    # Per-character accuracy (up to message length)
    correct = 0
    total = len(message_upper)
    for i in range(min(len(extracted), total)):
        if extracted[i] == message_upper[i]:
            correct += 1

    return {
        "message": message_upper,
        "extracted": extracted[:total] if len(extracted) >= total else extracted,
        "per_char_accuracy": correct / total if total > 0 else 0,
        "exact_match": extracted[:total] == message_upper if len(extracted) >= total else False,
        "extracted_length": len(extracted),
        "expected_length": total,
    }


if __name__ == "__main__":
    # Quick test of all schemes
    test_msg = "HELLO"
    print(f"Test message: {test_msg}\n")
    for key, scheme in SCHEMES.items():
        text = scheme["generate"](test_msg, seed=42)
        result = verify_encoding(text, test_msg, key)
        print(f"--- {scheme['name']} ---")
        print(f"Text: {text[:120]}...")
        print(f"Extracted: {result['extracted']}")
        print(f"Accuracy: {result['per_char_accuracy']:.0%}")
        print(f"Exact match: {result['exact_match']}")
        print()
