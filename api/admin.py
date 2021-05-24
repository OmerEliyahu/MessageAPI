from django.contrib import admin

from api.models.user import User
from api.models.message import Message

admin.site.register(User)
admin.site.register(Message)
