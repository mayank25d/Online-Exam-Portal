from django.db import models
from cities_light.models import *
from super_admin.models import *
from tests.models import Package


# Create your models here.
class SchoolDetails(models.Model):
    school_name = models.CharField(max_length=200, null=True)
    school_regId = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=1000, null=True)
    state = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=250, null=True)
    # state = models.ForeignKey(Region, related_name='atlp_school_state', null=True, on_delete=models.SET_NULL)
    # city = models.ForeignKey(City, related_name='atlp_school_city', null=True, on_delete=models.SET_NULL)
    pin_code = models.CharField(max_length=500, null=True)
    phone = models.CharField(max_length=500, null=True)
    email = models.EmailField(max_length=500, null=True)
    other_board = models.CharField(max_length=200, null=True)
    affiliation = models.ForeignKey(AffiliationType, related_name='atlp_school_affi', null=True,
                                    on_delete=models.SET_NULL)
    filled_by = models.ForeignKey(ATLPerson, related_name='school_data_by', null=True, on_delete=models.SET_NULL)


class SchoolATLIncharge(models.Model):
    name = models.CharField(max_length=200, null=True)
    unique_id = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=500, null=True)
    email = models.EmailField(max_length=500, null=True)
    filled_by = models.ForeignKey(ATLPerson, related_name='atlincharge_data_by', null=True, on_delete=models.SET_NULL)


class ATLStatus(models.Model):
    applied = models.BooleanField(default=True, null=True)
    date_applied = models.DateField(auto_now=False, auto_now_add=False, null=True)
    registered_by = models.CharField(max_length=200, null=True)
    reg_p_phone = models.CharField(max_length=500, null=True)
    reg_p_email = models.EmailField(max_length=500, null=True)
    atl_qualified = models.BooleanField(default=True, null=True)
    date_qualified = models.DateField(auto_now=False, auto_now_add=False, null=True)
    fund_received = models.BooleanField(default=True, null=True)
    fund_on = models.DateField(auto_now=False, auto_now_add=False, null=True)
    filled_by = models.ForeignKey(ATLPerson, related_name='atlstatus_data_by', null=True, on_delete=models.SET_NULL)


class TeacherNomination(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=500, null=True)
    email = models.EmailField(max_length=500, null=True)
    filled_by = models.ForeignKey(ATLPerson, related_name='teacher_data_by', null=True, on_delete=models.SET_NULL)


class VendorRegistration(models.Model):
    gem_order = models.BooleanField(default=True, null=True)
    gem_order_number = models.CharField(max_length=300, null=True)
    purchase_order_no = models.CharField(max_length=300, null=True)
    package = models.CharField(max_length=200, null=True)
    # package = models.ForeignKey(Package, related_name='atlp_vendor_package', null=True, on_delete=models.SET_NULL)
    company_name = models.CharField(max_length=500, null=True)
    company_inc_id = models.CharField(max_length=500, null=True)
    address = models.CharField(max_length=500, null=True)
    phone = models.CharField(null=True, max_length=500)
    email = models.EmailField(max_length=500, null=True)
    person_name = models.CharField(max_length=200, null=True)
    person_phone = models.CharField(max_length=500, null=True)
    person_email = models.EmailField(null=True)
    filled_by = models.ForeignKey(ATLPerson, related_name='vendor_data_by', null=True, on_delete=models.SET_NULL)


class PackComponent(models.Model):
    package = models.ForeignKey(Package, related_name='atlp_comp_package', null=True, on_delete=models.SET_NULL)
    component = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.component


class LabPackageReg(models.Model):
    package = models.ForeignKey(Package, related_name='atlp_lab_package', null=True, on_delete=models.SET_NULL)
    component = models.ForeignKey(PackComponent, related_name='atlp_lab_comp', null=True, on_delete=models.SET_NULL)
    other_offerings = models.TextField(null=True)
    scope_of_training = models.TextField(null=True)
    days_training = models.IntegerField(null=True)
    training_attendant = models.TextField(null=True)
    filled_by = models.ForeignKey(ATLPerson, related_name='lab_data_by', null=True, on_delete=models.SET_NULL)


class MentorOfChange(models.Model):
    name = models.CharField(max_length=200, null=True)
    mentor_id = models.CharField(max_length=200, null=True)
    who_appointed = models.CharField(max_length=200, null=True)
    appointment_date = models.DateField(auto_now_add=False, null=True, auto_now=False)
    edu_back = models.TextField(null=True)
    pro_back = models.TextField(null=True)
    phone = models.CharField(max_length=500, null=True)
    email = models.EmailField(max_length=500, null=True)
    address = models.TextField(null=True)
    current_company = models.CharField(max_length=500, null=True)
    profile = models.CharField(max_length=500, null=True)
    days_of_visit = models.IntegerField(null=True)
    skills = models.TextField(null=True)
    filled_by = models.ForeignKey(ATLPerson, related_name='mentor_data_by', null=True, on_delete=models.SET_NULL)
