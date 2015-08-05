from django.db import models
from django.conf import settings
from util.base import BaseModel


class Group(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
