from django.db import models
from users.models import User
from projects.models import Project

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    REPORT_CHOICES = [
        ('project', 'Project'),
        ('comment', 'Comment'),
        ('comment_reply', 'CommentReply')  # Add CommentReply as a report type
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=15, choices=REPORT_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    comment_reply = models.ForeignKey('CommentReply', on_delete=models.CASCADE, blank=True, null=True)  # New field
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
