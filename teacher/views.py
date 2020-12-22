from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from tests.models import *
from super_admin.models import *
from super_admin.forms import StudentReg
from accounts.models import Roles

from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

import xlsxwriter
import xlrd
import io
import string
import csv
import random
import pandas as pd


# Create your views here.

def teach_home_view(request):
    if request.user.is_authenticated:
        return render(request, 'teacher/dashboard.html')
    # else:
    #     return redirect('admin_login')


def load_test_view(request):
    standard = request.GET.get('standard')
    print(standard)
    standard_id = Standard.objects.get(standard_name=standard)
    print(standard_id.id)

    assigned_tests = AssignTest.objects.filter(standard=standard_id.id)
    print(assigned_tests)

    return render(request, 'teacher/test_dropdown_list.html', {'tests': assigned_tests})


def load_studentlist_view(request):
    test = request.GET.get('test')

    marksheet = MarkSheet.objects.filter(test=test)
    # print(marksheet)

    students = []
    marks = 0
    m_sheet = {}
    dic1 = {}
    for m in marksheet:
        students.append(m.student)
    students = list(set(students))
    print(students)

    for st in students:
        print(st.id)
        marksheet = MarkSheet.objects.filter(test=test, student=st)
        marks = marksheet.aggregate(Sum('marks'))
        m_sheet[st] = [marks, test]
        print(m_sheet)

    return render(request, 'teacher/studentlist.html', {'m_sheet': m_sheet})


def select_ans_sheet_view(request):
    tsss = TStdSecSub.objects.filter(teacher__user=request.user)
    assigned_tests = AssignTest.objects.filter(teacher__user=request.user).values('test_paper_id').distinct()
    print(tsss, assigned_tests)

    standard = []
    for t in tsss:
        standard.append(t.standard)
    standard = list(set(standard))
    print(standard)
    return render(request, 'teacher/select_ans_sheet.html', {'standard': standard, 'test': assigned_tests})


def answer_sheet_view(request, test_id, student_id):
    my_a = []
    marksheet = MarkSheet.objects.filter(test=test_id, student=student_id)
    test = Test.objects.get(id=test_id)

    for m in marksheet:
        my_answer = AnswerSheet.objects.filter(ques_id=m.question, marks_sheet=m)
        for ans in my_answer:
            # print(ans)
            my_a.append(ans)

        if m.question.question_tags == "Single Correct":
            valid_opt = Options.objects.get(question_id=m.question, is_valid=1)
            my_ans = AnswerSheet.objects.get(ques_id=m.question, marks_sheet=m)
            if my_ans.my_answer == valid_opt.option:
                m.marks = 1.00
                m.save()
            else:
                m.marks = 0.00
                m.save()
        if m.question.question_tags == "Multiple Correct":
            valid_opt = Options.objects.filter(question_id=m.question, is_valid=1)
            my_ans = AnswerSheet.objects.filter(ques_id=m.question, marks_sheet=m)
            mark = 0.00
            for vopt in valid_opt:
                for a in my_ans:
                    print(a.my_answer, vopt.option)
                    if a.my_answer == vopt.option:
                        mark = mark + 0.25
                    else:
                        mark = mark + 0
            print(mark, m.id)
            m.marks = mark
            m.save()
            # print(valid_opt)

    if request.method == "POST":
        for m in marksheet:
            mark = request.POST.get(str(m.id))
            if mark != None:
                m.marks = mark
                m.save()
        return redirect('select_ans_sheet')

    return render(request, 'teacher/answer_sheet.html', {'test': test, 'marksheet': marksheet, 'my_answer': my_a})


def load_sec2_view(request):
    teacher = Teacher.objects.get(user=request.user)
    std = request.GET.get('standard')
    print(std)
    sec = []

    tsss = TStdSecSub.objects.filter(teacher=teacher, standard_id=std)
    print("tsss", tsss)
    for t in tsss:
        print(t.section)
        sec.append(t.section)

    return render(request, 'teacher/section_dropdown_list.html', {'sec_nm': sec})


