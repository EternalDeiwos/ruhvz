from django.contrib import admin
from ruhvz.users.models import Profile

class ProfileAdmin(admin.ModelAdmin):
	search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')

admin.site.register(Profile, ProfileAdmin)