from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api_app/', include('api_app.urls')),
    path('admin/', admin.site.urls),
]
