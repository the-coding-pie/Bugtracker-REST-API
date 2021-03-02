from rest_framework import serializers
from .models import Issue
from users.serializers import UserSerializer
from projects.serializers import ProjectCreateSerializer
from users.models import User

class IssueSerializer(serializers.ModelSerializer):
    assignee = UserSerializer()
    reporter = UserSerializer()

    class Meta:
        model = Issue
        fields = ['title', 'key', 'description', 'link', 'assignee', 'status', 'priority', 'reporter', 'created_at', 'due_date']

class IssueCreateSerializer(serializers.ModelSerializer):
    assignee = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(), required=False)

    class Meta:
        model = Issue
        fields = ['title', 'description', 'link', 'assignee', 'status', 'priority', 'due_date']