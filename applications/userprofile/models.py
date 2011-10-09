from django.db import models
from django.contrib.auth.models import User

from applications.troop.models import Troop
from utils.values import states
from position.models import Position
from userrequirement.models import UserRequirement

def reverse_states():
	return [[s[1], s[0]] for s in states]


class Userprofile(models.Model):
	class Meta:
		permissions = (
            ("add_leaders", "Can add other leaders who can add other scouts"),
            ("add_scouts", "Can add scouts"),
            ("edit_scouts", "Can edit scouts"),
            ("mark_requirements", "Can sign off requirements"),
        )
		
	user = models.OneToOneField(User, related_name='profile', null=True, blank=True)
	nickname = models.CharField(max_length=50, null=True, blank=True)
	
	troop = models.ForeignKey(Troop, blank=True, null=True, related_name='members', default=1)
	position = models.ForeignKey('position.Position', default=2)
	birthday = models.DateTimeField(null=True, blank=True)
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	
	state = models.CharField(max_length=2, choices=reverse_states(), default='UT')
	city = models.CharField(max_length=100, null=True, blank=True)
	street1 = models.CharField(max_length=255, help_text='Street name and house number.', null=True, blank=True)
	street2 = models.CharField(max_length=100, help_text='Floor or room number.', null=True, blank=True)
	lat = models.IntegerField(null=True, blank=True, help_text='latitude')
	lng = models.IntegerField(null=True, blank=True, help_text='longitude')
	

	@property
	def fullname(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)
	
	def __unicode__(self):
		return self.nickname or self.user.first_name or self.username
	
	@property
	def name(self):
		return self.__unicode__()
	
	def user_requirement(self, req):
		try:
			r = UserRequirement.objects.get(user=self.user, requirement=req)
			return r
		except UserRequirementDoesNotExist:
			return None
	
	def completed_list(self, rank=None):
		urs = UserRequirement.objects.filter(user=self.user, completed=True)
		if rank is not None:
			urs = urs.filter(requirement__rank=rank)
		return [int(ur.requirement.id) for ur in urs]
	
	