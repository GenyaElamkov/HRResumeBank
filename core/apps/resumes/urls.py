from django.urls import path

from core.apps.resumes.views import (
    ResumeListView,
    TemplateListView,
)


app_name = "resumes"

urlpatterns = [
    path('', ResumeListView.as_view(), name='resume_list'),
    path('resumes/', ResumeListView.as_view(), name='resume_list'),
    path('templates/', TemplateListView.as_view(), name='template_list'),
]
