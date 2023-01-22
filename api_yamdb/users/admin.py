

from django.contrib import admin

from .models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_dispaly = ('__all__',)


admin.site.register(User, CustomUserAdmin)
