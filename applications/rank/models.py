from django.db import models
from utils.funcs import get_sized_image




class Rank(models.Model):
    class Meta:
        ordering = ['order']
        
    name = models.CharField(max_length=255)
    patch = models.ImageField(upload_to='rank')
    patch_thumb = models.ImageField(upload_to='rank', null=True, blank=True)
    order = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    
    @property
    def thumbnail(self):
        return get_sized_image(self.patch,(30,30))
    
    @property
    def num_requirements(self):
        return self.requirements.filter(type=0).count()
    
