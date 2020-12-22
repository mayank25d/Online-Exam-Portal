import sys
import string
import random
import io
import csv

sys.path.append("..")

from django.shortcuts import render, redirect
from accounts.models import Roles
from django.contrib.auth import get_user_model, logout
from django.db.models import Count, Q

User = get_user_model()

from .forms import *
from atl_person.forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from tests.models import *
from .models import *
from collections import Counter

letters_and_digits = string.ascii_letters + string.digits


def admin_login_view(request):
    return render(request, 'super_admin/login.html')


def admin_logout_view(request):
    logout(request)
    return render(request, 'super_admin/login.html')


@login_required
def admin_index_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        stu = Student.objects.all()
        t = Teacher.objects.all()
        tfreelancer = Teacher.objects.filter(school__isnull=True)
        sch = School.objects.all()
        auth = User.objects.filter(user_type=2)

        sch_dic = {}
        tea_dic = {}

        chart_val = {'stjoin': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'scjoin': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     'tfjoin': [0, 0, 0, 0, 0, 0]}

        # stu_joined = stu.values_list('created_at', flat=True)
        # sch_joined = sch.values_list('created_at', flat=True)

        today = datetime.today()
        this_year = today.year
        this_month = today.month

        # number of students joined per month
        for i in range(1, 13):
            for st_id in stu:
                if st_id.user.created_at.year == this_year:
                    if st_id.user.created_at.month == i:
                        chart_val['stjoin'][i - 1] += 1

        # number of schools joined per month
        for i in range(1, 13):
            for sch_id in sch:
                if sch_id.user.created_at.year == this_year:
                    if sch_id.user.created_at.month == i:
                        chart_val['scjoin'][i - 1] += 1

        # number of freelancing teachers joined per month
        for i in range(1, 13):
            for tf_id in tfreelancer:
                if tf_id.user.created_at.year == this_year:
                    if tf_id.user.created_at.month == i:
                        if this_month > 6 and i > 6:
                            chart_val['tfjoin'][i - 7] += 1
                        if this_month < 6 and i < 6:
                            chart_val['tfjoin'][i - 1] += 1
        print(chart_val['tfjoin'])

        # top 5 schools on the basis of maximum students
        sch_stu = School.objects.annotate(nstudents=Count('student_school'))
        for schl in sch_stu:
            sch_dic[schl] = schl.nstudents
        sch_dic = Counter(sch_dic).most_common(5)
        print(sch_dic)

        # top 5 freelancer teachers on the basis of maximum students
        tea_stu = Teacher.objects.filter(school=None).annotate(nstu=Count('student_ft'))
        for tea in tea_stu:
            tea_dic[tea] = tea.nstu
        tea_dic = Counter(tea_dic).most_common(5)
        print(tea_dic)

        user = request.user
        print(user.first_name)
        return render(request, 'super_admin/dashboard.html', {'total_stu': stu, 'total_t': t,
                                                              'total_sch': sch, 'total_auth': auth,
                                                              'user': user, 'data': chart_val, 'year': this_year,
                                                              'top_5_school': sch_dic, 'top_5_teacher': tea_dic})

    else:
        return redirect('admin_login')


def all_student_view(request, pk):
    standard = Standard.objects.all()
    student = Student.objects.all()
    print(pk)

    if request.method == "POST":
        std = request.POST.get('mystandard')
        stu = Student.objects.filter(standard=std, school=pk)

        return render(request, 'super_admin/all_student.html', {'student': stu, 'standard': standard})

    return render(request, 'super_admin/all_student.html', {'student': student, 'standard': standard})


