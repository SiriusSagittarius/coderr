# 2. Third-party
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# 3. Local
from .models import User

admin.site.register(User, UserAdmin)
