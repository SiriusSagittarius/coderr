# 2. Third-party
from django.contrib import admin

# 3. Local
from .models import Offer, OfferDetail

admin.site.register(Offer)
admin.site.register(OfferDetail)
