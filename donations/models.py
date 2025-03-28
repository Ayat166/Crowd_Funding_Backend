from django.db import models
from users.models import User
from projects.models import Project
from django.utils import timezone

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_donations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_donated = models.DateTimeField(default=timezone.now)
