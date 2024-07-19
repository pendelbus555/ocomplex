from django.urls import path

from .views import index
from .api import CitySearchCountAPIView

urlpatterns = [
    path("", index, name="index"),
    path("api/", CitySearchCountAPIView.as_view(), name="search"),
]
