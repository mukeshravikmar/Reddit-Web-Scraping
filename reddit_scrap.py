import time
import random
import httpx
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

base_url = 'https://www.reddit.com'

categories = [
    '/r/datascience',
    '/r/3d_printing',
    '/r/consumer_electronics',
    '/r/diy_electronics',
    '/r/programming',
    '/r/software_and_apps',
    '/r/streaming_services'
]

dataset = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

max_retries = 5


def fetch_with_backoff(url, params=None, headers=None, retries=max_retries):
    """Fetch data from the URL with exponential backoff on errors or rate limits."""
    delay = 1
    params = params or {}
    for attempt in range(retries):
        try:
            response = httpx.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                logging.info(f"Success: {url}")
                return response.json()
            elif response.status_code == 429:  
                retry_after = int(response.headers.get("Retry-After", delay))
                logging.warning(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after + random.uniform(1, 3))  
            else:
                logging.error(f"HTTP error {response.status_code}: {response.text}")
        except httpx.RequestError as e:
            logging.error(f"Request error: {e}")
        time.sleep(delay + random.uniform(1, 3))  
        delay *= 2 
    raise Exception(f"Failed to fetch data from {url} after {retries} retries.")


def extract_comments(comments, post_id, post_title, parent_comment_id=None):
    """Recursively extract all comments, including nested replies."""
    for comment in comments:
        if 'data' in comment and comment['kind'] == 't1': 
            comment_data = comment['data']
            dataset.append({
                'post_id': post_id,
                'post_title': post_title,
                'comment_id': comment_data['id'],
                'parent_comment_id': parent_comment_id,
                'comment': comment_data.get('body', 'No comment text'),
                'author': comment_data.get('author', 'Unknown')
            })
            if 'replies' in comment_data and comment_data['replies']:
                nested_comments = comment_data['replies']['data']['children']
                extract_comments(nested_comments, post_id, post_title, comment_data['id'])
for category in categories:
    url = base_url + category + "/hot.json"
    after_post_id = None
    for _ in range(2):  
        params = {
            'limit': 25, 
            'after': after_post_id
        }
        logging.info(f'Fetching posts from "{url}" with params {params}...')
        try:
            json_data = fetch_with_backoff(url, params, headers)
            if not ('data' in json_data and 'children' in json_data['data']):
                logging.error(f"Unexpected API response: {json_data}")
                break

            posts = json_data['data']['children']
            after_post_id = json_data['data']['after']

            for post in posts:
                post_data = post['data']
                post_id = post_data.get('id', 'Unknown')
                post_title = post_data.get('title', 'No title')
                post_subreddit = post_data.get('subreddit_name_prefixed', 'Unknown')

                logging.info(f'Fetching comments from "https://www.reddit.com/{post_subreddit}/comments/{post_id}.json"...')

                comment_url = f'https://www.reddit.com/{post_subreddit}/comments/{post_id}.json'
                try:
                    comments_data = fetch_with_backoff(comment_url, {}, headers)
                    if len(comments_data) > 1 and 'data' in comments_data[1]:
                        comments = comments_data[1]['data']['children']
                        extract_comments(comments, post_id, post_title)
                    else:
                        logging.error(f"Invalid comments data for post {post_id}: {comments_data}")
                except Exception as e:
                    logging.error(f"Failed to fetch comments for post ID {post_id}: {e}")
                time.sleep(1 + random.uniform(0.5, 1.5))  

        except Exception as e:
            logging.error(f"Error fetching posts: {e}")
df = pd.DataFrame(dataset)
df.to_csv('reddit_all_revuewcomments.csv', index=False)
logging.info("Data saved to reddit_all_comments.csv")
