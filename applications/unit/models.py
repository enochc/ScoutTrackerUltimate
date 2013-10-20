from django.db import models
from utils.values import reverse_states
from utils.funcs import email

class UnitRequest(models.Model):
    class Meta():
        unique_together = ("unit","member")
        
    unit = models.ForeignKey('unit.Unit')
    member = models.ForeignKey('userprofile.Userprofile')
    type = models.CharField(choices=(('request','request'),('invite','invite')),
                            max_length=10)
    email = models.CharField(max_length=100, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    
    def notify(self, is_approved=False):
        if self.type == "request":
            to = [u.email for u in self.unit.adults()]
            if is_approved:
                template = "request_approved.html"
            else:
                template = "request.html"
            email('request.html', to, {'req':self})
            
    def approve(self):
        if self.type == "request":
            self.member.unit = self.unit
            self.member.save()
            self.notify(True)
            self.delete()
            
    
    

class Unit(models.Model):

    number = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    council = models.ForeignKey('council.Council', null=True, blank=True)
    state = models.CharField(max_length="2", choices=reverse_states, blank=True)
    city = models.CharField(max_length="255", blank=True)
    calendar = models.CharField(max_length=255, blank=True, null=True)
    
    def scouts(self):
        return self.members.filter(position__youth=True)
    
    def adults(self):
        return self.members.filter(position__youth=False)
    
    def __unicode__(self):
        return '%s'%self.number
    
class Patrol(models.Model):
    unit = models.ForeignKey(Unit)
    name = models.CharField(max_length=200)
    
    def scouts(self):
        return self.patrol_members.filter(position__youth=True)
    
    def __unicode__(self):
        return "%s - %s"%(self.unit.number, self.name)