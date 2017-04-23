from django.shortcuts import render, redirect
from .oauth import get_twitter_authorization_url


def home(request):
    authorization_url = get_twitter_authorization_url()
    return redirect(authorization_url)


def return_authorization(request):
    # twitter_data = get_twitter_data(user_token)
    twitter_response = render(request, 'return_authorization.html')
    twitter_response.set_cookie('user_token', request.GET['oauth_token'])
    return twitter_response


def coordinates(request):
    pass

