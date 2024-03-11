from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_html_avatar', 'date_birth', 'is_staff')
    list_display_links = ('username', )

    def get_html_avatar(self, object):
        if object.avatar:
            return mark_safe(f"<img src='{object.avatar.url}' width=50>")
        return 'No avatar'

    get_html_avatar.short_description = "Avatar miniature"


