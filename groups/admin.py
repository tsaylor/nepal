from django.contrib import admin
from groups.models import Group


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Group, GroupAdmin)
