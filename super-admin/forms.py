from django import forms
from .models import *
from tests.models import Test, TestTopic, Package, Question, Subjects, Options, QuestionHistory
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime


class Packages(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

        widgets = {
            'package': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }


class SchoolBoard(forms.ModelForm):
    class Meta:
        model = AffiliationType
        fields = "__all__"

        widgets = {
            'affiliation_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }


class SchoolReg(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
        exclude = ('user', 'password')

        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'state': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'city': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'atl': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'school_board': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'incharge_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'incharge_email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['state'].queryset = Region.objects.filter(country_id=105)
        self.fields['atl'].label = 'ATL Authorised'
        self.fields['atl'].required = False
        # self.fields['city'].queryset = City.objects.values_list('slug', flat=True)


class StudentReg(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('user', 'password', 'assessment_given')

        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'school': forms.Select(attrs={'class': 'form-control form-control-alternative', 'placeholder': 'If Any'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'state': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'city': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'fteacher': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'enrollment_no': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'standard': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'section': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fteacher'].queryset = Teacher.objects.filter(school__isnull=True)
        self.fields['state'].queryset = Region.objects.filter(country_id=105)

        self.fields['fteacher'].label = "Freelancing Teachers"
        self.fields['fteacher'].required = False

        self.fields['school'].required = False
        self.fields['enrollment_no'].required = False


class TeacherReg(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ('user', 'password', 'assessment_created')

        widgets = {
            'teacher_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'enrollment_no': forms.TextInput(
                attrs={'class': 'form-control form-control-alternative', 'placeholder': 'If Any'}),
            'school': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'state': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'city': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['state'].queryset = Region.objects.filter(country_id=105)


class AuthorityReg(forms.ModelForm):
    class Meta:
        model = AuthorityAccount
        fields = '__all__'
        exclude = ('user', 'password', 'government')

        widgets = {
            'employee_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'designation': forms.TextInput(
                attrs={'class': 'form-control form-control-alternative', 'placeholder': 'If Any'}),
            'authority_type': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'state': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'city': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
        }


class ATLPersonReg(forms.ModelForm):
    class Meta:
        model = ATLPerson
        fields = '__all__'
        exclude = ('user', 'password')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'state': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'city': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['state'].queryset = Region.objects.filter(country_id=105)



class CreateSubject(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = '__all__'
        exclude = ('atl',)

        widgets = {
            'standard': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'package': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'sub_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].required = False


class CreateTopic(forms.ModelForm):
    class Meta:
        model = TestTopic
        fields = '__all__'

        widgets = {
            'standard': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'package': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'sub_name': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'topic_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }


class CreateQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ('language', 'created_at', 'updated_at', 'created_by', 'updated_by', 'level')

        widgets = {
            'standard': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'package': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'sub_name': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'topic': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'question_tags': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'question': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['package'].initial = "----------"


class CreateOptions(forms.ModelForm):
    class Meta:
        model = Options
        fields = '__all__'
        exclude = ('question_id',)
        widgets = {
            'option': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'is_valid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_valid'].label = ''
        self.fields['option'].label = ''


class AddQuestion(forms.ModelForm):
    class Meta:
        model = QuestionHistory
        fields = '__all__'
        exclude = ('test', 'updated_by', 'created_at')

        widgets = {
            'question': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'value': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }


class CreateTest(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by', 'test_lang', 'test_date')

        widgets = {
            'affiliation': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'quarter': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'package': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'sub_name': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'test_duration': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'standard': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['affiliation'].required = False


class AssignTests(forms.ModelForm):
    class Meta:
        model = AssignTest
        fields = '__all__'
        exclude = ('test_status', 'student', 'school', 'teacher')

        widgets = {
            'standard': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'subject': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'test_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-alternative'}),
            'test_paper': forms.Select(attrs={'class': 'form-control form-control-alternative'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test_date'].initial = datetime.now()
