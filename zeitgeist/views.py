import json


from django.shortcuts import render, redirect
from json import dumps, loads

# from zeitgeist.twitter_data import parse_twitter_data
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


def coordinates(request):
    my_lat = request.GET.get('lat')
    my_lng = request.GET.get('lng')
    twitter_token = request.COOKIES['token']
    twitter_response = get_twitter_data(my_lat, my_lng, twitter_token)
    # twitter_json_data = twitter_response.json()
    # parse_twitter_data(twitter_json_data)
    # parse_twitter_data(twitter_response)
    lat_lng_json = JsonResponse({'lat': my_lat, 'lng': my_lng})
    return lat_lng_json

