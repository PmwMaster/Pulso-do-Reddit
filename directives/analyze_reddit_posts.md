# Directive: Analyze Reddit Posts

## Goal
Fetch recent posts from specific subreddits and identify high-engagement content.

## Inputs
*   `subreddits`: List of subreddit names (e.g., `["n8n", "automation"]`).
*   `limit`: Number of posts to fetch per subreddit (default: 100).
*   `top_n`: Number of top posts to return per subreddit (default: 5).

## Tool
*   `execution/reddit_public_analyzer.py`

## Instructions
1.  Run the `reddit_public_analyzer.py` script with the specified arguments.
    ```bash
    python execution/reddit_public_analyzer.py --subreddits n8n automation --limit 100 --top 5
    ```
2.  The script will output the results in JSON format or a readable report.
3.  Review the output for relevance.

## Output
*   A list of top posts with titles, URLs, and engagement scores.
