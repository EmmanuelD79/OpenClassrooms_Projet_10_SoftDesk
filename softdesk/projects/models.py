from django.db import models
from django.conf import settings

from authentication.models import User


class Project(models.Model):
    '''Project Model with attribut:
        - project_id
        - author_user_id (ForeignKey)
        - title
        - description
        - type (choices : 'back-end', 'front-end', 'iOS' or 'Android')
        - created_time
        - contributors (Many-to-many relation with User Model through Contributor Model)
    '''

    BACK_END = 'back-end'
    FRONT_END = 'front-end'
    IOS = 'iOS'
    ANDROID = 'Android'

    TYPE_CHOICES = (
        (BACK_END, 'back-end'),
        (FRONT_END, 'front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),

    )
    project_id = models.BigAutoField(primary_key=True)
    author_user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='author_project')
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=8192, blank=False)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name='Type')
    created_time = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(User, through="Contributor")

    def __str__(self):
        return f"{self.project_id} - {self.title} "


class Issue(models.Model):
    '''Issue Model with attribut:
        - title
        - desc
        - tag (choices : 'BUG', 'IMPROVEMENT' or 'TASK')
        - priority (choices : 'HIGH', 'MEDIUM' or 'LOW')
        - project_id (ForeignKey)
        - status (choices : 'TO DO', 'IN PROGRESS' or 'DONE')
        - author_user_id (ForeignKey)
        - assignee_user_id (ForeignKey)
        - created_time
    '''

    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

    PRIORITY_CHOICES = (
        (HIGH, 'ÉLEVÉE'),
        (MEDIUM, 'MOYENNE'),
        (LOW, 'FAIBLE'),
    )

    BUG = 'BUG'
    IMPROVEMENT = 'IMPROVEMENT'
    TASK = 'TASK'

    TAG_CHOICES = (
        (BUG, 'BUG'),
        (IMPROVEMENT, 'AMÉLIORATION'),
        (TASK, 'TÂCHE'),
    )

    TO_DO = 'TO DO'
    IN_PROGRESS = 'IN PROGRESS'
    DONE = 'DONE'

    STATUS_CHOICES = (
        (TO_DO, 'À faire'),
        (IN_PROGRESS, 'En cours'),
        (DONE, 'Terminé'),
    )

    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=8192)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, verbose_name='Tag')
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, verbose_name='Priority')
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='project')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name='Status')
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_id')
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignee_id')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    '''Comment Model with attribut:
        - comment_id
        - description
        - author_user_id (ForeignKey)
        - issue_id (ForeignKey)
        - created_time
    '''

    comment_id = models.BigAutoField(primary_key=True)
    description = models.TextField(max_length=8192, blank=False)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    '''Contributor Model (through table) with attribut:
        - user_id (ForeignKey)
        - project_id (ForeignKey)
        - permission
        - role
    '''

    user_id = models.ForeignKey(to=User, related_name='contributor_user', on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, related_name='contributor_project', on_delete=models.CASCADE)
    permission = models.CharField(max_length=128, blank=False)
    role = models.CharField(max_length=128, blank=False)

    class Meta:
        unique_together = ('user_id', 'project_id')

    def __str__(self):
        return f"{self.user_id} - {self.project_id} "
