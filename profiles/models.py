import json

from django.db import models
from util.base import BaseModel

class Profile(BaseModel):
    user = models.ForeignKey('auth.user', null=True, blank=True)
    profile_id = models.BigIntegerField(db_index=True)
    screen_name = models.CharField(max_length=45, db_index=True)
    name = models.CharField(max_length=45)
    location = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    profile_image_url = models.URLField()
    oauth_token = models.CharField(max_length=200)
    oauth_token_secret = models.CharField(max_length=200)
    # _user_json = models.TextField(blank=True)

    # @property
    # def user_json(self):
    #     return json.loads(self._user_json)
    # @user_json.setter
    # def user_json(self, value):
    #     self._user_json = json.dumps(value)
    
    def get_pic(self):
        return {'normal': self.profile_image_url,
                'bigger': self.profile_image_url.replace('_normal', '_bigger'),
                '200': self.profile_image_url.replace('_normal', '_200x200'),
                '400': self.profile_image_url.replace('_normal', '_400x400')}


    @classmethod
    def from_json(cls, data):
        """ returns (obj, created) for the profile data passed to it """
        field_names = [a.name for a in cls._meta.fields]
        data = dict([(key, data[key]) for key in data if key in field_names])
        return cls.objects.update_or_create(profile_id=data['profile_id'], defaults=data)


class Status(BaseModel):
    profile = models.ForeignKey(Profile)
    status_id = models.BigIntegerField(db_index=True)
    text = models.CharField(max_length=200)
    _status_json = models.TextField(blank=True)

    @property
    def status_json(self):
        return json.loads(self._status_json)
    @status_json.setter
    def status_json(self, value):
        self._status_json = json.dumps(value)
