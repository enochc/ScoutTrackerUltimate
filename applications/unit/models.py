from django.db import models
from utils.values import reverse_states

class UnitRequest(models.Model):
    unit = models.ForeignKey('unit.Unit')
    member = models.ForeignKey('userprofile.Userprofile')
    type = models.CharField(choices=(('request','request'),('invite','invite')),
                            max_length=10)
    email = models.CharField(max_length=100, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    

class Unit(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=True)
    council = models.ForeignKey('council.Council', null=True, blank=True)
    state = models.CharField(max_length="2", choices=reverse_states, blank=True)
    city = models.CharField(max_length="255", blank=True)
    calendar = models.CharField(max_length=255, blank=True, null=True)
    
    def scouts(self):
        return self.members.filter(position__youth=True)
    
    
    def __unicode__(self):
        return '%s'%self.number
    
class Patrol(models.Model):
    unit = models.ForeignKey(Unit)
    name = models.CharField(max_length=200)
    
    def scouts(self):
        return self.patrol_members.filter(position__youth=True)
    
    def __unicode__(self):
        return "%s - %s"%(self.unit.number, self.name)