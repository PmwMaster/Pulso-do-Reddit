import argparse
import requests
import json
import time
from datetime import datetime

def fetch_posts(subreddit, limit=100):
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    posts = []
    after = None
    
    while len(posts) < limit:
        params = {'limit': 100}
        if after:
            params['after'] = after
            
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Error fetching {subreddit}: {response.status_code}")
                break
                
            data = response.json()
            if 'data' not in data or 'children' not in data['data']:
                break
                
            new_posts = data['data']['children']
            if not new_posts:
                break
                
            posts.extend(new_posts)
            after = data['data']['after']
            
            if not after:
                break
                
            time.sleep(2) # Be polite to API
            
        except Exception as e:
            print(f"Exception fetching {subreddit}: {e}")
            break
            
    return posts[:limit]

def calculate_score(post_data):
    # Simple engagement score: ups + (num_comments * 2)
    ups = post_data.get('ups', 0)
    comments = post_data.get('num_comments', 0)
    return ups + (comments * 2)

def analyze_subreddits(subreddits, limit, top_n):
    results = {}
    
    for sub in subreddits:
        print(f"Fetching posts from r/{sub}...")
        raw_posts = fetch_posts(sub, limit)
        
        analyzed_posts = []
        for post in raw_posts:
            data = post['data']
            score = calculate_score(data)
            analyzed_posts.append({
                'title': data.get('title'),
                'url': data.get('url'),
                'permalink': f"https://reddit.com{data.get('permalink')}",
                'score': score,
                'ups': data.get('ups'),
                'comments': data.get('num_comments'),
                'created_utc': datetime.utcfromtimestamp(data.get('created_utc')).strftime('%Y-%m-%d %H:%M:%S')
            })
            
        # Sort by score descending
        analyzed_posts.sort(key=lambda x: x['score'], reverse=True)
        results[sub] = analyzed_posts[:top_n]
        
    return results

def main():
    parser = argparse.ArgumentParser(description='Analyze Reddit posts.')
    parser.add_argument('--subreddits', nargs='+', required=True, help='List of subreddits')
    parser.add_argument('--limit', type=int, default=100, help='Max posts to fetch per subreddit')
    parser.add_argument('--top', type=int, default=5, help='Number of top posts to return')
    
    parser.add_argument('--output', help='Output JSON file path')
    
    args = parser.parse_args()
    
    results = analyze_subreddits(args.subreddits, args.limit, args.top)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
