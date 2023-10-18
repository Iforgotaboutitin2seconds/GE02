from django.urls import path
from . import views

from django.views.generic import ListView, DetailView
from .models import *


urlpatterns = [
    # path function defines a url pattern
    # '' is empty to represent based path to app
    # views.index is the function defined in views.py
    # name='index' parameter is to dynamically create url
    # example in html <a href="{% url 'index' %}">Home</a>.
    path('', views.index, name='index'),

    # include path to list and detail views
    path('students/', views.StudentListView.as_view(), name='students'),
    path('student/<int:pk>', views.StudentDetailView.as_view(),
         name='student-detail'),
    path('portfolio/<int:pk>', views.PortfolioDetailView.as_view(),
         name='portfolio-detail'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailVIew.as_view(),
         name='project-detail'),
    path('portfolio/<int:portfolio_id>/create_project/',
         views.createProject, name='create_project'),
path('portfolio/<int:portfolio_id>/delete_project/<int:project_id>/', views.DeleteProjectView.as_view(), name='delete_project'),
path('portfolio/<int:portfolio_id>/update_project/<int:project_id>/', views.UpdateProjectView.as_view(), name='update_project'),


]
