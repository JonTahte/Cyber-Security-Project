from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Comment(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	pub_time = models.DateTimeField(default=timezone.now)
