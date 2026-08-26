# 2. Third-party
from django.contrib import admin

# 3. Local
from .models import Order

admin.site.register(Order)
