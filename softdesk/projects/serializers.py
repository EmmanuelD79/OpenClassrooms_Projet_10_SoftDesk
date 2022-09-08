from rest_framework import serializers
from projects.models import Project, Contributor, Issue, Comment
from authentication.models import User
from django.shortcuts import get_object_or_404


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type']


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']


class ContributorListSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project__id',
    }

    class Meta:
        model = Contributor
        fields = ['user_id','permission', 'role']



class ContributorSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project__id',
    }

    email = serializers.EmailField(max_length=None, min_length=3, allow_blank=False, write_only=True)


    class Meta:
        model = Contributor
        fields = ['email','permission', 'role']
        

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.filter(email=email)
        if not user:
            raise serializers.ValidationError({'user': "User don't exist"})
        validated_data.pop('email')
        validated_data['user_id'] = get_object_or_404(user)
        return Contributor.objects.create(**validated_data)


class IssueListSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project__id',
    }

    class Meta:
        model = Issue
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project__id',
    }

    assignee_user_email = serializers.EmailField(max_length=None, min_length=3, allow_blank=False, write_only=True)

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'status', 'assignee_user_email']
    
    def create(self, validated_data):
        assignee_user_email = validated_data.pop('assignee_user_email')
        user = User.objects.filter(email=assignee_user_email)
        if not user:
            raise serializers.ValidationError({'user': "Assignee User don't exist"})
        validated_data['assignee_user_id'] = get_object_or_404(user)
        return Issue.objects.create(**validated_data)

class CommentSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'issue_id': 'issue__id',
    }

    class Meta:
        model = Comment
        fields = ['description']

class CommentListSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'issue_id': 'issue__id',
    }

    class Meta:
        model = Comment
        fields = '__all__'

class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model: User
        fields = ['email']