from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    current_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # New field
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    tags = models.CharField(max_length=255)  # Comma-separated tags
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # New field for average rating

    def is_below_25_percent(self):
        """Check if donations are less than 25% of the total target."""
        return self.current_donations < (self.total_target * 0.25)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def update_avg_rating(self):
        """
        Updates the average rating of the project based on its ratings.
        """
        ratings = self.ratings.all()
        if ratings.exists():
            self.avg_rating = ratings.aggregate(models.Avg('score'))['score__avg']
        else:
            self.avg_rating = 0.00
        self.save()

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField()  # Example: 1 to 5 stars

    class Meta:
        unique_together = ('user', 'project')  # Ensure a user can rate a project only once

    def save(self, *args, **kwargs):
        """
        Override the save method to update the project's average rating.
        """
        super().save(*args, **kwargs)
        self.project.update_avg_rating()
