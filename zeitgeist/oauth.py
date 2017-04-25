from requests_oauthlib import OAuth1Session
from .settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from json import dumps
from django.shortcuts import render, redirect

TWITTER_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TWITTER_AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
TWITTER_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'


def get_oauth_request_token(callback, error):
    oauth = OAuth1Session(
        client_key=TWITTER_CONSUMER_KEY,
        client_secret=TWITTER_CONSUMER_SECRET)
    fetch_response_json = oauth.fetch_request_token(TWITTER_REQUEST_TOKEN_URL)
    if fetch_response_json and fetch_response_json["oauth_callback_confirmed"]:
        resource_owner_key = fetch_response_json.get('oauth_token')
        resource_owner_secret = fetch_response_json.get('oauth_token_secret')
        return callback(resource_owner_key, resource_owner_secret)
    else:
        return error("Request token failed")


def build_oauth_url(resource_owner_key, resource_owner_secret):
    oauth = OAuth1Session(
        client_key=TWITTER_CONSUMER_KEY,
        client_secret=TWITTER_CONSUMER_SECRET,
        resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret)
    return oauth.authorization_url(TWITTER_AUTHORIZATION_URL)


def get_access_token(request):
    oauth_token = request.GET['oauth_token']
    oauth_verifier = request.GET['oauth_verifier']
    oauth = OAuth1Session(
        client_key=TWITTER_CONSUMER_KEY,
        client_secret=TWITTER_CONSUMER_SECRET,
        resource_owner_key=oauth_token)
    access_token = oauth.fetch_access_token(url=TWITTER_ACCESS_TOKEN_URL, verifier=oauth_verifier)
    return access_token




# def request_twitter_token():
#     '''Gets client token from Twitter'''
#     token_oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET)
#     twitter_token_request_url = 'https://api.twitter.com/oauth/request_token'
#     fetch_response = token_oauth.fetch_request_token(twitter_token_request_url)
#     return fetch_response


# def get_twitter_authorization_url():
#     token_oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET)
#     twitter_token_request_url = 'https://api.twitter.com/oauth/request_token'
#     fetch_response = token_oauth.fetch_request_token(twitter_token_request_url)
#     resource_owner_key = fetch_response.get('oauth_token')
#     resource_owner_secret = fetch_response.get('oauth_token_secret')
#     request_oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET,
#                                resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret)
#     base_authorization_url = 'https://api.twitter.com/oauth/authorize'
#     twitter_authorization_url = request_oauth.authorization_url(base_authorization_url)
#     return twitter_authorization_url

# def build_query_string(lat, lng):
#     # percent encode the query string
#     q = quote('?q=&geocode=' + lat + ',' + lng + ',' + '1mi&result_type=recent&count=100')
#     return q

#
# def get_access_token(request, verifier):
#     access_token_url = 'https://api.twitter.com/oauth/access_token'
#     resource_owner_key = request.COOKIES.get('resource_owner_key')
#     resource_owner_secret = request.COOKIES.get('resource_owner_secret')
#     oauth = OAuth1Session(client_key=TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET,
#                           resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret,
#                           verifier=verifier)
#     oauth_access_tokens = oauth.fetch_access_token(access_token_url)
#     print('oauth_access_tokens: ' + oauth_access_tokens)
#
#     return oauth_access_tokens
#
#



#
#
# def get_some_twitter_data(request, lat, lng):
#     resource_owner_key = request.COOKIES.get('resource_owner_key')
#     resource_owner_secret = request.COOKIES.get('resource_owner_secret')
#     twitter_search_url = 'https://api.twitter.com/1.1/search/tweets.json'
#     twitter_query = build_query_string(lat, lng)
#     oauth = OAuth1Session(client_key=TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET,
#                           resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret)
#     twitter_data = oauth.get(twitter_search_url + twitter_query)
#     print(twitter_data)
#     return twitter_data

