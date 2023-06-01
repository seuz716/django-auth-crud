from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Default Title')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=False)
    completed = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title + '-by ' +  self.author.username

    def mark_as_completed(self):
        self.completed = True
        self.save()

    def mark_as_pending(self):
        self.completed = False
        self.save()
