from ast import And
from urllib import request
from .models import Contributor, Project, Issue, Comment
from authentication.models import User
from .serializers import ProjectSerializer, ContributorSerializer, ContributorListSerializer, IssueSerializer, CommentSerializer, CommentListSerializer, IssueListSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor, IsContributor
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ProjectViewSet(viewsets.ViewSet):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_object(self):
        obj = get_object_or_404(Project.objects.all(), project_id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action in ['retrieve']:
            self.permission_classes = [IsAuthor | IsContributor]
        elif self.action in ['list','update', 'destroy']:
            self.permission_classes = [IsAuthor]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        projects = Project.objects.filter(author_user_id=self.request.user)
        return projects.all()

    def list(self, request,):
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request,):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author_user_id=self.request.user)
  
    def update(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        project = self.get_object()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewSet(viewsets.ViewSet):
    #serializer_class = ContributorSerializer

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [IsAuthor | IsContributor]
        elif self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()

    def list(self, request, project_pk=None):
        queryset = Contributor.objects.filter(project_id=project_pk)
        serializer = ContributorListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        serializer = ContributorSerializer(data=request.data)
        project = get_object_or_404(Project.objects.filter(project_id=project_pk))
        if serializer.is_valid():
            self.perform_create(serializer, project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer, project):
        serializer.save(project_id=project)
    
    def destroy(self, request, pk=None, project_pk=None):
        queryset = Contributor.objects.filter(user_id=pk, project_id=project_pk)
        contributor = get_object_or_404(queryset, user_id=pk)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class IssueViewset(viewsets.ViewSet):

    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [IsAuthor | IsContributor]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthor | IsContributor]
        return super().get_permissions()
    
    def list(self, request, project_pk=None):
        queryset = Issue.objects.filter(project_id=project_pk)
        serializer = IssueListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        serializer = IssueSerializer(data=request.data)
        project = get_object_or_404(Project.objects.filter(project_id=project_pk))
        if serializer.is_valid():
            self.perform_create(serializer, project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, project):
        serializer.save(project_id=project,author_user_id=self.request.user)

    def update(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(id=pk, project_id=project_pk)
        issue = get_object_or_404(queryset, id=pk)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(id=pk, project_id=project_pk)
        issue = get_object_or_404(queryset, id=pk)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve','create']:
            self.permission_classes = [ IsAuthor | IsContributor]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()

    def list(self, request, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(issue_id=issue_pk)
        serializer = CommentListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(comment_id=pk, issue_id=issue_pk)
        comment = get_object_or_404(queryset, comment_id=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request, project_pk=None, issue_pk=None):
        serializer = CommentSerializer(data=request.data)
        issue = get_object_or_404(Issue.objects.filter(pk=issue_pk))
        if serializer.is_valid():
            self.perform_create(serializer, issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, issue):
        serializer.save(issue_id=issue, author_user_id=self.request.user)
    
    def update(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(comment_id=pk, issue_id=issue_pk)
        comment = get_object_or_404(queryset, comment_id=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(comment_id=pk, issue_id=issue_pk)
        comment = get_object_or_404(queryset, comment_id=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
