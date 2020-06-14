from django.conf import settings
import twython
from django_rq import job

from profiles.models import Profile

@job
def get_friends(profile_id, friend_cursor=-1):
    profile = Profile.objects.get(profile_id=profile_id)
    api = twython.Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
                          profile.oauth_token, profile.oauth_token_secret)
    response = api.get_friends_ids(user_id=profile_id, count=5000, cursor=friend_cursor)
    id_list = response['ids']
    next_cursor = response['next_cursor']
    (cur_list, id_list) = id_list[:100], id_list[100:]
    while len(cur_list) > 0:
        existing = Profile.objects.filter(
            profile_id__in=cur_list).values_list('profile_id', flat=True)
        cur_list = set(cur_list) - set(existing)
        for user in api.lookup_user(','.join(cur_list)):
            Profile.from_json(user.)


    #print api.get_user_timeline(count=5)
    # get all friend/follower id's
    # If friend/follower id exists and is linked to profile, do nothing
    # if friend/follower id exists and is not linked to profile, link it
    # if friend/follower id does not exist, enqueue job to create it (job will link)


"""
api.get_friends_ids(user_id=7686862, count=6)
{u'ids': [2474023375, 70524499, 20548503, 320949928, 379839760, 1666038950],
 u'next_cursor': 1493131132302123646,
 u'next_cursor_str': u'1493131132302123646',
 u'previous_cursor': 0,
 u'previous_cursor_str': u'0'}


 api.get_followers_ids(user_id=7686862, count=5000)
 {u'ids': [3041537756,
  253005885,
  70524499,
  ...
  7043692],
 u'next_cursor': 0,
 u'next_cursor_str': u'0',
 u'previous_cursor': 0,
 u'previous_cursor_str': u'0'}
"""