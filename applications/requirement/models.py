from django.db import models

from applications.rank.models import Rank

REQUIREMENT_TYPES = ((0, "Standard"),
                     (1, "Dissabled"),
                     )

class Requirement(models.Model):
    class Meta:
        ordering = ['rank','order']
        
    order = models.IntegerField()
    rank = models.ForeignKey(Rank)
    desc = models.TextField()
    type = models.IntegerField(choices=REQUIREMENT_TYPES, default=0)
    
    def __unicode__(self):
        return '%s #%s'% (self.rank, self.order)
    
    
