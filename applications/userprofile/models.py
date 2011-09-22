from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.ForeignKey(User)
	
	@property
	def fullname(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)

	def test(self):
		return 'test'