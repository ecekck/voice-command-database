from django.contrib import admin
from .models import Users

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "authority_level", "is_staff", "is_active")
    search_fields = ("username", "email")
# Register your models here.
