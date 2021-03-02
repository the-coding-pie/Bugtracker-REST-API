from django.db import models
from autoslug import AutoSlugField
from users.models import User
from projects.models import Project
from django.utils import timezone

class Issue(models.Model):
    STATUS_TYPES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    PRIORITY_TYPES = [
        ('N', 'None'),
        ('L', 'Low'),
        ('M', 'Medium'),
        ('C', 'Critical')
    ]
    
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    link = models.SlugField(max_length=255, blank=True, null=True)
    key = AutoSlugField(unique=True, populate_from='title', max_length=8, always_update=True)
    assignee = models.ForeignKey(User, related_name='assigned_issues', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=11, choices=STATUS_TYPES, default='Open')
    priority = models.CharField(max_length=2, choices=PRIORITY_TYPES, default='N')
    reporter = models.ForeignKey(User, blank=True, null=True, related_name='reported_issues', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)

    def __str__(self):
        return self.key