from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, logout



# Create your views here.
def atlp_home_view(request):
    return redirect('atl_school_details')


def school_details_view(request):
    if request.method == 'POST':
        form = SchoolDetailsFill(request.POST)

        if form.is_valid():
            other_board = request.POST.get('other_affi')
            form = form.save(commit=False)
            form.save()
            if other_board is not None:
                form.other_board = other_board.upper()
            messages.success(request, 'Data Added Successfully', extra_tags="data_add_success")
            return redirect('atl_school_details')
        else:
            messages.error(request, 'Incorrect Format', extra_tags="incorrect_format")
            return redirect('atl_school_details')
    else:
        form = SchoolDetailsFill()
        return render(request, 'atl_person/atl_school_details.html', {'form': form})


def atl_incharge_info_view(request):
    if request.method == 'POST':
        form = ATLInchargeInfo(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Data Added Successfully', extra_tags="data_add_success")
            return redirect('atl_incharge_info')
        else:
            messages.error(request, 'Incorrect Format', extra_tags="incorrect_format")
            return redirect('atl_incharge_info')
    else:
        form = ATLInchargeInfo()
        return render(request, 'atl_person/atl_incharge_info.html', {'form': form})


def atl_status_view(request):
    if request.method == 'POST':
        form = ATLStatusFill(request.POST)

        if form.is_valid():
            applied = request.POST.get("applied")
            qualified = request.POST.get("qualified")
            fund_received = request.POST.get("fund_received")
            form = form.save(commit=False)
            form.applied = applied
            form.qualified = qualified
            form.fund_received = fund_received
            form.save()
            messages.success(request, 'Data Added Successfully', extra_tags="data_add_success")
            return redirect('atl_status')
        else:
            messages.error(request, 'Incorrect Format', extra_tags="incorrect_format")
            return redirect('atl_status')
    else:
        form = ATLStatusFill()
        return render(request, 'atl_person/atl_status.html', {'form': form})


def teacher_nomination_view(request):
    if request.method == 'POST':
        form = TeacherNominationFill(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Data Added Successfully', extra_tags="data_add_success")
            return redirect('teacher_nomini')
        else:
            messages.error(request, 'Incorrect Format', extra_tags="incorrect_format")
            return redirect('teacher_nomini')
    else:
        form = TeacherNominationFill()
        return render(request, 'atl_person/teacher_nomini.html', {'form': form})


def vendor_reg_view(request):
    if request.method == 'POST':
        form = VendorReg(request.POST)

        if form.is_valid():
            order = request.POST.get('order')
            package = request.POST.getlist('package')
            print(package)
            form = form.save(commit=False)
            form.gem_order = order
            form.package = package
            form.save()
            messages.success(request, 'Data Added Successfully', extra_tags='data_add_success')
            return redirect('vendor_reg')
        else:
            messages.error(request, 'Incorrect Format', extra_tags='incorrect_format')
            return redirect('vendor_reg')
    else:
        form = VendorReg()
        package = Package.objects.all()
        return render(request, 'atl_person/vendor_reg.html', {'form': form, 'package': package})


def lab_reg_view(request):
    if request.method == 'POST':
        form = LabReg(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Data Added Successfully', extra_tags='data_add_success')
            return redirect('lab_reg')
        else:
            messages.error(request, 'Incorrect Format', extra_tags='incorrect_format')
            return redirect('lab_reg')
    else:
        form = LabReg()
        return render(request, 'atl_person/lab_reg.html', {'form': form})


def mentor_of_change_view(request):
    if request.method == 'POST':
        form = MOCReg(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Data Added Successfully', extra_tags='data_add_success')
            return redirect('mentor_of_change')
        else:
            messages.error(request, 'Incorrect Format', extra_tags='incorrect_format')
            return redirect('mentor_of_change')
    else:
        form = MOCReg()
        return render(request, 'atl_person/mentor_of_change.html', {'form': form})


def add_components(request):
    if request.method == 'POST':
        form = AddComponents(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Data Added Successfully', extra_tags='data_add_success')
            return redirect('add_component')
        else:
            messages.error(request, 'Incorrect Format', extra_tags='incorrect_format')
            return redirect('add_component')
    else:
        form = AddComponents()
        return render(request, 'atl_person/add_components.html', {'form': form})


def load_component_view(request):
    package_id = request.GET.get('package')
    component = PackComponent.objects.filter(package_id=package_id)  # .values_list('slug', flat=True)
    print(package_id, component)
    return render(request, 'atl_person/component_dropdown_list.html', {'comp': component})


def logout_view(request):
    logout(request)
    return render(request, 'accounts/login.html')


def change_password_view(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        return render(request, 'accounts/login.html')
    return render(request, 'super_admin/change_password.html', {'form': form})

