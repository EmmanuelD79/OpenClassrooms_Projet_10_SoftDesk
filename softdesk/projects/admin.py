from django.contrib import admin
from projects.models import Project, Issue, Comment, Contributor


class ProjectAdmin(admin.ModelAdmin):
    fields = ['author_user_id', 'title', 'description', 'type', 'contributors', 'created_time']
    readonly_fields = ['created_time', 'contributors']


class ContributorAdmin(admin.ModelAdmin):
    class Meta:
        model = Contributor
        fields = '__all__'


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue)
admin.site.register(Comment)
