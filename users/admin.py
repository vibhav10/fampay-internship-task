from django.contrib import admin
from .models import User, APIKey, SearchString
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


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'last_used')
    search_fields = ('user', 'key')
    ordering = ('user', 'key', 'last_used')
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('user', 'key',)}),
    )   
    add_fieldsets = (
        (None, {'fields': ('user', 'key',)}),
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        instance.key = instance.key
        instance.save()
        return instance
    

@admin.register(SearchString)
class SearchStringAdmin(admin.ModelAdmin):
    list_display = ('user', 'search')
    search_fields = ('user', 'search')
    ordering = ('user', 'search')
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('user', 'search',)}),
    )   
    add_fieldsets = (
        (None, {'fields': ('user', 'search',)}),
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        instance.search = instance.search
        instance.save()
        return instance