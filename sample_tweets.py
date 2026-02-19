#!/usr/bin/env python3
"""
Extract representative tweets to understand Josh's actual voice.
"""

import json
import random

# Load recent tweets
with open('/root/.openclaw/workspace/recent_tweets.json', 'r') as f:
    tweets = json.load(f)

print("=== REPRESENTATIVE TWEETS (random sample of 30) ===\n")

# Shuffle and pick 30 diverse tweets
random.shuffle(tweets)
sample_tweets = tweets[:30]

for i, tweet in enumerate(sample_tweets, 1):
    text = tweet.get('full_text', '')
    created = tweet.get('created_at', '')
    fav = tweet.get('favorite_count', '0')
    rt = tweet.get('retweet_count', '0')
    is_rt = tweet.get('retweeted', False)

    # Clean up HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')

    prefix = "RT " if is_rt else ""
    print(f"{i}. [{created[:16]}] {prefix}❤️{fav} RT{rt}")
    print(f"   {text[:300]}")
    if len(text) > 300:
        print(f"   ...")
    print()

# Also show the actual most recent 10 tweets chronologically
print("\n\n=== MOST RECENT 10 TWEETS (chronological) ===\n")

sorted_tweets = sorted(tweets, key=lambda t: t.get('created_at', ''), reverse=True)
for i, tweet in enumerate(sorted_tweets[:10], 1):
    text = tweet.get('full_text', '')
    created = tweet.get('created_at', '')
    fav = tweet.get('favorite_count', '0')
    rt = tweet.get('retweet_count', '0')
    is_rt = tweet.get('retweeted', False)

    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')

    prefix = "RT " if is_rt else ""
    print(f"{i}. [{created[:16]}] {prefix}")
    print(f"   {text}")
    print()
