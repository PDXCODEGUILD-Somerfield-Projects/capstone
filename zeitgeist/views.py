from django.shortcuts import render, redirect
from .oauth import get_twitter_authorization_url


def home(request):
    authorization_url = get_twitter_authorization_url()
    return redirect(authorization_url)


def return_authorization(request):
    return render(request, 'return_authorization.html', {'token': request.GET['oauth_token']})
