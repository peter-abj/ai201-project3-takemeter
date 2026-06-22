#!/usr/bin/env python3
"""
Collect film discussion posts from r/TrueFilm for classification.
Requires PRAW (pip install praw) and a Reddit API credential set.

To use:
1. Create a Reddit app at https://www.reddit.com/prefs/apps
2. Set environment variables or provide credentials:
   - export REDDIT_CLIENT_ID="your_client_id"
   - export REDDIT_CLIENT_SECRET="your_client_secret"
   - export REDDIT_USER_AGENT="your_user_agent"
3. Run: python collect_data.py --output data.csv --limit 300

The script collects more than 200 to account for filtering short/spam posts.
"""

import os
import csv
import argparse
from datetime import datetime
try:
    import praw
except ImportError:
    print("PRAW not installed. Install with: pip install praw")
    exit(1)


def collect_posts(output_file, limit=300):
    """Collect posts from r/TrueFilm."""

    # Initialize Reddit API
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    subreddit = reddit.subreddit("TrueFilm")
    posts = []

    print(f"Collecting posts from r/TrueFilm (target: {limit})...")

    # Collect from top posts (past 6 months)
    for submission in subreddit.top(time_filter="all", limit=limit):
        # Skip if it's a link post (we want self-posts with text)
        if submission.is_self and len(submission.selftext) > 100:
            posts.append({
                "text": submission.selftext,
                "title": submission.title,
                "score": submission.score,
                "created": datetime.fromtimestamp(submission.created_utc).isoformat()
            })

    # Also collect from new/hot
    for submission in subreddit.new(limit=limit // 2):
        if submission.is_self and len(submission.selftext) > 100:
            posts.append({
                "text": submission.selftext,
                "title": submission.title,
                "score": submission.score,
                "created": datetime.fromtimestamp(submission.created_utc).isoformat()
            })

    # Deduplicate by title (rough check)
    seen = set()
    unique_posts = []
    for post in posts:
        if post["title"] not in seen:
            seen.add(post["title"])
            unique_posts.append(post)

    print(f"Collected {len(unique_posts)} unique posts")

    # Save to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["text", "title", "score", "created", "label", "notes"])
        writer.writeheader()

        for post in unique_posts:
            writer.writerow({
                "text": post["text"],
                "title": post["title"],
                "score": post["score"],
                "created": post["created"],
                "label": "",  # To be filled in by annotator
                "notes": ""   # For borderline cases
            })

    print(f"Saved {len(unique_posts)} posts to {output_file}")
    print("Next: Review and annotate the 'label' column using your label definitions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect r/TrueFilm posts")
    parser.add_argument("--output", default="truefilm_raw.csv", help="Output CSV file")
    parser.add_argument("--limit", type=int, default=300, help="Limit of posts to collect")
    args = parser.parse_args()

    try:
        collect_posts(args.output, args.limit)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you've set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT")
