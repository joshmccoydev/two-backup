#!/usr/bin/env python3
"""
Analyze Twitter data to learn Josh's voice and personality.
Focus on tweets from past ~3 years (2023 onwards).
"""

import json
import re
from datetime import datetime
from collections import Counter

# Read tweets.js
twitter_file = "/root/.openclaw/workspace/twitter-2026-02-19-624a8ae0dfc4ccd71bcdbf1fe49f90cdac7ca40975e7c3664664b142ddb0e13f/data/tweets.js"

with open(twitter_file, 'r') as f:
    content = f.read()

# Strip the JavaScript wrapper
json_start = content.find('[')
json_end = content.rfind(']') + 1

if json_start == -1 or json_end == 0:
    print("Could not find JSON array in tweets.js")
    exit(1)

json_content = content[json_start:json_end]
tweets_data = json.loads(json_content)

# Filter tweets from past ~3 years (2023 onwards)
from zoneinfo import ZoneInfo
cutoff_date = datetime(2023, 1, 1, tzinfo=ZoneInfo('UTC'))
recent_tweets = []

for item in tweets_data:
    tweet = item.get('tweet', {})
    created_at_str = tweet.get('created_at', '')
    if created_at_str:
        try:
            # Parse Twitter date format: "Wed Feb 18 04:59:08 +0000 2026"
            tweet_date = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S %z %Y')
            if tweet_date >= cutoff_date:
                recent_tweets.append(tweet)
        except ValueError as e:
            print(f"Error parsing date: {created_at_str}: {e}")
            continue

print(f"Found {len(tweets_data)} total tweets")
print(f"Filtered to {len(recent_tweets)} tweets from 2023 onwards\n")

# Analyze tweet patterns
total_chars = 0
tweet_texts = []
hashtags = []
mentions = []

for tweet in recent_tweets:
    text = tweet.get('full_text', '')
    if text:
        tweet_texts.append(text)
        total_chars += len(text)

        # Count hashtags
        entities = tweet.get('entities', {})
        for tag in entities.get('hashtags', []):
            hashtags.append(tag['text'])

        # Count mentions
        for mention in entities.get('user_mentions', []):
            mentions.append(mention['screen_name'])

# Basic stats
print("=== BASIC STATS ===")
print(f"Total tweets (2023+): {len(recent_tweets)}")
if recent_tweets:
    print(f"Avg tweet length: {total_chars / len(recent_tweets):.1f} chars")
print(f"Total hashtags: {len(hashtags)}")
print(f"Total mentions: {len(mentions)}\n")

# Top hashtags
if hashtags:
    top_hashtags = Counter(hashtags).most_common(10)
    print("=== TOP HASHTAGS ===")
    for tag, count in top_hashtags:
        print(f"  #{tag}: {count}")
    print()

# Top mentions
if mentions:
    top_mentions = Counter(mentions).most_common(10)
    print("=== TOP MENTIONS ===")
    for mention, count in top_mentions:
        print(f"  @{mention}: {count}")
    print()

# Save recent tweets for further analysis
output_file = "/root/.openclaw/workspace/recent_tweets.json"
with open(output_file, 'w') as f:
    json.dump(recent_tweets, f, indent=2)

print(f"Saved {len(recent_tweets)} recent tweets to {output_file}")

# Show sample tweets
if recent_tweets:
    print("\n=== SAMPLE TWEETS (most recent 5) ===")
    for i, tweet in enumerate(recent_tweets[:5]):
        print(f"\n{i+1}. [{tweet.get('created_at', 'unknown date')}]")
        print(f"   {tweet.get('full_text', '')[:200]}")
