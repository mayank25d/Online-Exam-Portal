from django.urls import path
from . import views

urlpatterns = [
    path('', views.teach_home_view, name='teacher_home'),
    path('dashboard/', views.teach_home_view, name='teacher_home'),
    path('answer_sheet/<int:test_id>/<int:student_id>/', views.answer_sheet_view, name='answer_sheet'),
    path('manage_students/', views.manage_student_view, name='manage_student'),
    path('manage_tests/', views.manage_test_view, name='manage_test'),
    path('ajax/load_test/', views.load_test_view, name='ajax_load_test'),
    path('ajax/load_studentlist/', views.load_studentlist_view, name='ajax_load_studentlist'),
    path('select_ans_sheet/', views.select_ans_sheet_view, name='select_ans_sheet'),
    path('ajax/load-sec/', views.load_sec2_view, name='ajax_load_sec2'),
    # path('Create/Test/', views.create_test_view, name='add_test'),
    # path('Add/basic/', views.add_basic_view, name='add_basic'),
    # path('Add/Category/', views.add_category_view, name='add_category'),
    # path('Edit/Test/', views.edit_test_view, name='edit_test'),
    # path('delete/test/<int:id>', views.delete_test_view, name='delete_test'),
    # path('edit/test/<int:id>', views.edit_test_details_view, name='edit_test_details'),
    # path('add/question/', views.add_question_view, name='add_question'),
    # path('add/question/passage/', views.add_question_passage_view, name='add_passage_question'),
    #
    # path('Sample/Excel/', views.download_sample_excel_view, name='download_sample_excel'),
    # path('Upload/Excel/', views.excel_upload_view, name='excel_uploads'),
    #
    # path('delete/Question/', views.del_quest_view, name='del_quest')
]
