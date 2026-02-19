#!/usr/bin/env python3
"""
Deep analysis of Josh's Twitter voice and personality.
"""

import json
import re
from collections import Counter

# Load recent tweets
with open('/root/.openclaw/workspace/recent_tweets.json', 'r') as f:
    tweets = json.load(f)

# Extract all tweet text
all_text = []
lowercase_tweets = 0
uppercase_tweets = 0
mixed_case_tweets = 0
no_punctuation = 0
has_emoji = 0

for tweet in tweets:
    text = tweet.get('full_text', '')
    if text:
        all_text.append(text)

        # Case analysis
        if text.islower():
            lowercase_tweets += 1
        elif text.isupper():
            uppercase_tweets += 1
        else:
            mixed_case_tweets += 1

        # Punctuation check
        cleaned = re.sub(r'[^\w\s]', '', text)
        if not any(c in '.,!?;:' for c in text):
            no_punctuation += 1

        # Emoji check
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"
            "]+"
        )
        if emoji_pattern.search(text):
            has_emoji += 1

print("=== VOICE ANALYSIS ===")
print(f"Total tweets analyzed: {len(all_text)}")
print()
print("--- CASE USAGE ---")
print(f"  All lowercase: {lowercase_tweets} ({lowercase_tweets/len(all_text)*100:.1f}%)")
print(f"  Mixed case: {mixed_case_tweets} ({mixed_case_tweets/len(all_text)*100:.1f}%)")
print(f"  All uppercase: {uppercase_tweets} ({uppercase_tweets/len(all_text)*100:.1f}%)")
print()
print("--- PUNCTUATION ---")
print(f"  No end punctuation: {no_punctuation} ({no_punctuation/len(all_text)*100:.1f}%)")
print()
print("--- EMOJIS ---")
print(f"  Tweets with emojis: {has_emoji} ({has_emoji/len(all_text)*100:.1f}%)")
print()

# Common words/phrases (2+ words)
all_words = []
for text in all_text:
    words = re.findall(r'\b\w+\b', text.lower())
    all_words.extend(words)

word_freq = Counter(all_words)
print("--- TOP WORDS (excluding common) ---")
skip_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out',
              'get', 'to', 'of', 'in', 'it', 'that', 'this', 'is', 'i', 'a', 'be', 'with', 'on', 'just', 'so',
              'have', 'if', 'my', 'as', 'at', 'do', 'up', 'like', 'from', 'by', 'about', 'me', 'when', 'what',
              'im', 'dont', 'know', 'go', 'time', 'now', 'they', 'want', 'or', 'we', 'an', 'will', 'some',
              'no', 'has', 'more', 'would', 'your', 'who', 'them', 'make', 'only', 'its', 'really', 'going',
              'think', 'how', 'than', 'because', 'their', 'there', 'first', 'much', 'being', 'been', 'into',
              'most', 'good', 'right', 'any', 'work', 'also', 'see', 'way', 'back', 'even', 'am', 'still',
              'something', 'yeah', 'lol', 'well', 'say', 'need', 'same', 'thing', 'use', 'too', 'should'}

filtered_words = [(word, count) for word, count in word_freq.most_common(50) if word not in skip_words and len(word) > 2]
for word, count in filtered_words[:20]:
    print(f"  '{word}': {count}")
print()

# Look for sentence starters and patterns
sentence_starters = []
for text in all_text:
    # Find sentences starting with common words
    starters = re.findall(r'(?i)^(i|the|just|so|no|when|but|my|why|what|how|if|this|that)\b', text)
    sentence_starters.extend([s.lower() for s in starters])

starter_freq = Counter(sentence_starters)
print("--- COMMON SENTENCE STARTERS ---")
for starter, count in starter_freq.most_common(10):
    print(f"  '{starter}': {count}")
print()

# Look for common phrases (2-3 words)
from itertools import combinations

phrases = []
for text in all_text:
    words = re.findall(r'\b\w+\b', text.lower())
    # 2-word phrases
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i+1]}"
        if len(phrase) > 5 and phrase.count(' ') == 1:
            phrases.append(phrase)

phrase_freq = Counter(phrases)
print("--- COMMON PHRASES (2 words) ---")
for phrase, count in phrase_freq.most_common(15):
    if count > 2:
        print(f"  '{phrase}': {count}")
