from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    id = models.AutoField(unique=True, primary_key=True, serialize=False)
    sender = models.ForeignKey(on_delete=models.CASCADE, to='api.User', related_name='sent_messages')
    receiver = models.ForeignKey(on_delete=models.CASCADE, to='api.User', related_name='received_messages')
    message = models.TextField()
    subject = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'message'



