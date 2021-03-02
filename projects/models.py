from django.db import models
from autoslug import AutoSlugField
from users.models import User

class Project(models.Model):
    name = models.CharField(max_length=120, unique=True)
    key = AutoSlugField(unique=True, populate_from='name', max_length=24, always_update=True)
    lead = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collaborators = models.ManyToManyField(User, blank=True)
    # img

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.key