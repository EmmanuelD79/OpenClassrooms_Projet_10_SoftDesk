from rest_framework import serializers
from projects.models import Project, Contributor, Issue, Comment
from authentication.models import User
from authentication.serializers import UserSerializer
from django.shortcuts import get_object_or_404


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type']


class ContributorListSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project__id',
    }

    user_id = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['user_id', 'permission', 'role']


class ContributorSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'project_id': 'project__id',
    }

    email = serializers.EmailField(max_length=None, min_length=3, allow_blank=False, write_only=True)

    class Meta:
        model = Contributor
        fields = ['email', 'permission', 'role']

    def create(self, validated_data):
        email = validated_data.pop('email')
        project = validated_data['project_id']
        contributors = project.contributors.all()

        user = User.objects.filter(email=email)
        active_user = get_object_or_404(user)

        is_contributor = contributors.filter(user_id=active_user.user_id).exists()

        user = User.objects.filter(email=email)

        if project.author_user_id == active_user:
            raise serializers.ValidationError({'user': "User is the author"})
        elif is_contributor:
            raise serializers.ValidationError({'user': "User is already contributor"})
        validated_data['user_id'] = active_user
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
            raise serializers.ValidationError({'user': "User don't assignee"})
        validated_data['assignee_user_id'] = get_object_or_404(user)
        return Issue.objects.create(**validated_data)

    def update(self, instance, validated_data):
        assignee_user_email = validated_data.pop('assignee_user_email')
        user = User.objects.filter(email=assignee_user_email)
        if not user:
            raise serializers.ValidationError({'user': "User don't assignee"})
        validated_data['assignee_user_id'] = get_object_or_404(user)
        instance.assignee_user_id = validated_data.get('assignee_user_id', instance.assignee_user_id)
        instance.title = validated_data.get('title', instance.title)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


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
