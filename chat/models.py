from django.contrib.auth.models import User
from django.db import models


class Friend(models.Model):
    userone = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requester')
    usertwo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requestee')
    statususerone = models.BooleanField(default=False)
    statususertwo = models.BooleanField(default=False)

    def __str__(self):
        return self.userone.username + ' and ' + self.usertwo.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['userone', 'usertwo'], name='unique_record'),
        ]
