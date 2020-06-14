from django.db.models import Q
from rest_framework import serializers, viewsets

from profiles.models import Profile


# Serializers define the API representation.
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    pic_url = serializers.DictField(source='get_pic', child=serializers.CharField())

    class Meta:
        model = Profile
        fields = ('profile_id', 'screen_name', 'name', 'description', 'pic_url')


# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    model = Profile
    serializer_class = ProfileSerializer

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        qs = self.model.objects.all()
        if self.request.is_authenticated():
            user = self.request.user
            qs = qs.filter(Q(follows=user) |
                           Q(followed_by=user))
        if search != '':
            qs = qs.filter(Q(name__icontains=search) |
                           Q(description__icontains=search))
        return qs
