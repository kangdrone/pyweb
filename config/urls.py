from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_views.index),            #127.0.0.1:8000/
    path('pybo/', include('pybo.urls')),   #127.0.0.1:8000/pybo/
    path('common/', include('common.urls')),#127.0.0.1:8000/common/
    path('poll/', include('poll.urls')),
]
