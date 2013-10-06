from django.db import models
from utils.funcs import get_sized_image

AWARD_TYPES = ((0,"Merit Badge"),
               )

class AwardRequirement(models.Model):
            
    order = models.IntegerField()
    desc = models.TextField()
    short_desc = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return '%s #%s'% (self.rank, self.order)
    
    class Meta:
        ordering = ['order']


class Award(models.Model):
    type = models.IntegerField(choices = AWARD_TYPES, default=0)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='awards')
    group = models.ManyToManyField('self', related_name="group", blank=True, null=True)
    required = models.BooleanField(default=False)
    requirements = models.ManyToManyField(AwardRequirement, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    @property
    def thumbnail(self):
        return get_sized_image(self.image,(30,30))
    
    @property
    def num_requirements(self):
        return self.requirements.filter(type=0).count()
    
    def next(self):
        try:
            return Rank.objects.get(order=self.order+1)
        except Rank.DoesNotExist:
            return None
    
