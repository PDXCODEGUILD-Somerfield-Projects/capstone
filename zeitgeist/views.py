import json

from django.shortcuts import render, redirect
from json import dumps, loads
from .oauth import get_oauth_request_token, get_access_token, build_oauth_url, get_twitter_data
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')


def home(request):
    if 'token' in request.COOKIES:
        token = loads(request.COOKIES['token'])
        print(token['oauth_token'], token['oauth_token_secret'])
        return render(request, 'home.html')
    else:
        print('no token')
        return get_oauth_request_token(
            lambda key, secret: redirect(build_oauth_url(key, secret)),
            lambda message: render(request, 'error.html', {'error': message}))


def authorization(request):
    access_token = get_access_token(request)
    response = redirect('/home')
    response.set_cookie('token', json.dumps(access_token))
    return response



# def home(request):
#     token_oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET)
#     twitter_token_request_url = 'https://api.twitter.com/oauth/request_token'
#     fetch_response = token_oauth.fetch_request_token(twitter_token_request_url)
#     resource_owner_key = fetch_response.get('oauth_token')
#     resource_owner_secret = fetch_response.get('oauth_token_secret')
#
#
#     request_oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET,
#                                resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret)
#     base_authorization_url = 'https://api.twitter.com/oauth/authorize'
#     twitter_authorization_url = request_oauth.authorization_url(base_authorization_url)
#
#     response = redirect(twitter_authorization_url)
#     response.set_cookie('resource_owner_key', resource_owner_key)
#     response.set_cookie('resource_owner_secret', resource_owner_secret)
#     return response
#
#
# def return_authorization(request):
#     oauth_response = render(request, 'authorization.html')
#     oauth_response.set_cookie('oauth_token', request.GET['oauth_token'])
#     verifier = request.GET['oauth_verifier']
#     access_token = get_access_token(request, verifier)
#     resource_owner_key_access_token = access_token.get('oauth_token')
#     resource_owner_secret_access_token = access_token.get('oauth_token_secret')
#     access_token.set_cookie('access_token', resource_owner_key_access_token)
#     access_token.set_cookie('access_secret', resource_owner_secret_access_token)
#
#
#
def coordinates(request):
    my_lat = request.GET.get('lat')
    my_lng = request.GET.get('lng')
    twitter_token = request.COOKIES['token']
    twitter_response = get_twitter_data(my_lat, my_lng, twitter_token)
    print(twitter_response)
    lat_lng_json = JsonResponse({'lat': my_lat, 'lng': my_lng})
    return lat_lng_json

