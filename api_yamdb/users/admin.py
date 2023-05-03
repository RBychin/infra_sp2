from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'confirmation_code',
    )
    list_display_links = (
        'pk',
        'username',
    )
    empty_value_display = '-пусто-'
    list_editable = ('role',)
    search_fields = ('username',)
    list_filter = ('role',)
    list_select_related = False
