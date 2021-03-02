from django.urls import path
from .import views

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('<slug:key>/', views.project, name='project'),
    path('<slug:key>/issues/', views.issues, name='issues'),
    path('<slug:key>/issues/<slug:issue_key>/', views.issue, name='issue'),
    path('<slug:key>/collaborators/', views.collaborators, name='collaborators'),
]