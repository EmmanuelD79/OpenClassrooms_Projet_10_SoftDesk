from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Project, Comment, Issue


class IsAuthor(permissions.BasePermission):
    '''
    Permission defining whether the logged user is the author of the project, issue or comment.
    '''

    def has_permission(self, request, view):
        if view.basename == 'projects' and view.suffix == 'List':
            return request.user.is_authenticated
        elif (view.basename == 'projects' or view.basename == 'contributors'):
            if 'project_pk' in view.kwargs:
                project = get_object_or_404(Project, project_id=view.kwargs['project_pk'])
            else:
                project = get_object_or_404(Project, project_id=view.kwargs['pk'])
            return request.user.is_authenticated and project.author_user_id == request.user
        elif view.basename == 'comments':
            if 'pk' in view.kwargs:
                comment = get_object_or_404(Comment, comment_id=view.kwargs['pk'])
                return request.user.is_authenticated and comment.author_user_id == request.user
            else:
                project = get_object_or_404(Project, project_id=view.kwargs['project_pk'])
                return request.user.is_authenticated and project.author_user_id == request.user
        elif view.basename == 'issues':
            if 'pk' in view.kwargs:
                issue = get_object_or_404(Issue, id=view.kwargs['pk'])
                print(view.kwargs, issue.author_user_id, request.user)
                return request.user.is_authenticated and issue.author_user_id == request.user
        return False

    def has_object_permission(self, request, view, obj):
        return obj.author_user_id == request.user


class IsContributor(permissions.BasePermission):
    '''
    Permission defining whether the logged user is a contributor of the project or
    the author of the project for issues and comments permissions.
    '''

    def get_list_contributors(self, request, view):

        if view.basename == 'projects' and 'pk' in view.kwargs:
            project = get_object_or_404(Project, project_id=view.kwargs['pk'])
        elif 'project_pk' in view.kwargs:
            project = get_object_or_404(Project, project_id=view.kwargs['project_pk'])
        contributors = project.contributors.all()
        is_contributor = contributors.filter(user_id=request.user.user_id).exists()
        return request.user.is_authenticated and (is_contributor or project.author_user_id == request.user)

    def has_permission(self, request, view):
        return self.get_list_contributors(request, view)

    def has_object_permission(self, request, view, obj):
        return self.get_list_contributors(request, view)