def student_details_view(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentReg(instance=student)
    print(pk)

    return render(request, 'super_admin/student_dashboard.html', {'form': form, 'student': student})


def all_school_view(request):
    school = School.objects.all()
    city = City.objects.all()
    state = Region.objects.filter(country_id=105).all()
    board = AffiliationType.objects.all()

    if request.method == "POST":
        mystate = request.POST.get('mystate')
        mycity = request.POST.get('mycity')
        myboard = request.POST.get('myboard')

        school = School.objects.filter(state=mystate, city=mycity, school_board=myboard)

        return render(request, 'super_admin/all_school.html', {'school': school, 'city': city, 'state': state,
                                                               'board': board})

    return render(request, 'super_admin/all_school.html', {'school': school, 'city': city, 'state': state,
                                                           'board': board})


def school_details_view(request, pk):
    school = School.objects.get(id=pk)
    stu = Student.objects.filter(school=school)
    teacher = Teacher.objects.filter(school=school)
    test = AssignTest.objects.filter(school=school)
    form = SchoolReg(instance=school)

    tsss = TStdSecSub.objects.filter(school=school, teacher__isnull=True)
    standard = Standard.objects.all()
    section = Section.objects.filter(school=school)
    if not school.atl:
        package = Package.objects.filter(id=5)
        subject = Subjects.objects.filter(atl=0)
    else:
        package = Package.objects.all()
        subject = Subjects.objects.all()
        for sub in subject:
            if sub.atl == 1 and not tsss:
                new_subj = TStdSecSub.objects.create(package=sub.package, standard=sub.standard, subject=sub,
                                                     school_id=pk)
                new_subj.save()

    # count of total assessments created by the school
    assessment = teacher.values_list('assessment_created', flat=True)

    # count of total questions created by the school
    ques_count = 0
    for t in teacher:
        ques_count += Question.objects.filter(created_by=t.user.id).count()

    if request.method == "POST":
        if "edit_school" in request.POST:
            form = SchoolReg(request.POST, instance=school)
            form.save()
            return HttpResponseRedirect(reverse('school_details', args=(pk,)))

        if 'add_subject' in request.POST:
            std = request.POST.get("mystd1")
            pack = request.POST.get("mypack1")
            sub = request.POST.get("mysub1")
            new_sub = TStdSecSub.objects.create(standard_id=std, package_id=pack, subject_id=sub, school_id=pk)
            new_sub.save()
            return HttpResponseRedirect(reverse('school_details', args=(pk,)))

        if 'add_section' in request.POST:
            std = request.POST.get("mystd")
            sec = request.POST.get("mysec")
            new_sec = Section.objects.create(section_name=sec, school=school, standard_id=std)
            new_sec.save()
            return HttpResponseRedirect(reverse('school_details', args=(pk,)))

    return render(request, 'super_admin/school_dashboard.html', {'school': school, 'stu': stu, 'teacher': teacher,
                                                                 'a_count': sum(assessment), 'q_count': ques_count,
                                                                 'form': form, 'subject': subject, 'section': section,
                                                                 'standard': standard, 'package': package,
                                                                 'tsss': tsss})

    # # student report_card
    # for s in stu:
    #     if s.standard.id == 1:
    #         print(s.standard.id)
    #         report1 = ReportCard.objects.filter(student=s)
    #         print(report1)
    #     if s.standard.id == 2:
    #         print(s.standard.id)
    #         report2 = ReportCard.objects.filter(student=s)
    #         print(report2)

    # performance of children in a quarter, standard wise
    # q1 = {'P1': [0, 0, 0, 0, 0, 0, 0], 'P2': [0, 0, 0, 0, 0, 0, 0], 'P3': [0, 0, 0, 0, 0, 0, 0],
    #       'P4': [0, 0, 0, 0, 0, 0, 0]}
    # q2 = {'P1': [0, 0, 0, 0, 0, 0, 0], 'P2': [0, 0, 0, 0, 0, 0, 0], 'P3': [0, 0, 0, 0, 0, 0, 0],
    #       'P4': [0, 0, 0, 0, 0, 0, 0]}
    # q3 = {'P1': [0, 0, 0, 0, 0, 0, 0], 'P2': [0, 0, 0, 0, 0, 0, 0], 'P3': [0, 0, 0, 0, 0, 0, 0],
    #       'P4': [0, 0, 0, 0, 0, 0, 0]}
    # q4 = {'P1': [0, 0, 0, 0, 0, 0, 0], 'P2': [0, 0, 0, 0, 0, 0, 0], 'P3': [0, 0, 0, 0, 0, 0, 0],
    #       'P4': [0, 0, 0, 0, 0, 0, 0]}
    #
    # for s in stu:
    #     print(s)
    #     test_s = AssignTest.objects.filter(student=s)
    #     print(test_s)
    #     for t in test_s:
    #         subject = t.test_paper.sub_name
    #         package = t.test_paper.package
    #         quarter = t.test_paper.quarter
    #         marksheet = MarkSheet.objects.filter(test=t.test_paper.id, student=s.user.id)
    #         marks = marksheet.aggregate(Sum('marks'))
    #         print(subject, marks['marks__sum'], package, quarter)
    # for m in marks:
    #     if t.test_paper.quarter.id == 1:
    #         q1[t.test_paper.package] = []


def all_tfreelancer_view(request):
    tf = Teacher.objects.filter(school=None)
    city = City.objects.all()
    state = Region.objects.filter(country_id=105).all()

    if request.method == "POST":
        mystate = request.POST.get('mystate')
        mycity = request.POST.get('mycity')

        tf = Teacher.objects.filter(state=mystate, city=mycity, school=None)

        return render(request, 'super_admin/all_tf.html', {'tfreelancer': tf, 'city': city, 'state': state})

    return render(request, 'super_admin/all_tf.html', {'tfreelancer': tf, 'city': city, 'state': state})


def teacher_details_view(request, pk):
    print(pk)
    teacher = Teacher.objects.get(id=pk)
    tsss = TStdSecSub.objects.filter(teacher_id=pk)
    form = TeacherReg(instance=teacher)
    standard = Standard.objects.all()

    if teacher.school_id != None:
        school = School.objects.get(id=teacher.school_id)
        section = Section.objects.filter(school=school)
        if not school.atl:
            package = Package.objects.filter(id=5)
        else:
            package = Package.objects.all()
    else:
        section = Section.objects.filter(school__isnull=True)
        package = Package.objects.filter(id=5)

    subject = Subjects.objects.all()

    if request.method == "POST":
        if 'edit_teacher' in request.POST:
            form = TeacherReg(request.POST, instance=teacher)
            form.save()
            return HttpResponseRedirect(reverse('teacher_details', args=(pk,)))
        if 'add_subject_T' in request.POST:
            std = request.POST.get('mystd')
            sec = request.POST.get('mysec')
            pack = request.POST.get('mypack')
            sub = request.POST.get('mysub')
            new_tsss = TStdSecSub.objects.create(section_id=sec, standard_id=std, package_id=pack, teacher_id=pk,
                                                 subject_id=sub, school=school)
            new_tsss.save()
            return HttpResponseRedirect(reverse('teacher_details', args=(pk,)))

    return render(request, 'super_admin/teacher_dashboard.html', {'form': form, 'teacher': teacher, 'tsss': tsss,
                                                                  'standard': standard, 'section': section,
                                                                  'subject': subject, 'package': package})


def load_tsss_view(request):
    std = request.GET.get('std')
    school = request.GET.get('school')
    pack = request.GET.get('pack')
    tsss = TStdSecSub.objects.filter(school_id=school, package_id=pack, teacher__isnull=True)
    print(tsss, std, school, pack)
    return render(request, 'super_admin/tsss_dropdown_list.html', {'tsss_nm': tsss})


def load_sec_view(request):
    std = request.GET.get('standard')
    school = request.GET.get('school')
    print(std, school)
    sec = Section.objects.filter(school_id=school, standard_id=std)
    if not sec:
        sec = Section.objects.filter(school__isnull=True, standard__isnull=True)
    return render(request, 'super_admin/section_dropdown_list.html', {'sec_nm': sec})


@login_required
def change_password_view(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        return redirect('admin_login')
    return render(request, 'super_admin/change_password.html', {'form': form})


def delete_teacher_view(request, pk):
    teacher = Teacher.objects.get(id=pk)
    teacher.delete()
    return redirect("teacher_manage")


def delete_school_view(request, pk):
    school = School.objects.get(id=pk)
    school.delete()
    return redirect("school_manage")


def delete_student_view(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    return redirect("student_manage")


def delete_authority_view(request, pk):
    auth = AuthorityAccount.objects.get(id=pk)
    auth.delete()
    return redirect("authority_manage")


def delete_section_view(request, pk):
    sec = Section.objects.get(id=pk)
    school_id = sec.school_id
    sec.delete()
    return HttpResponseRedirect(reverse('school_details', args=(school_id,)))


def delete_tsss_view(request, pk):
    tsss = TStdSecSub.objects.get(id=pk)
    teacher_id = tsss.teacher_id
    tsss.delete()
    return HttpResponseRedirect(reverse('teacher_details', args=(teacher_id,)))


def delete_atlp_view(request, pk):
    atlp = ATLPerson.objects.get(id=pk)
    atlp.delete()
    return redirect("atl_person")


def delete_test_view(request, pk):
    test = Test.objects.get(id=pk)
    test.delete()
    return redirect("create_test")


@user_passes_test(lambda u: u.is_superuser)
def add_staff_view(request):
    # letters_and_digits = string.ascii_letters + string.digits
    super_admin = User.objects.filter(is_staff=True, is_superuser=True)

    if request.method == 'POST':
        # random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email_id = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        user_count = User.objects.filter(email=email_id, is_staff=True).count()
        if user_count == 0:
            if password2 == password:
                user = User.objects.create(username=username, first_name=first_name, last_name=last_name,
                                           email=email_id,
                                           user_type=Roles.objects.get(role_name='super_admin'), is_staff=True,
                                           is_superuser=True)
                user.set_password(password)
                user.save()

                messages.success(request, 'User Added Successfully', extra_tags='add_staff')
            else:

                messages.error(request, "Password fields should match", extra_tags='add_staff')
                print(messages)

            return redirect('add_staff')
        else:
            print("User already exist with this email")
            messages.warning(request, 'User already exist with this email', extra_tags='add_staff')

    return render(request, 'super_admin/add_staff.html', {'super_admin': super_admin})


def boards_packages_view(request):
    packages = Package.objects.all()
    boards = AffiliationType.objects.all()

    if request.method == 'POST':
        package_form = Packages(request.POST)
        board_form = SchoolBoard(request.POST)

        if package_form.is_valid():
            print(package_form.is_valid())
            package_form = package_form.save(commit=False)
            package_form.save()
            messages.success(request, "New ATL Package Added", extra_tags='new_pNb')

        if board_form.is_valid():
            print(board_form.is_valid())
            board_form = board_form.save(commit=False)
            board_form.save()
            messages.success(request, "New School Board Added", extra_tags='new_pNb')
        return redirect('boards_packages')

    else:
        package_form = Packages()
        board_form = SchoolBoard()
        return render(request, 'super_admin/boards_packages.html',
                      {'packageform': package_form, 'boardform': board_form, 'packages': packages, 'boards': boards})


def load_city_view(request):
    state_id = request.GET.get('state')
    city = City.objects.filter(region_id=state_id)  # .values_list('slug', flat=True)
    return render(request, 'super_admin/city_dropdown_list.html', {'city_nm': city})


@user_passes_test(lambda u: u.is_superuser)
def school_manage_view(request):
    letters_and_digits = string.ascii_letters + string.digits

    if request.method == 'POST':
        if 'file_upload' in request.POST:
            state = request.POST.get('mystate')
            city = request.POST.get('mycity')
            board = request.POST.get('myboard')
            # print("state. city and board", state, city, board)
            csv_file = request.FILES['file']
            # print(csv_file)

            try:
                data_set = csv_file.read().decode('UTF-8')
                # setup a stream which is when we loop through each line we are able to handle a data in a stream
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    sch_name = column[0]
                    random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
                    user_count = User.objects.filter(first_name__iexact=sch_name).count()
                    if user_count == 0:
                        user = User.objects.create(username=sch_name, password=random_str, first_name=sch_name,
                                                   user_type=Roles.objects.get(role_name='school'))
                    else:
                        user = User.objects.create(username=sch_name + str(user_count + 1), password=random_str,
                                                   first_name=sch_name, user_type=Roles.objects.get(role_name='school'))

                    try:
                        _, created = School.objects.update_or_create(
                            user=user,
                            school_name=column[0],
                            password=random_str,
                            email=column[1],
                            address=column[2],
                            state=Region.objects.get(id=state),
                            city=City.objects.get(id=city),
                            phone=column[3],
                            school_board=AffiliationType.objects.get(id=board),
                            incharge_name=column[4],
                            incharge_email=column[5],
                            atl=column[6],
                        )
                    except Exception as e:
                        user.delete()
                        messages.error(request,
                                       "We caught an error while uploading your file. Please check your file again.",
                                       extra_tags='error_loading_file')
                        print(e)
            except:
                messages.error(request, "Incorrect File Format", extra_tags="incorrect_file_format")

        if 'add_school' in request.POST:
            form = SchoolReg(request.POST)
            sc_name = request.POST['school_name']
            random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
            atl = request.POST.get('atl')
            print(atl)

            if form.is_valid():
                user_count = User.objects.filter(first_name__iexact=sc_name).count()
                if user_count == 0:
                    user = User.objects.create(username=sc_name, password=random_str, first_name=sc_name,
                                               user_type=Roles.objects.get(role_name='school'))
                else:
                    user = User.objects.create(username=sc_name + str(user_count + 1), password=random_str,
                                               first_name=sc_name, user_type=Roles.objects.get(role_name='school'))

                form = form.save(commit=False)
                form.password = random_str
                form.user = user
                form.save()
        messages.success(request, 'School Added Successfully')
        return redirect('school_manage')
    else:
        form = SchoolReg()
        school = School.objects.all()
        city = City.objects.all()
        state = Region.objects.filter(country_id=105).all()
        board = AffiliationType.objects.all()
        return render(request, 'super_admin/manage_school.html', {'form': form, 'school': school, 'mycity': city,
                                                                  'mystate': state, 'board': board})


def load_teachers_view(request):
    city_id = request.GET.get('city')
    school_id = request.GET.get('school')
    if school_id == None:
        teachers = Teacher.objects.filter(city_id=city_id, school__isnull=True)
    else:
        teachers = Teacher.objects.filter(city_id=city_id, school_id=school_id)
    return render(request, 'super_admin/teachers_dropdown_list.html', {'teachers_nm': teachers})


@user_passes_test(lambda u: u.is_superuser)
def add_student_view(request):
    letters_and_digits = string.ascii_letters + string.digits

    if request.method == 'POST':
        if 'file_upload_stu' in request.POST:
            csv_file = request.FILES['file']
            state = request.POST.get('stustate')
            city = request.POST.get('stucity')
            school = request.POST.get('stuschool')
            teacher = request.POST.get('stuteacher')
            standard = request.POST.get('stustandard')

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
                                                   first_name=stu_name, user_type=Roles.objects.get(role_name='student'))

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
                messages.error(request, "Incorrect File Format. Only .csv files can be uploaded. ", extra_tags="incorrect_file_format")


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
                form.password = random_str
                form.user = user
                form.save()
        messages.success(request, 'Student Added Successfully')
        return redirect('student_manage')
    else:
        form = StudentReg()
        school = School.objects.all()
        city = City.objects.all()
        state = Region.objects.filter(country_id=105).all()
        student = Student.objects.all()
        teacher = Teacher.objects.all()
        standard = Standard.objects.all()
        return render(request, 'super_admin/manage_students.html', {'form': form, 'student': student, 'school': school,
                                                                    'stucity': city, 'stustate': state,
                                                                    'teacher': teacher,
                                                                    'standard': standard})


def load_school_view(request):
    city = request.GET.get('city')
    school = School.objects.filter(city=city)

    return render(request, 'super_admin/school_dropdown_list.html', {'school_list': school})


def load_subject_view(request):
    sch = request.GET.get('school')
    school = School.objects.get(id=sch)
    # print(school.atl)
    if school.atl == False:
        print(school.atl)
        subject = Subjects.objects.filter(atl=False)
    else:
        subject = Subjects.objects.all()

    return render(request, 'super_admin/subject_dropdown_list.html', {'subject_list': subject})


@user_passes_test(lambda u: u.is_superuser)
def add_teacher_view(request):
    letters_and_digits = string.ascii_letters + string.digits

    if request.method == 'POST':
        if "file_upload_T" in request.POST:
            state = request.POST.get('mystate')
            city = request.POST.get('mycity')
            school = request.POST.get('myschool')
            if school == '':
                school_obj = None
            else:
                school_obj = School.obejcts.get(id=school)
            # print("state. city and board", state, city, board)
            csv_file = request.FILES['file']
            # print(csv_file)

            try:
                data_set = csv_file.read().decode('UTF-8')
                # setup a stream which is when we loop through each line we are able to handle a data in a stream
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    teac_name = column[0]
                    random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
                    user_count = User.objects.filter(first_name__iexact=teac_name).count()
                    if user_count == 0:
                        user = User.objects.create(username=teac_name, password=random_str, first_name=teac_name,
                                                   user_type=Roles.objects.get(role_name='teacher'))
                    else:
                        user = User.objects.create(username=teac_name + str(user_count + 1), password=random_str,
                                                   first_name=teac_name, user_type=Roles.objects.get(role_name='teacher'))

                    try:
                        _, created = Teacher.objects.update_or_create(
                            user=user,
                            teacher_name=column[0],
                            email=column[1],
                            phone=column[2],
                            address=column[3],
                            enrollment_no=column[4],
                            password=random_str,
                            state=Region.objects.get(id=state),
                            city=City.objects.get(id=city),
                            school=school_obj,
                        )
                    except Exception as e:
                        user.delete()
                        messages.error(request,
                                       "We caught an error while uploading your file. Please check your file again.",
                                       extra_tags='error_loading_file')
                        print(e)
            except:
                messages.error(request, "Incorrect File Format. Only .csv files can be uploaded.", extra_tags="incorrect_file_format")

        if 'add_teacher' in request.POST:
            random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
            form = TeacherReg(request.POST)
            teac_name = request.POST.get('teacher_name')
            # print(teac_name)

            if form.is_valid():
                user_count = User.objects.filter(first_name__iexact=teac_name).count()

                if (user_count == 0):
                    user = User.objects.create_user(username=teac_name, password=random_str, first_name=teac_name,
                                                    user_type=Roles.objects.get(role_name='teacher'))
                else:
                    user = User.objects.create_user(username=teac_name + str(user_count + 1), password=random_str,
                                                    first_name=teac_name,
                                                    user_type=Roles.objects.get(role_name='teacher'))

                form = form.save(commit=False)
                form.password = random_str
                form.user = user
                form.save()
        messages.success(request, 'Teacher Added Successfully')
        return redirect('teacher_manage')
    else:
        form = TeacherReg()
        teacher = Teacher.objects.all()
        state = Region.objects.filter(country_id=105).all()
        return render(request, 'super_admin/manage_teachers.html', {'form': form, 'teacher': teacher, 'state': state})


@user_passes_test(lambda u: u.is_superuser)
def add_auth_view(request):
    letters_and_digits = string.ascii_letters + string.digits

    if request.method == 'POST':
        random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
        form = AuthorityReg(request.POST)
        auth_name = request.POST.get('authority_name')
        # print(auth_name)

        if form.is_valid():
            user_count = User.objects.filter(first_name__iexact=auth_name).count()

            if (user_count == 0):
                user = User.objects.create_user(username=auth_name, password=random_str, first_name=auth_name,
                                                user_type=Roles.objects.get(role_name='teacher'))
            else:
                user = User.objects.create_user(username=auth_name + str(user_count + 1), password=random_str,
                                                first_name=auth_name,
                                                user_type=Roles.objects.get(role_name='authority'))

            form = form.save(commit=False)
            form.password = random_str
            form.user = user
            form.save()
            messages.success(request, 'Authority Added Successfully')
            return redirect('authority_manage')
        else:
            print("invalid")
            return render(request, 'super_admin/manage_authority.html', {'form': form})
    else:
        form = AuthorityReg()
        authority = AuthorityAccount.objects.all()
        return render(request, 'super_admin/manage_authority.html', {'form': form, 'authority': authority})


def atlp_details_view(request, pk):
    atlp = ATLPerson.objects.get(id=pk)
    school_details = SchoolDetails.objects.get(filled_by_id=pk)
    form1 = SchoolDetailsFill(instance=school_details)
    form2 = ATLInchargeInfo(instance=atlp)
    form3 = ATLStatusFill(instance=atlp)
    form4 = TeacherNominationFill(instance=atlp)
    return render(request, 'super_admin/atl_person_dashboard.html', {'pk': pk, 'form1': form1, 'form2': form2,
                                                                     'form3': form3, 'form4': form4})


def vendor_data_view(request, pk):
    atlp = ATLPerson.objects.get(id=pk)
    vendor = VendorRegistration.objects.get(filled_by_id=pk)
    form = VendorReg(instance=vendor)
    return render(request, 'super_admin/vendor_data.html', {'pk': pk, 'form': form})


def lab_reg_data_view(request, pk):
    atlp = ATLPerson.objects.get(id=pk)
    lab = LabPackageReg.objects.get(filled_by_id=pk)
    form = LabReg(instance=lab)
    return render(request, 'super_admin/lab_reg_data.html', {'pk': pk, 'form': form})


def mentor_data_view(request, pk):
    atlp = ATLPerson.objects.get(id=pk)
    mentor = MentorOfChange.objects.get(filled_by_id=pk)
    form = MOCReg(instance=mentor)
    return render(request, 'super_admin/mentor_data.html', {'pk': pk, 'form': form})


def add_atl_person(request):
    letters_and_digits = string.ascii_letters + string.digits

    if request.method == 'POST':
        random_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
        form = ATLPersonReg(request.POST)
        atlp_name = request.POST.get('name')
        # print(atlp_name)

        if form.is_valid():
            user_count = User.objects.filter(first_name__iexact=atlp_name).count()

            if (user_count == 0):
                user = User.objects.create_user(username=atlp_name, password=random_str, first_name=atlp_name,
                                                user_type=Roles.objects.get(role_name='atl_person'))
                user.set_password(random_str)
                user.save()
            else:
                user = User.objects.create_user(username=atlp_name + str(user_count + 1), password=random_str,
                                                first_name=atlp_name,
                                                user_type=Roles.objects.get(role_name='authority'))
                user.set_password(random_str)
                user.save()

            form = form.save(commit=False)
            form.password = random_str
            form.user = user
            form.save()
            messages.success(request, 'Authority Added Successfully')
            return redirect('atl_person')
        else:
            print("invalid")
            return render(request, 'super_admin/atl_person.html', {'form': form})
    else:
        form = ATLPersonReg()
        atl_person = ATLPerson.objects.all()
        return render(request, 'super_admin/atl_person.html', {'form': form, 'atlp': atl_person})


def load_sub_view(request):
    affiliation = int(request.GET.get('affiliation'))
    if affiliation == 1:
        package = Package.objects.all()[:4]
    else:
        package = Package.objects.all()[4:5]
        # print(package)
    return render(request, 'super_admin/package_dropdown_list.html', {'package': package})


def add_sub_view(request):
    if request.method == 'POST':
        form = CreateSubject(request.POST)

        if form.is_valid():
            atl = request.POST.get('atl')
            # print(atl)
            form = form.save(commit=False)
            if atl == 'on':
                form.atl = True
            else:
                form.atl = False
            form.save()
            messages.success(request, 'Subject Added Successfully')
            return redirect('add_sub')
        else:
            return render(request, 'super_admin/test_sub.html', {'form': form})
    else:
        form = CreateSubject()
        test_sub = Subjects.objects.all()
        return render(request, 'super_admin/test_sub.html', {'form': form, 'test_sub': test_sub})


def load_topic_view(request):
    package_id = request.GET.get('package')
    standard_id = request.GET.get('standard')
    # print(package_id)
    if package_id is '5':
        sub_name = Subjects.objects.filter(package__isnull=True).filter(standard_id=int(standard_id))
    else:
        sub_name = Subjects.objects.filter(package_id=int(package_id))
    return render(request, 'super_admin/sub_dropdown_list.html', {'sub_name': sub_name})


def add_topic_view(request):
    if request.method == 'POST':
        form = CreateTopic(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Topic Added Successfully')
            return redirect('test_topic')
        else:
            return render(request, 'super_admin/test_topic.html', {'form': form})

    else:
        test_topic = TestTopic.objects.all()
        form = CreateTopic()
        return render(request, 'super_admin/test_topic.html', {'form': form, 'test_topic': test_topic})


def load_que_view(request):
    package_id = request.GET.get('package')
    standard_id = request.GET.get('standard')
    subject_id = request.GET.get('sub_name')

    topic = TestTopic.objects.filter(sub_name_id=int(subject_id)).filter(package_id=int(package_id)).filter(
        standard_id=int(standard_id))

    return render(request, 'super_admin/topic_dropdown_list.html', {'topic': topic})


def save_opt_view(request):
    option1 = request.GET.get('option1')
    option2 = request.GET.get('option2')
    option3 = request.GET.get('option3')
    option4 = request.GET.get('option4')
    valid1 = request.GET.get('is_valid1')
    valid2 = request.GET.get('is_valid2')
    valid3 = request.GET.get('is_valid3')
    valid4 = request.GET.get('is_valid4')
    ques = request.GET.get('question')

    # print(ques)

    question = Question.objects.get(question=ques)
    # print(question.id)

    if question.question_tags == "Passage Based":
        opt1 = Options.objects.create(option=option1, is_valid=valid1, question_id_id=question.id)
        opt1.save()
    else:
        opt1 = Options.objects.create(option=option1, is_valid=valid1, question_id_id=question.id)
        opt1.save()
        opt2 = Options.objects.create(option=option2, is_valid=valid2, question_id_id=question.id)
        opt2.save()
        opt3 = Options.objects.create(option=option3, is_valid=valid3, question_id_id=question.id)
        opt3.save()
        opt4 = Options.objects.create(option=option4, is_valid=valid4, question_id_id=question.id)
        opt4.save()

    return redirect('add_question')


def atl_pack_view(request):
    atl = request.GET.get('atl')
    if atl == 'true':
        package = Package.objects.exclude(package="None")
    else:
        package = Package.objects.filter(package="None")

    return render(request, 'super_admin/package_dropdown_list.html', {'package': package})


def atl_que_view(request):
    atl = request.GET.get('atl')
    if atl == 'true':
        que_tags = ['Single Correct', 'Multiple Correct']
    else:
        que_tags = ['Single Correct', 'Multiple Correct', 'Passage Based']

    return render(request, 'super_admin/que_tags_dropdown.html', {'que_tags': que_tags})



def add_question_view(request):
    if request.method == 'POST':
        user = request.user
        form_que = CreateQuestion(request.POST)
        form_opt1 = CreateOptions(request.POST or None, prefix="option1")
        form_opt2 = CreateOptions(request.POST, prefix="option2")
        form_opt3 = CreateOptions(request.POST, prefix="option3")
        form_opt4 = CreateOptions(request.POST, prefix="option4")

        if 'file_upload_que' in request.POST:
            package_id = request.POST.get('package')
            standard_id = request.POST.get('standard')
            sub_name_id = request.POST.get('sub_name')
            topic_id = request.POST.get('topic')
            # print(package_id, standard_id, sub_name_id, topic_id)

            csv_file = request.FILES['file']
            # print(csv_file)

            if not csv_file.name.endswith('.csv'):
                messages.error(request, "This is not a csv file")

            data_set = csv_file.read().decode('UTF-8')
            # setup a stream which is when we loop through each line we are able to handle a data in a stream
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                valid_opt = [column[2], column[4], column[6], column[8]]
                # print(valid_opt.count('1'))

                if valid_opt.count('1') > 1:
                    que_tag = 'Multiple Correct'
                elif valid_opt.count('1') == 1:
                    que_tag = 'Single Correct'
                else:
                    que_tag = 'Passage Based'

                question = Question.objects.create(question=column[0], created_by=user, topic_id=topic_id,
                                                   package_id=package_id,
                                                   sub_name_id=sub_name_id, standard_id=standard_id,
                                                   question_tags=que_tag)
                question.save()

                try:
                    a = 1
                    for i in range(4):
                        _, created = Options.objects.update_or_create(
                            option=column[a],
                            is_valid=column[a + 1],
                            question_id=question,
                        )
                        a += 2
                except Exception as e:
                    question.delete()
                    messages.error(request,
                                   "We caught an error while uploading your file. Please check your file again.",
                                   extra_tags='error_loading_file')
                    return redirect('add_question')

        if 'add_que' in request.POST:
            if form_que.is_valid() and form_opt1.is_valid() and form_opt2.is_valid() and form_opt3.is_valid() and form_opt4.is_valid():
                form_que = form_que.save(commit=False)
                form_que.created_by = user
                form_que.save()
                # print(form_que.id)
                # que_id = form_que.id
                if form_que.question_tags == "Passage Based":
                    form_opt1 = form_opt1.save(commit=False)
                    form_opt1.question_id = form_que
                    form_opt1.save()
                else:
                    form_opt1 = form_opt1.save(commit=False)
                    form_opt1.question_id = form_que
                    form_opt1.save()
                    form_opt2 = form_opt2.save(commit=False)
                    form_opt2.question_id = form_que
                    form_opt2.save()
                    form_opt3 = form_opt3.save(commit=False)
                    form_opt3.question_id = form_que
                    form_opt3.save()
                    form_opt4 = form_opt4.save(commit=False)
                    form_opt4.question_id = form_que
                    form_opt4.save()
        messages.success(request, 'Question Added Successfully')
        return redirect('add_question')
    else:
        form_que = CreateQuestion(initial={'package': "++++++++++"})
        form_opt1 = CreateOptions(prefix="option1")
        form_opt2 = CreateOptions(prefix="option2")
        form_opt3 = CreateOptions(prefix="option3")
        form_opt4 = CreateOptions(prefix="option4")
        package = Package.objects.all()
        standard = Standard.objects.all()

        return render(request, 'super_admin/test_questions.html',
                      {'form_que': form_que, 'form_opt1': form_opt1, 'form_opt2': form_opt2, 'form_opt3': form_opt3,
                       'form_opt4': form_opt4, 'package': package, 'standard': standard})


def load_que_history_view(request):
    package_id = request.GET.get('package')
    standard_id = request.GET.get('standard')
    subject_id = request.GET.get('sub_name')
    topic = request.GET.get('topic_name')

    # print(package_id, standard_id, subject_id, topic)

    questions = Question.objects.filter(topic_id=int(topic)).filter(sub_name_id=int(subject_id)).filter(
        package_id=int(package_id)).filter(standard_id=int(standard_id))

    return render(request, 'super_admin/questions_dropdown_list.html', {'questions': questions})


def test_detail_view(request, pk):
    test = Test.objects.get(id=pk)
    form = CreateTest(instance=test)

    if request.method == 'POST':
        form = CreateTest(request.POST, instance=test)
        form.updated_by = request.user
        form.save()
        return redirect('create_test')

    return render(request, 'super_admin/tests.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def create_test_view(request):
    if request.method == 'POST':
        form = CreateTest(request.POST)
        selected = request.POST.getlist('selected')
        print(selected)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            # print(form.id)
            for i in selected:
                question = Question.objects.get(id=i)
                value = request.POST.get('value' + i)
                que_history = QuestionHistory.objects.create(question=question, value=value, updated_by=request.user,
                                                             test_id=form.id)
                que_history.save()

            messages.success(request, 'Test Created Successfully', extra_tags="test_created")
            return redirect('create_test')
        else:
            return render(request, 'super_admin/tests.html', {'form': form})

    else:
        form = CreateTest()
        test = Test.objects.all()
        return render(request, 'super_admin/tests.html', {'form': form, 'test': test})


def load_std_view(request):
    teacher = request.GET.get("teacher")
    tsss = TStdSecSub.objects.filter(teacher_id=teacher)
    standard = []

    for t in tsss:
        standard.append(Standard.objects.get(standard_name=t.standard))

    print(standard)

    return render(request, 'super_admin/standard_dropdown_list.html', {'standard': standard})


# def load_student_view(request):
#     standard = request.GET.get('standard')
#     teacher = request.GET.get('teacher')
#     tsss = TStdSecSub.objects.get(teacher=teacher)
#     school = School.objects.get(school_name=tsss.school)
#
#     student = Student.objects.filter(standard=standard).filter(school=school)
#     return render(request, 'super_admin/student_dropdown_list.html', {'student': student})


def load_test_sub_view(request):
    atl = request.GET.get('atl')
    print(atl)
    if atl == 'true':
        subject = Subjects.objects.filter(atl=1)
    else:
        subject = Subjects.objects.filter(atl=0)
    return render(request, 'super_admin/subject_dropdown_list.html', {'subject_list': subject})


def load_test_school_view(request):
    atl = request.GET.get('atl')
    city = request.GET.get('city')
    std = request.GET.get('standard')
    sub = request.GET.get('subject')
    test_paper = request.GET.get('test_paper')
    quarter = request.GET.get('quarter')

    totl_test = Test.objects.filter(sub_name=sub).filter(quarter=quarter)

    teacher = []
    stu_count = []
    if atl == 'true':
        school = School.objects.filter(atl=1).filter(city=city)
        for sch in school:
            t = TStdSecSub.objects.filter(school = sch).filter(standard=std).filter(subject=sub)
            for tt in t:
                stu_count.append(Student.objects.filter(standard=tt.standard).filter(section=tt.section).filter(
                    school=tt.school).count())
                test = Test.objects
                teacher.append(tt)
        st = zip(teacher, stu_count)
    else:
        teacher.append(Teacher.objects.filter(city=city))

    return render(request, 'super_admin/test_sch_table.html', {'teacher': teacher, 'stu': stu_count, 'st': st})


def assign_test_view(request):
    if request.method == 'POST':
        standard = request.POST.get('standard')
        tstdsecsub = request.POST.getlist('selected')
        atl = request.POST.get('atl_test')
        # print("atl", atl, standard)

        # if atl == 'true':
        for t in tstdsecsub:
            tsss = TStdSecSub.objects.get(id=t)
            school = tsss.school
            section = tsss.section
            student = Student.objects.filter(standard_id=standard).filter(school=school).filter(section=section)
            for stu in student:
                form = AssignTests(request.POST)
                print('form', form.is_valid())
                if form.is_valid():
                    form.instance.school = school
                    form.instance.teacher = tsss.teacher
                    form.instance.student = stu
                    form.save()
        # if school is '' and student is '':
        #     student = Student.objects.filter(standard_id=standard).filter(fteacher_id=teacher)
        # elif school is not '' and student is '':
        #     student = Student.objects.filter(standard_id=standard).filter(school_id=school)
        # else:
        #     student = Student.objects.filter(id=student)
        #
        # for stu in student:
        #     form = AssignTests(request.POST)
        #     if form.is_valid():
        #         form.instance.student = stu
        #         form.save()
        messages.success(request, 'Test Assigned Successfully', extra_tags='test_assigned')
        return redirect('assign_test')
    else:
        form = AssignTests()
        state = Region.objects.filter(country_id=105)
        city = City.objects.all()
        quarter = Quarter.objects.all()
        board = AffiliationType.objects.all()
        return render(request, 'super_admin/test_assign.html', {'form': form, 'city': city, 'state': state,
                                                                'quarter': quarter, 'board': board})
