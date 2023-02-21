from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserImages(admin.TabularInline):
    model = models.Image


class UserAdmin(admin.ModelAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'membership']
    inlines = [UserImages]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Image)