import json


from django.shortcuts import render, redirect
from json import dumps, loads

from zeitgeist.twitter_data import deserialized_twitter_data, pull_tweet_text, \
    find_most_common_parcels
from .oauth import get_oauth_request_token, get_access_token, build_oauth_url, get_twitter_data
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')


def home(request):
    if 'token' in request.COOKIES:
        token = loads(request.COOKIES['token'])
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


def coordinates(request):
    my_lat = request.GET.get('lat')
    my_lng = request.GET.get('lng')
    twitter_token = request.COOKIES['token']
    twitter_response = get_twitter_data(my_lat, my_lng, twitter_token)

    # deserialize the Twitter response json object into tweets
    tweet_list = deserialized_twitter_data(twitter_response.json())
    pull_tweet_text(tweet_list)
    hashtag_list = find_most_common_parcels(tweet_list, 'hashtags')
    user_mention_list = find_most_common_parcels(tweet_list, 'user_mentions')
    urls_list = find_most_common_parcels(tweet_list, 'urls')

    lat_lng_json = JsonResponse({'lat': my_lat, 'lng': my_lng})
    return lat_lng_json

