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
    
    def save(self, *args, **kwargs):
        super(UserRequirement, self).save(*args, **kwargs)
        num_reqs = self.requirement.rank.num_requirements
        completed_reqs = len(self.user.profile.completed_list(self.requirement.rank))      
        
        if self.completed:
            if num_reqs == completed_reqs:
                return True
            else:
                return False
        return False
        
        