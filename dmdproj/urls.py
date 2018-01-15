"""
    dmdproj URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('findshop/', include('findshop.urls')),
    path('admin/', admin.site.urls),
]
