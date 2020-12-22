from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_home_view, name='student_home'),
    path('home/', views.student_home_view, name='student_home'),
    path('dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('start_test/<int:id>', views.start_test_view, name='start_test'),
    path('upcoming_test/', views.upcoming_test_view, name='upcoming_test'),
    path('test_history/', views.test_history_view, name='test_history'),
    path('cancel/Test/<int:id>', views.cancel_test_view, name='cancel_test'),
]
