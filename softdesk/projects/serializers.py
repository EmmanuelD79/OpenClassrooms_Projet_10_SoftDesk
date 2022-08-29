from rest_framework.serializers import ModelSerializer
from projects.models import Project, Contributor, Issue, Comment
from authentication.models import User


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class ContributorSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project__id',
    }

    class Meta:
        model = Contributor
        fields = '__all__'

class IssueSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project__id',
    }

    class Meta:
        model = Issue
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'issue_id': 'issue__id',
    }

    class Meta:
        model = Comment
        fields = '__all__'