# 2. Third-party
from django.contrib import admin

# 3. Local
from .models import Profile

admin.site.register(Profile)
