from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("weather/", include("myapp.urls")),
    path('admin/', admin.site.urls),
]
