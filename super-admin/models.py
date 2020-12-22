from django.db import models
from django.contrib.auth import get_user_model
from cities_light.models import City, Region, Country
# from cities_light.receivers import connect_default_signals

User = get_user_model()


# Create your models here.

class AffiliationType(models.Model):
    affiliation_name = models.CharField(max_length=200)

    def __str__(self):
        return self.affiliation_name


class Standard(models.Model):
    standard_name = models.CharField(max_length=20)

    def __str__(self):
        return self.standard_name


class School(models.Model):
    user = models.ForeignKey(User, null=True, related_name="school_pro", on_delete=models.SET_NULL)
    school_name = models.CharField(max_length=50)
    password = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.BigIntegerField()
    address = models.TextField()
    state = models.ForeignKey(Region, null=True, related_name="sch_state", on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, related_name="sch_city", on_delete=models.SET_NULL)
    atl = models.BooleanField(default=True)
    school_board = models.ForeignKey(AffiliationType, related_name="board", on_delete=models.SET_NULL, null=True)
    stu_limit = models.CharField(max_length=100, default=100, null=True)
    test_limit = models.CharField(max_length=100, default=4, null=True)
    incharge_name = models.CharField(max_length=90, null=True)
    incharge_email = models.EmailField(null=True)

    def __str__(self):
        return self.school_name


class Section(models.Model):
    school = models.ForeignKey(School, null=True, related_name='sec_school', on_delete=models.SET_NULL)
    standard = models.ForeignKey(Standard, null=True, related_name='section_standard', on_delete=models.SET_NULL)
    section_name = models.CharField(max_length=20)

    def __str__(self):
        return self.section_name


class Teacher(models.Model):
    user = models.ForeignKey(User, null=True, related_name="teacher", on_delete=models.SET_NULL)
    school = models.ForeignKey(School, null=True, blank=True, related_name="teacher_school", on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=40)
    enrollment_no = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField()
    stu_limit = models.CharField(max_length=100, default=100, null=True)
    test_limit = models.CharField(max_length=100, default=4, null=True)
    state = models.ForeignKey(Region, null=True, related_name="teach_state", on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, related_name="teach_city", on_delete=models.SET_NULL)
    assessment_created = models.IntegerField(default=0)

    def __str__(self):
        return self.teacher_name


class TStdSecSub(models.Model):
    school = models.ForeignKey(School, null=True, related_name='tsss_sch', on_delete=models.SET_NULL)
    teacher = models.ForeignKey(Teacher, null=True, related_name='tsss_teacher', on_delete=models.SET_NULL)
    standard = models.ForeignKey(Standard, null=True, related_name='tsss_std', on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, related_name='tsss_sec', on_delete=models.SET_NULL)
    package = models.ForeignKey('tests.Package', null=True, related_name='tsss_pack', on_delete=models.SET_NULL)
    subject = models.ForeignKey('tests.Subjects', null=True, related_name='tsss_sub', on_delete=models.SET_NULL)


class Student(models.Model):
    user = models.ForeignKey(User, null=True, related_name="student", on_delete=models.SET_NULL)
    school = models.ForeignKey(School, null=True, related_name="student_school", on_delete=models.SET_NULL)
    student_name = models.CharField(max_length=40)
    enrollment_no = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=40)
    email = models.EmailField(null=True)
    phone = models.IntegerField(null=True)
    address = models.TextField()
    state = models.ForeignKey(Region, null=True, related_name="stu_state", on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, related_name="stu_city", on_delete=models.SET_NULL)
    standard = models.ForeignKey(Standard, max_length=10, related_name="student_class", null=True,
                                 on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, related_name='stu_sec', null=True, on_delete=models.SET_NULL)
    fteacher = models.ForeignKey(Teacher, related_name='student_ft', null=True, on_delete=models.SET_NULL)
    assessment_given = models.IntegerField(default=0)

    def __str__(self):
        return self.student_name


class ATLPerson(models.Model):
    user = models.ForeignKey(User, null=True, related_name="atl_person", on_delete=models.SET_NULL)
    name = models.CharField(max_length=70)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField()
    state = models.ForeignKey(Region, null=True, related_name='atl_person_state', on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, related_name='atl_person_city', on_delete=models.SET_NULL)
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.name


# class SchoolAssignedTestPaper(models.Model):
#     test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
#     students = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
#     school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
#     duration = models.IntegerField()
#     start_time = models.DateTimeField()
#
#
# class IndividualTestPaper(models.Model):
#     test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
#     student = models.ForeignKey(IndividualStudents, on_delete=models.SET_NULL, null=True)
#     duration = models.IntegerField()
#     start_time = models.DateTimeField()


class AuthorityAccount(models.Model):
    auth_type = (
        ('CBSE Authority', 'CBSE Authority'),
        ('Niti Aayog', 'Niti Aayog'),
        ('State Eductaion', 'State Eductaion'),
        ('Cooperation', 'Cooperation'),
    )
    user = models.ForeignKey(User, related_name="authority", on_delete=models.SET_NULL, null=True)
    email = models.EmailField(null=True)
    employee_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    state = models.ForeignKey(Region, null=True, related_name="auth_state", on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, related_name="auth_city", on_delete=models.SET_NULL)
    phone = models.IntegerField()
    password = models.CharField(max_length=40)
    designation = models.CharField(max_length=100, null=True)
    government = models.CharField(max_length=50, null=True)
    authority_type = models.CharField(max_length=60, choices=auth_type)


class AssignTest(models.Model):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    standard = models.ForeignKey(Standard, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey('tests.Subjects', on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    test_paper = models.ForeignKey('tests.Test', on_delete=models.SET_NULL, null=True)
    test_date = models.DateTimeField(null=True)
    test_status = models.CharField(max_length=60, default="pending")

# class StudentTestPaper(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
#     elearning_stu = models.ForeignKey(IndividualStudents, on_delete=models.SET_NULL, null=True)
#     assigned_test = models.ForeignKey(AssignTest, on_delete=models.SET_NULL, null=True)
#     marks = models.IntegerField()
#     attempt = models.IntegerField()
#     question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
