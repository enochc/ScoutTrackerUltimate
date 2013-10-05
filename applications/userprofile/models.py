import datetime
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User, Group

from applications.troop.models import Troop
from utils.values import reverse_states
from utils.funcs import add_months
from position.models import Position
from userrequirement.models import UserRequirement


class UserGoal(models.Model):
	date_due = models.DateTimeField()
	name = models.CharField(max_length=200)
	notes = models.TextField(null=True, blank=True)
	user = models.ForeignKey("userprofile.Userprofile", related_name="goals")
	klass = models.CharField(max_length=50, null=True, blank=True)
	
			

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
	
	troop = models.ForeignKey(Troop, blank=True, null=True, related_name='members')
	position = models.ForeignKey('position.Position', default=2)
	__original_position = None;
	birthday = models.DateTimeField(null=True, blank=True)
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	
	state = models.CharField(max_length=2, choices=reverse_states, default='UT', null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	street1 = models.CharField(max_length=255, help_text='Street name and house number.', null=True, blank=True)
	street2 = models.CharField(max_length=100, help_text='Floor or room number.', null=True, blank=True)
	lat = models.IntegerField(null=True, blank=True, help_text='latitude')
	lng = models.IntegerField(null=True, blank=True, help_text='longitude')
	google_oauth_token = models.CharField(max_length=255, null=True, blank=True)
	google_refresh_token = models.CharField(max_length=255, null=True, blank=True)
	google_code = models.CharField(max_length=255, null=True, blank=True)
	google_id = models.CharField(max_length=25, null=True, blank=True)

	
	def is_scout(self):
		return self.position.youth
	
	def __init__(self, *args, **kwargs):
	    super(Userprofile, self).__init__(*args, **kwargs)
	    self.__original_position = self.position
	
	def has_google_login(self):
		return self.google_id is not None and len(self.google_id)>0 and self.google_id != 'None'
	
	def set_goals(self):
		if self.goals.all().count()==0:
			from rank.models import Rank
		
			eagle = self.birthday.replace(year=(self.birthday.year+18))
			life = add_months(-6, eagle)
			star = add_months(-6, life)
			frstcls = add_months(-4, star)

			goal_data = [('Receive Eagle',eagle),
				('Receive Life',life),
				('Receive Star',star),
				('Receive First Class',frstcls)]
			for data in goal_data:
				try:
					goal = UserGoal.objects.get(name=data[0], user=self)
					goal.date_due = data[1]
					
				except UserGoal.DoesNotExist:
					goal = UserGoal(name=data[0],date_due=data[1], user=self)
				goal.save()
				self.goals.add(goal)

	@property
	def fullname(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)

	def __unicode__(self):
		return self.nickname or (self.user.first_name if self.user else "unknown")
	
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
	
	def rank(self):
		from rank.models import Rank
		ranks = Rank.objects.filter(userranks__user=self.user).order_by('-order')
		if ranks.count() > 0:
			return ranks[0]
	
	def save(self, *args, **kwargs):

		if self.position != self.__original_position and self.pk:
			"""update user group and update permissions
			"""
			group, created = Group.objects.get_or_create(name=self.position.name)
			self.user.groups.clear()
			group.user_set.add(self.user)
			self.__original_position = self.position
			
		super(Userprofile, self).save(*args, **kwargs)
		
		if self.birthday and self.is_scout():
			self.set_goals()
    	
    	
   
    	
    	
	