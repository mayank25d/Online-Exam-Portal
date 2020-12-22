from django import forms
from .models import *


class SchoolDetailsFill(forms.ModelForm):
    class Meta:
        model = SchoolDetails
        fields = "__all__"
        exclude = ("other_board",)

        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'school_regId': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'state': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'affiliation': forms.Select(attrs={'class': 'form-control form-control-alternative'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['school_regId'].label = 'School Registration ID'


class ATLInchargeInfo(forms.ModelForm):
    class Meta:
        model = SchoolATLIncharge
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'unique_id': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }


class ATLStatusFill(forms.ModelForm):
    class Meta:
        model = ATLStatus
        fields = "__all__"
        exclude = ('applied', 'atl_qualified', 'fund_received')

        widgets = {
            'date_applied': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'registered_by': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'reg_p_phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'reg_p_email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'date_qualified': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'fund_on': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registered_by'].label = 'Name'
        self.fields['reg_p_phone'].label = 'Contact Number'
        self.fields['reg_p_email'].label = 'Email ID'
        self.fields['date_applied'].label = 'Which Date'
        self.fields['date_applied'].required = False
        self.fields['date_qualified'].label = 'Which Date'
        self.fields['date_qualified'].required = False
        self.fields['fund_on'].label = 'Which Date'
        self.fields['fund_on'].required = False



class TeacherNominationFill(forms.ModelForm):
    class Meta:
        model = TeacherNomination
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }


class VendorReg(forms.ModelForm):
    class Meta:
        model = VendorRegistration
        fields = "__all__"
        exclude = ('gem_order', 'package')

        widgets = {
            'gem_order_number': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'purchase_order_no': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'company_inc_id': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'person_name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'person_phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'person_email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gem_order_number'].label = 'Please fill GEM order number'
        self.fields['purchase_order_no'].label = 'Purchase Order No.'
        self.fields['company_name'].label = 'Company Name'
        self.fields['company_inc_id'].label = 'Company Incorporation ID'
        self.fields['person_email'].label = 'Email ID'
        self.fields['phone'].label = 'Contact Number'
        self.fields['email'].label = 'Email ID'
        self.fields['person_name'].label = 'Name'
        self.fields['person_phone'].label = 'Contact Number'

class AddComponents(forms.ModelForm):
    class Meta:
        model = PackComponent
        fields = "__all__"

        widgets = {
            'package': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'component': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }


class LabReg(forms.ModelForm):
    class Meta:
        model = LabPackageReg
        fields = "__all__"

        widgets = {
            'package': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'component': forms.Select(attrs={'class': 'form-control form-control-alternative'}),
            'other_offerings': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'scope_of_training': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'days_training': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'training_attendant': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['other_offerings'].label = 'Other Offerings Please specify'
        self.fields['scope_of_training'].label = 'Scope of training'
        self.fields['days_training'].label = 'No of days of training'
        self.fields['training_attendant'].label = 'Who attended training'

        self.fields['component'].queryset = PackComponent.objects.none()


class MOCReg(forms.ModelForm):
    class Meta:
        model = MentorOfChange
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'mentor_id': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'who_appointed': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'appointment_date': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'edu_back': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'pro_back': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'current_company': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'days_of_visit': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'skills': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
            'profile': forms.TextInput(attrs={'class': 'form-control form-control-alternative'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = 'Name of Mentor'
        self.fields['mentor_id'].label = 'Mentor ID(Assigned by Niti Aayog)'
        self.fields['who_appointed'].label = 'Who Appointed'
        self.fields['appointment_date'].label = 'Which date he got appointed'
        self.fields['edu_back'].label = 'Education Background'
        self.fields['pro_back'].label = 'Professional Background'
        self.fields['phone'].label = 'Contact Details'
        self.fields['current_company'].label = 'Which company currently she/he is working'
        self.fields['days_of_visit'].label = 'How many days does she/he visits schools'
        self.fields['skills'].label = 'Specialization and skills'
        self.fields['profile'].label = 'Which profile she/he is working'

