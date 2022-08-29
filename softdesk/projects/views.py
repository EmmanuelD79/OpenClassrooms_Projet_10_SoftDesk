from .models import Contributor, Project, Issue, Comment
from authentication.models import User
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ProjectViewSet(viewsets.ViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwner]
    queryset = Project.objects.all()

    def get_project_mixin(self, project_id):
        queryset = Project.objects.filter()
        project = get_object_or_404(queryset, project_id=project_id)
        return project
    
    def get_permissions(self):
        if self.action in ['update', 'destroy', 'retreive']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated,]
        return super().get_permissions()

    def get_queryset(self):
        projects = Project.objects.filter(author_user_id=self.request.user)
        return projects.all()

    def list(self, request,):
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        project = self.get_project_mixin(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request,):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        project = self.get_project_mixin(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        project = self.get_project_mixin(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContributorViewSet(viewsets.ViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsOwner]

    def list(self, request, project_pk=None):
        queryset = Contributor.objects.filter(project_id=project_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        request.data._mutable = True
        request.data['project_id'] = project_pk
        request.data._mutable = False
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None, project_pk=None):
        queryset = Contributor.objects.filter(user_id=pk, project_id=project_pk)
        contributor = get_object_or_404(queryset, user_id=pk)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class IssueViewset(viewsets.ViewSet):

    serializer_class = IssueSerializer

    def list(self, request, project_pk=None):
        queryset = Issue.objects.filter(project_id=project_pk)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        request.data._mutable = True
        request.data['project_id'] = project_pk
        request.data._mutable = False
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(id=pk, project_id=project_pk)
        issue = get_object_or_404(queryset, id=pk)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(id=pk, project_id=project_pk)
        issue = get_object_or_404(queryset, id=pk)
        serializer = IssueSerializer(issue)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(id=pk, project_id=project_pk)
        issue = get_object_or_404(queryset, id=pk)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ViewSet):
    serializer_class = CommentSerializer

    def list(self, request, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(issue_id=issue_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(comment_id=pk, issue_id=issue_pk)
        comment = get_object_or_404(queryset, comment_id=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request, project_pk=None, issue_pk=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
