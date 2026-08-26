# 2. Third-party
from django.urls import path

# 3. Local
from .views import BaseInfoView

urlpatterns = [
    path("base-info/", BaseInfoView.as_view(), name="base-info"),
]
