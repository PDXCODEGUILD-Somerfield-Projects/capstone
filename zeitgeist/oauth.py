from requests_oauthlib import OAuth1Session
from .settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

def request_twitter_token():
    '''Gets client token from Twitter'''
    token_oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET)
    twitter_token_request_url = 'https://api.twitter.com/oauth/request_token'
    fetch_response = token_oauth.fetch_request_token(twitter_token_request_url)
    return fetch_response


def get_twitter_authorization_url():
    fetch_response = request_twitter_token()
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    request_oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET,
                               resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret)
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    twitter_authorization_url = request_oauth.authorization_url(base_authorization_url)
    return twitter_authorization_url
