from enum import unique

from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    notes = models.ManyToManyField(Note, blank=True)
    def __str__(self):
        return self.name