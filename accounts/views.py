from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from super_admin.models import *
from accounts.models import *
from .forms import *


# Create your views here.
def index_view(request):
    print('index')
    return redirect('login_view')


def super_login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    print(username)
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        if request.user.user_type.role_name == 'super_admin':
            return redirect('admin_index')
    else:
        messages.error(request, 'Invalid Username or password!')
        # previous_page=request.META['HTTP_REFERER']
        print('na')

        return render(request, 'super_admin/login.html')


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    print(username)
    print(password)
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        if request.user.user_type.role_name == 'school':
            print('school')
            return redirect('school_home')
        if request.user.user_type.role_name == 'teacher':
            print('teacher')
            return redirect('teacher_home')
        if request.user.user_type.role_name == 'student':
            print('student')
            return redirect('student_home')
        if request.user.user_type.role_name == 'atl_person':
            print('atl_person')
            return redirect('atlp_home')
    else:
        messages.error(request, 'Invalid Username or password!', extra_tags="invalid_user")
        # previous_page=request.META['HTTP_REFERER']
        return render(request, 'accounts/login.html')


def school_reg_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('school_home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/registerschool.html', {'form': form})


def student_reg_view(request):
    if request.method == 'POST':
        form = SignUpForm_Person(request.POST)
        print("student")
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            u = User.objects.get(username=username, last_name=last_name, email=email)
            u.user_type = Roles.objects.get(role_name="student")
            u.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('student_home')
    else:
        form = SignUpForm_Person()
    return render(request, 'accounts/registerstudent.html', {'form': form})


def teacher_reg_view(request):
    if request.method == 'POST':
        form = SignUpForm_Person(request.POST)
        print("teacher")
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            u = User.objects.get(username=username, last_name=last_name, email=email)
            u.user_type = Roles.objects.get(role_name="teacher")
            u.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('teacher_home')
    else:
        form = SignUpForm_Person()
    return render(request, 'accounts/registerteacher.html', {'form': form})

# def choose_reg_view(request):
#     return render(request, 'common/chooseschoolreg.html')
#
#
# def atl_school_reg_view(request):
#     return render(request, 'common/schoolreg.html')
#
#
# def cbse_reg_view(request):
#     return render(request, 'common/inchargecbse.html')
#
#
# def school_atl_incharge_view(request):
#     return render(request, 'common/incharge.html')
#
#
# def vendor_reg_view(request):
#     return render(request, 'common/vendor.html')
#
#
# def lab_reg_view(request):
#     return render(request, 'common/regi.html')
#
#
# def mentor_change_view(request):
#     return render(request, 'common/mentorofchange.html')
#
#
# def authority_dash_view(request):
#     return render(request, 'common/authority.html')
#
#
# def assessment_view(request):
#     return render(request, 'common/atlcbse.html')
#
#
# def logout_admin_view(request):
#     logout(request)
#     return redirect('admin_index')


# def cbse_login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         schoolid = request.POST.get('schoolid')
#
#         if request.POST.get('type') == 'Teacher':
#             teacherid = request.POST.get('teacherid')
#             if (Teacher.objects.filter(user__username=username, school_id=schoolid, id=teacherid).count() == 1):
#                 print(username, password)
#                 user = authenticate(username=username, password=password)
#                 print(user)
#                 if user != None:
#                     login(request, user)
#                     messages.success(request, 'Login Successful!')
#                     return redirect('cbse_login')
#                 else:
#                     messages.error(request, 'Invalid username or passsword!')
#                     return redirect('cbse_login')
#
#             else:
#                 messages.error(request, 'Invalid Credentials!')
#                 return redirect('cbse_login')
#
#         else:
#             studentid = request.POST.get('studentid')
#             print(studentid)
#             if (Student.objects.filter(user__username=username, school_id=schoolid, id=studentid).count() == 1):
#                 user = authenticate(username=username, password=password)
#                 if user != None:
#                     login(request, user)
#                     messages.success(request, 'Login Successful!')
#                     return redirect('student_home')
#                 else:
#                     messages.error(request, 'Invalid username or passsword!')
#                     return redirect('cbse_login')
#
#             else:
#                 messages.error(request, 'Invalid Credentials!')
#                 return redirect('cbse_login')
#     else:
#         return render(request, 'common/cbselogin.html')
#
#
# def atl_login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         schoolid = request.POST.get('schoolid')
#
#         if request.POST.get('type') == 'Teacher':
#             teacherid = request.POST.get('teacherid')
#             if (Teacher.objects.filter(user__username=username, school_id=schoolid, id=teacherid).count() == 1):
#                 print(username, password)
#                 user = authenticate(username=username, password=password)
#                 print(user)
#                 if user != None:
#                     login(request, user)
#                     messages.success(request, 'Login Successful!')
#                     return redirect('atl_login')
#                 else:
#                     messages.error(request, 'Invalid username or passsword!')
#                     return redirect('atl_login')
#
#             else:
#                 messages.error(request, 'Invalid Credentials!')
#                 return redirect('atl_login')
#
#         else:
#             studentid = request.POST.get('studentid')
#             print(studentid)
#             if (Student.objects.filter(user__username=username, school_id=schoolid, id=studentid).count() == 1):
#                 user = authenticate(username=username, password=password)
#                 if user != None:
#                     login(request, user)
#                     messages.success(request, 'Login Successful!')
#                     return redirect('student_home')
#                 else:
#                     messages.error(request, 'Invalid username or passsword!')
#                     return redirect('atl_login')
#
#             else:
#                 messages.error(request, 'Invalid Credentials!')
#                 return redirect('atl_login')
#
#     return render(request, 'common/atllogin.html')
#
#
