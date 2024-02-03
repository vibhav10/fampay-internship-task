from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(User)
class CustomUserView(UserAdmin):
    list_display = ('email', 'is_staff','is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2', 'full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    ) 

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
