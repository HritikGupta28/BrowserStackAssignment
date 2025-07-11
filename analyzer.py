import re
from collections import Counter

def find_repeated_words(titles):
    tokens = []
    for title in titles:
        tokens += re.findall(r'\b\w+\b', title.lower())
    return {word: count for word, count in Counter(tokens).items() if count > 2}
