from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('school/', views.school_reg_view, name='school_reg'),
    path('student/', views.student_reg_view, name='student_reg'),
    path('teacher/', views.teacher_reg_view, name='teacher_reg'),
    path('login/', views.login_view, name='login_view'),
    path('super_login/', views.super_login_view, name='super_login_view'),
    # path('choose/School/Reg/', views.choose_reg_view, name='choose_reg'),
    # path('ATL/Reg/', views.atl_school_reg_view, name='atl_reg'),
    # path('CBSE/Reg/', views.cbse_reg_view, name='cbse_reg'),
    #
    # path('School-atl-incharge/', views.school_atl_incharge_view, name='atl_incharge'),
    # path('Vendor-Reg/', views.vendor_reg_view, name='vendor_reg'),
    # path('Lab-Reg/', views.lab_reg_view, name='lab_reg'),
    # path('Mentor-Change/', views.mentor_change_view, name='mentor_change'),
    #
    # path('Authority-Dashboard/', views.authority_dash_view, name='authority_dash'),
    #
    # path('Assessment/', views.assessment_view, name='assessment'),
    #
    # path('Logout/', views.logout_admin_view, name='logout_admin'),
    # path('ATL/login/', views.atl_login_view, name='atl_login'),
    # path('CBSE/login/', views.cbse_login_view, name='cbse_login'),

]
