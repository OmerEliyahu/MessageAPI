from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from api.views.message import message_urls

urlpatterns = [
    url('', include(message_urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
]
