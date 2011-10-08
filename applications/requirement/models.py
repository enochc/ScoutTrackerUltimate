from django.db import models
from django.contrib.auth.models import User


from userrequirement.models import UserRequirement

REQUIREMENT_TYPES = ((0, "Standard"),
                     (1, "Dissabled"),
                     )

class Requirement(models.Model):
    class Meta:
        ordering = ['rank','order']
        unique_together = (("rank", "order", "type"),)
        
    order = models.IntegerField()
    rank = models.ForeignKey('rank.Rank')
    desc = models.TextField()
    short_desc = models.CharField(max_length=255, null=True, blank=True)
    type = models.IntegerField(choices=REQUIREMENT_TYPES, default=0)
    
    def __unicode__(self):
        return '%s #%s'% (self.rank, self.order)
    
    """
    def has_completed(self, user):
        try:
            ur = UserRequirement.objects.get(requirement=self, user=User)
            return ur.completed
        except UserRequirement.DoesNotExist:
            return False
    """
