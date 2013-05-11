from django.db import models
from django.contrib.auth.models import User
from requirement.models import Requirement


class UserRequirement(models.Model):
    class Meta:
        unique_together= ('user', 'requirement')

    user = models.ForeignKey(User)
    requirement = models.ForeignKey('requirement.Requirement')
    completed_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    signed_by = models.ForeignKey(User, related_name='signed')
    completed = models.BooleanField(default=False)
    
        
        
        
        