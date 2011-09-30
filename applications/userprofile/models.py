from django.db import models
from django.contrib.auth.models import User

from applications.troop.models import Troop

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	troop = models.ForeignKey(Troop, blank=True, null=True)
	
	@property
	def fullname(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)

	def test(self):
		return 'test'