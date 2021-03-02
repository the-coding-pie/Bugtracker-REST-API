from rest_framework import serializers
from .models import Project
from users.serializers import UserSerializer
from django.template.defaultfilters import slugify

class ProjectSerializer(serializers.ModelSerializer):
    lead = UserSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['name', 'key', 'lead', 'created_at', 'collaborators']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name']
    