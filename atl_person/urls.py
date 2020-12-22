from django.urls import path
from . import views

urlpatterns = [
    path('', views.atlp_home_view, name='atlp_home'),
    path('home/', views.atlp_home_view, name='atlp_home'),
    path('school-details/', views.school_details_view, name='atl_school_details'),
    path('atl-incharge-info/', views.atl_incharge_info_view, name='atl_incharge_info'),
    path('atl-status/', views.atl_status_view, name='atl_status'),
    path('teacher-nomination/', views.teacher_nomination_view, name='teacher_nomini'),
    path('vendor-reg/', views.vendor_reg_view, name='vendor_reg'),
    path('add_component/', views.add_components, name='add_component'),
    path('lab-reg/', views.lab_reg_view, name='lab_reg'),
    path('mentor-of-change/', views.mentor_of_change_view, name='mentor_of_change'),
    path('ajax/load-component/', views.load_component_view, name='ajax_load_component'),
    path('change_password/', views.change_password_view, name='atlp_change_password'),
    path('logout/', views.logout_view, name='atlp_logout'),

]