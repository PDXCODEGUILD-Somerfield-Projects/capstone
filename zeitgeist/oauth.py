from django.utils.decorators import make_middleware_decorator
from requests_oauthlib import OAuth1Session
from .settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from json import loads


TWITTER_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TWITTER_AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
TWITTER_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
TWITTER_VERIFY_CRED_URL = 'https://api.twitter.com/1.1/account/verify_credentials.json'


class TwitterOauthMiddleware(object):

    # def __init__(self, get_response):
    #     print("init")
    #     self.get_response = get_response
    # #     # One-time configuration and initialization.

    def process_request(self, request):
        print("process request")
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        twitter_token = request.COOKIES['token']
        access_token_dict = loads(twitter_token)
        oauth = OAuth1Session(
            client_key=TWITTER_CONSUMER_KEY,
            client_secret=TWITTER_CONSUMER_SECRET,
            resource_owner_key=access_token_dict['oauth_token'],
            resource_owner_secret=access_token_dict['oauth_token_secret'])
        response = oauth.get(TWITTER_VERIFY_CRED_URL)


        print(response)

        # Code to be executed for each request/response after
        # the view is called.

        return None

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


def build_query_string(lat, lng):
    q = ('q=&geocode=' + lat + ',' + lng + ',' +
              '5mi&result_type=recent&lang=en&count=100')
    q = 'https://api.twitter.com/1.1/search/tweets.json?' + q
    return q


def get_twitter_data(latitude, longitude, access_token):
    access_token_dict = loads(access_token)
    oauth = OAuth1Session(
        client_key=TWITTER_CONSUMER_KEY,
        client_secret=TWITTER_CONSUMER_SECRET,
        resource_owner_key=access_token_dict['oauth_token'],
        resource_owner_secret=access_token_dict['oauth_token_secret'])
    query_string = build_query_string(latitude, longitude)
    return oauth.get(query_string)