def manage_student_view(request):
    letters_and_digits = string.ascii_letters + string.digits
    teacher = Teacher.objects.get(user=request.user)
    tsss = TStdSecSub.objects.filter(teacher=teacher)
    school = teacher.school

    std = []
    student = []
    for t in tsss:
        std.append(t.standard)
        student.append(Student.objects.filter(school=school, standard=t.standard, section=t.section))

    fl = False
    if school == None:
        fl = True

    print(fl, school)

    if request.method == 'POST':
        if 'file_upload_stu' in request.POST:
            csv_file = request.FILES['file']
            state = request.POST.get('stustate')
            city = request.POST.get('stucity')
            standard = request.POST.get('stustd')

            try:
                data_set = csv_file.read().decode('UTF-8')
                # setup a stream which is when we loop through each line we are able to handle a data in a stream
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    stu_name = column[0]
                    random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
                    user_count = User.objects.filter(first_name__iexact=stu_name).count()
                    if user_count == 0:
                        user = User.objects.create(username=stu_name, password=random_str, first_name=stu_name,
                                                   user_type=Roles.objects.get(role_name='student'))
                    else:
                        user = User.objects.create(username=stu_name + str(user_count + 1), password=random_str,
                                                   first_name=stu_name,
                                                   user_type=Roles.objects.get(role_name='student'))

                    try:
                        _, created = Student.objects.update_or_create(
                            user=user,
                            student_name=column[0],
                            enrollment_no=column[1],
                            email=column[2],
                            phone=column[3],
                            address=column[4],
                            state=Region.objects.get(id=state),
                            city=City.objects.get(id=city),
                            school=School.objects.get(id=school),
                            teacher_assigned=Teacher.objects.get(id=teacher),
                            standard=Standard.objects.get(id=standard),
                            password=random_str,
                        )
                    except Exception as e:
                        user.delete()
                        messages.error(request,
                                       "We caught an error while uploading your file. Please check your file again.",
                                       extra_tags='error_loading_file')
                        print(e)
            except:
                messages.error(request, "Incorrect File Format. Only .csv files can be uploaded. ",
                               extra_tags="incorrect_file_format")

        if 'add_stu' in request.POST:
            random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
            form = StudentReg(request.POST)
            stu_name = request.POST.get('student_name')

            if form.is_valid():
                user_count = User.objects.filter(first_name__iexact=stu_name).count()
                print(user_count)

                if (user_count == 0):
                    user = User.objects.create_user(username=stu_name, password=random_str, first_name=stu_name,
                                                    user_type=Roles.objects.get(role_name='student'))
                else:
                    user = User.objects.create_user(username=stu_name + str(user_count + 1), password=random_str,
                                                    first_name=stu_name,
                                                    user_type=Roles.objects.get(role_name='student'))

                form = form.save(commit=False)
                form.school = school
                form.password = random_str
                form.user = user
                form.save()
        messages.success(request, 'Student Added Successfully')
        return redirect('student_manage')
    else:
        form = StudentReg()
        city = City.objects.all()
        state = Region.objects.filter(country_id=105).all()
        return render(request, 'teacher/manage_students.html', {'form': form, 'student': student, 'school': school,
                                                                'stucity': city, 'stustate': state,
                                                                'teacher': teacher, 'fl': fl, 'standard': std})


def manage_test_view(request):
    return render(request, 'teacher/manage_tests.html')

