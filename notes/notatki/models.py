from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username}'

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.title}'

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    notes = models.ManyToManyField(Note, blank=True)
    def __str__(self):
        return f'{self.name}'