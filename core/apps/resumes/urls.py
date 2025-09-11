from django.urls import path

from core.apps.resumes.views import (
    ResumeDetailView,
    ResumeListView,
    TemplateListView,
)


app_name = "resumes"

urlpatterns = [
    path('', ResumeListView.as_view(), name='resume_list'),
    path('resumes/', ResumeListView.as_view(), name='resume_list'),
    path('resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('templates/', TemplateListView.as_view(), name='template_list'),
]
