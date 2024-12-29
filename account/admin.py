from django.contrib import admin
from .models import AuthUser, UserProfile, BlacklistedToken
# Register your models here.

@admin.register(AuthUser)
class AdminAuthUser(admin.ModelAdmin):
	list_display = ['id', 'email', 'is_active', 'is_verified']
	list_editable = ['is_active',]
	list_display_links = ['email']
	readonly_fields = ['email']


@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
	list_display = ['id', 'user', 'age', 'gender']
	list_display_links = ['id', 'user']
	list_filter = ['gender']


@admin.register(BlacklistedToken)
class AdminBlacklistToken(admin.ModelAdmin):
	list_display = ['token', 'blacklisted_at']