# def create_test_view(request):
#     if request.method == 'POST':
#         print('fsFDS');
#
#     if request.user.is_authenticated and request.user.user_type.role_name == 'Assessment':
#         # english_form = AddQuestionForm()
#         # hindi_form = AddQuestionForm()
#         lang = Language.objects.all()
#         stand = Standard.objects.all()
#
#         return render(request, 'assessment/add_test.html', {'lang': lang, 'stand': stand})
#     else:
#         return redirect('admin_login')
#
#
# @csrf_exempt
# def add_basic_view(request):
#     year = request.POST.get('year')
#     quater = request.POST.get('quater')
#     package = request.POST.get('package')
#     test_name = request.POST.get('test_name')
#     lang = request.POST.get('lang')
#     date = request.POST.get('date')
#     duration = request.POST.get('duration')
#     standard = request.POST.get('standard')
#     exam_no = request.POST.get('exam_no')
#     print(duration)
#
#     subject_dict = {'P1': 'Embedded', 'P2': '3D Printer', 'P3': 'Mechanical', 'P4': 'Safety Measureszzs',
#                     'nonatl': 'nonatl'}
#
#     if str(exam_no) == "1":
#         test = Test.objects.create(
#             test_year=year,
#             quater=quater,
#             subject_name=subject_dict[package],
#             test_duration=duration,
#             package=package,
#             test_date=date,
#             standard_id=standard,
#             created_by=request.user,
#             updated_by=request.user
#         )
#
#         for i in lang.split(','):
#             TestLanguage.objects.create(
#                 test=test,
#                 test_lang=i
#             )
#
#     else:
#         print(duration, 'value')
#         test = Test.objects.get(id=exam_no)
#         test.test_year = year
#         test.quater = quater
#         test.subject_name = subject_dict[package]
#         test.test_duration = duration
#         test.package = package
#         test.test_date = date
#         test.standard_id = standard
#         test.updated_by = request.user
#         test.save()
#
#         TestLanguage.objects.filter(test=test).delete()
#         for i in lang.split(','):
#             TestLanguage.objects.create(
#                 test=test,
#                 test_lang=i
#             )
#
#     return JsonResponse({'id': test.id})
#
#
# @csrf_exempt
# def add_category_view(request):
#     exam_id = request.POST.get('exam_id')
#     cat_name = request.POST.get('cat_name').split(',')
#     max_mark = request.POST.get('max_mark').split(',')
#     no_question = request.POST.get('no_question').split(',')
#     cat_id = request.POST.get('cat_id').split(',')
#
#     c_id = ''
#     print(exam_id)
#     for i in range(1, len(cat_name)):
#         if str(cat_id[i]) != '1':
#             qc = QuestionCategory.objects.get(id=cat_id[i])
#             qc.category_name = cat_name[i]
#             qc.question_to_deliver = no_question[i]
#             qc.max_score = max_mark[i]
#             qc.updated_by = request.user
#             qc.save()
#         else:
#             q = QuestionCategory.objects.create(
#                 test_id=exam_id,
#                 category_name=cat_name[i],
#                 question_to_deliver=no_question[i],
#                 max_score=max_mark[i],
#                 created_by=request.user
#             )
#             c_id += str(q.id) + ','
#
#     return JsonResponse({'cat_id': c_id})
#
#
# def edit_test_view(request):
#     test = Test.objects.all()
#     return render(request, 'assessment/edit_test.html', {'test': test})
#
#
# def delete_test_view(request, id):
#     obj = Test.objects.get(id=id)
#     obj.delete()
#     return redirect('edit_test')
#
#
# def edit_test_details_view(request, id):
#     test = Test.objects.get(id=id)
#     lang = Language.objects.all()
#     stand = Standard.objects.all()
#
#     selected_lang = TestLanguage.objects.filter(test=test).values('test_lang')
#     return render(request, 'assessment/edit_test_details.html', {'test': test, 'lang': lang, 'stand': stand,
#                                                                  'selected_lang': selected_lang})
#
#
# @csrf_exempt
# def add_question_view(request):
#     question = request.POST.get('question')
#     level = request.POST.get('level')
#     quest_type = request.POST.get('quest_type')
#     options = request.POST.get('options')
#     answer = request.POST.get('answer')
#     exam_id = request.POST.get('exam_id')
#     category = request.POST.get('category')
#     print('Exam id is', answer, options)
#     ques = Question.objects.create(
#         question_category=QuestionCategory.objects.get(test__id=exam_id, category_name=category),
#         test=Test.objects.get(id=exam_id),
#         language=Language.objects.get(lang_name='Hindi'),
#         question_title=question,
#         question_tags=quest_type,
#         level=level,
#         updated_by=request.user
#     )
#
#     o = Options.objects.filter(question=ques).delete()
#     opt = options.split(',')
#     ans = [i for i in answer.split(',')[:len(answer) - 1]]
#     print(ans)
#     for i in range(len(opt) - 1):
#         if str(i) in ans:
#             Options.objects.create(question=ques, answer=opt[i], is_valid=True)
#         else:
#             Options.objects.create(question=ques, answer=opt[i], is_valid=False)
#
#     data = dict()
#     qestions = Question.objects.filter(test__id=exam_id)
#     option = Options.objects.filter(question=qestions[0])
#     data['content'] = render_to_string('assessment/partial/partial-table.html',
#                                        {'qestions': qestions, 'option': option})
#     return JsonResponse(data)
#
#
# @csrf_exempt
# def add_question_passage_view(request):
#     question = request.POST.get('question')
#     level = request.POST.get('level')
#     quest_type = request.POST.get('quest_type')
#     exam_id = request.POST.get('exam_id')
#     category = request.POST.get('category')
#     print(category)
#     print(exam_id)
#     print(question)
#     ques = Question.objects.create(
#         question_category=QuestionCategory.objects.get(test__id=exam_id, category_name=category),
#         test=Test.objects.get(id=exam_id),
#         language=Language.objects.get(lang_name='Hindi'),
#         question_title=question,
#         question_tags=quest_type,
#         level=level,
#         updated_by=request.user
#     )
#
#     data = dict()
#     qestions = Question.objects.filter(test__id=exam_id)
#     option = Options.objects.filter(question=qestions[0])
#     data['content'] = render_to_string('assessment/partial/partial-table.html',
#                                        {'qestions': qestions, 'option': option})
#     return JsonResponse(data)
#
#
# def download_sample_excel_view(request):
#     exam_id = request.GET.get('exam_id')
#     cat = QuestionCategory.objects.filter(test_id=exam_id)
#     category = [i.category_name for i in cat]
#     output = io.BytesIO()  # Create an in-memory output file for the new workbook.
#
#     workbook = xlsxwriter.Workbook(output)  # write
#     worksheet = workbook.add_worksheet()
#     data = ['Category', 'Question Title', 'Level(Easy/Medium/Difficult)',
#             'Question Type(Single Correct/Multiple Correct)', 'Options separated with ;',
#             'Correct Answer sepatreted with;']
#     text_format = workbook.add_format({'text_wrap': True, 'valign': 'vcenter', 'bold': True})
#     row = 0
#     col = 0
#
#     for i in data:
#         worksheet.write(row, col, i, text_format)
#         col += 1
#     worksheet.data_validation(1, 2, 10000, 2, {'validate': 'list', 'source': ['Easy', 'Medium', 'Difficult']})
#     worksheet.data_validation(1, 3, 10000, 3,
#                               {'validate': 'list', 'source': ['Single Correct', 'Multiple Correct', 'Passage Based']})
#     worksheet.data_validation(1, 0, 10000, 0, {'validate': 'list', 'source': category})
#
#     workbook.close()
#
#     output.seek(0)
#     # worksheet4.filter_column('C'
#     # worksheet.data_validation(1,3,1000,3, {'validate': 'list','source': ['Easy', 'Medium', 'Difficult']})
#     filename = 'sample.xlsx'
#     response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=%s' % filename
#     return response
#
#
# @csrf_exempt
# def excel_upload_view(request):
#     exam_id = request.POST.get('exam_no')
#     excel_file = request.FILES['xlsx']
#     data = dict()
#     df = pd.read_excel(excel_file, header=0)
#     q_type = {'Single Correct': 'Single', 'Multiple Correct': 'Multiple', 'Passage Based': 'Passage'}
#
#     if len(df.values) > 0:
#         for row in df.values:
#             q = Question.objects.create(
#                 question_category=QuestionCategory.objects.get(test_id=exam_id, category_name=row[0]),
#                 test=Test.objects.get(id=exam_id),
#                 question_title=row[1],
#                 question_tags=q_type[row[3]],
#                 level=row[2],
#                 updated_by=request.user
#
#             )
#             if q.question_type in ['Single', 'Multiple']:
#                 answer = row[5].split(';')
#                 for i in row[4].split(';'):
#                     if i in answer:
#                         Options.objects.create(question=q, answer=i, is_valid=True)
#                     else:
#                         Options.objects.create(question=q, answer=i, is_valid=False)
#
#     qestions = Question.objects.filter(test_id=exam_id)
#     option = Options.objects.filter(question=qestions[0])
#     data['content'] = render_to_string('assessment/partial/partial-table.html',
#                                        {'qestions': qestions, 'option': option})
#     return JsonResponse(data)
#
#
# def del_quest_view(request):
#     id = request.GET.get('id')
#     exam_id = request.GET.get('exam_id')
#
#     Question.objects.filter(id=id).delete()
#     data = dict()
#     qestions = Question.objects.filter(test__id=exam_id)
#     if (qestions.count() == 0):
#         option = {}
#     else:
#         option = Options.objects.filter(question=qestions[0])
#     data['content'] = render_to_string('assessment/partial/partial-table.html',
#                                        {'qestions': qestions, 'option': option})
#     return JsonResponse(data)
