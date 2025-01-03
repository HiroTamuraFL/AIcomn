from django.db import models
#from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth import get_user_model


class UserRelation(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user_relations"
    )
    friend = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="friend_relations", default=None
    )
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"


class Messages(models.Model):
    description = models.TextField()
    sender_name = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="sender"
    )
    receiver_name = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="receiver"
    )
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name='イメージ画像', null=True, blank=True) # 追加

    class Meta:
        ordering = ("timestamp",)

