from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from twython import Twython
from profiles.models import Profile


def logout(request, redirect_url=settings.LOGOUT_REDIRECT_URL):
    """
        Nothing hilariously hidden here, logs a user out. Strip this out if your
        application already has hooks to handle this.
    """
    django_logout(request)
    return HttpResponseRedirect(request.build_absolute_uri(redirect_url))


def begin_auth(request):
    """The view function that initiates the entire handshake.

    For the most part, this is 100% drag and drop.
    """
    # Instantiate Twython with the first leg of our trip.
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET)

    # Request an authorization url to send the user to...
    callback_url = request.build_absolute_uri(reverse('twython_auth.views.thanks'))
    auth_props = twitter.get_authentication_tokens(callback_url)

    # Then send them over there, durh.
    request.session['request_token'] = auth_props

    #request.session['next_url'] = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    
    return HttpResponseRedirect(auth_props['auth_url'])


def thanks(request, redirect_url=settings.LOGIN_REDIRECT_URL):
    """A user gets redirected here after hitting Twitter and authorizing your app to use their data.

    This is the view that stores the tokens you want
    for querying data. Pay attention to this.

    """
    User = get_user_model()

    # Now that we've got the magic tokens back from Twitter, we need to exchange
    # for permanent ones and store them...
    oauth_token = request.session['request_token']['oauth_token']
    oauth_token_secret = request.session['request_token']['oauth_token_secret']
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
                      oauth_token, oauth_token_secret)

    # Retrieve the tokens we want...
    authorized_tokens = twitter.get_authorized_tokens(request.GET['oauth_verifier'])

    # If they already exist, grab them, login and redirect to a page displaying stuff.
    try:
        user = User.objects.get(username=authorized_tokens['user_id'])
    except User.DoesNotExist:
        twitter = Twython(
            settings.TWITTER_KEY, settings.TWITTER_SECRET,
            authorized_tokens['oauth_token'], authorized_tokens['oauth_token_secret']
        )
        user_info = twitter.verify_credentials()
        user_info.update(authorized_tokens)
        user_info['profile_id'] = user_info['id']
        profile, created = Profile.from_json(user_info)
        if created:
            profile.user = User.objects.create_user(
                user_info['profile_id'], password=user_info['oauth_token_secret']
            )
            profile.save()

    user = authenticate(
        username=user_info['profile_id'],
        password=user_info['oauth_token_secret']
    )
    login(request, user)
    redirect_url = request.session.get('next_url', redirect_url)

    return HttpResponseRedirect(redirect_url)
