import requests, os, json, datetime, boto3
from datetime import date, datetime, timezone
from time import strftime
from main import *

bearer_token = my_bearer_token
search_url = "https://api.twitter.com/2/tweets/search/recent"
today_date = date.today()
converted_today_date = str(today_date)
x = "T01:01:00+00:00"
rfc_date = converted_today_date + x


#CHANGE max_results to 100 (only changing so I don't reach the limit)
query_params = {'query': '(Powell -is:retweet is:verified) OR (Monetary -is:retweet is:verified) OR (Markets -is:retweet is:verified) OR (Inflation -is:retweet is:verified)', 'tweet.fields': 'id,text,public_metrics', 'start_time': rfc_date,
                'max_results': 10, 'expansions': 'author_id',
                'user.fields': 'name,username'}

sns_client = boto3.client('sns')

def bearer_access(r):

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_access, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def accesstwitter():
    json_response = connect_to_endpoint(search_url, query_params)
    z = json.dumps(json_response, indent=4, sort_keys=True)
    python_dict_format = json.loads(z)
    cleaned_up_dict = python_dict_format['data']

    print(python_dict_format)

    for x in cleaned_up_dict:
        tweet_id = x['id']
        author_id = x['author_id']
        like_count = x['public_metrics']['like_count']
        tweet_text = x['text']
        new_tweet = TweetsModel(tweetid=tweet_id, authorid=author_id, likecount=like_count,tweet=tweet_text)
        db.session.add(new_tweet)
        db.session.commit()

    cleaned_up_dict_user = python_dict_format['includes']['users']
    for w in cleaned_up_dict_user:
        author_id = w['id']
        author_name = w['name']
        author_username = w['username']
        new_user = UserModel(userid=author_id, name=author_name, username=author_username)
        db.session.add(new_user)
        db.session.commit()
