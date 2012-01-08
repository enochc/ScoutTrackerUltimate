from django.db import models
from django.contrib.auth.models import User


class UserRank(models.Model):
    class Meta:
        unique_together= ('user', 'rank')

    user = models.ForeignKey(User)
    rank = models.ForeignKey('rank.Rank')
    completed_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    authorized_by = models.ForeignKey(User, related_name='authorized_by')
    earned = models.BooleanField(default=False)