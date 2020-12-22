from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
User = get_user_model()

from super_admin.models import School, Student, Teacher


# Create your views here.
def school_home_view(request):
    if request.user.is_authenticated:
        stu = Student.objects.all()
        t = Teacher.objects.all()
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
        tea_stu = Teacher.objects.filter(school=None).annotate(nstu=Count('stu_teacher_assigned'))
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
