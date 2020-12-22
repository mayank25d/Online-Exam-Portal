from django.urls import path
from . import views

urlpatterns = [
    path('', views.school_home_view, name='school_home'),
    path('dashboard/', views.school_home_view, name='school_home'),
]
