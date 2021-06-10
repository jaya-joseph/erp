import datetime

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from RITSOFT_APP.models import FacultyDetails, Department, FacultyDesignation, AcademicYear


def home(request):
    return render(request, 'RITSOFT_APP/users/home.html')


def about(request):
    return render(request, 'RITSOFT_APP/users/about.html')


def contact(request):
    return render(request, 'RITSOFT_APP/users/contact.html')


def login_redirect(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if user.login.usertype == 'admin':
                return redirect('admin_home')
            if request.user.login.usertype == 'faculty':
                return redirect('admin_home')
            else:
                return redirect('login')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')

    return render(request, 'RITSOFT_APP/users/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'RITSOFT_APP/users/logout.html')


@login_required
def admin_home(request):
    return render(request, 'RITSOFT_APP/admin/home.html', {'title': "Admin Home"})


@login_required
def designation(request):
    departments = Department.objects.all().order_by('dept_name')
    if request.method == 'POST':
        dept_id = request.POST['dept_id']
        department = Department.objects.get(pk=dept_id)
        faculty_id = request.POST['faculty_id']
        faculty = FacultyDetails.objects.get(pk=faculty_id)
        new_designations = request.POST.getlist('designation[]')

        old_designations = list(FacultyDesignation.objects.filter(faculty=faculty_id).values('designation'))

        # delete all old designations of that faculty
        FacultyDesignation.objects.filter(faculty=faculty_id).delete()

        # delete old designations like prncpl, pgdean, ugdean, sadean, stfadv
        # as these designations can be allotted only to one person
        if 'prncpl' in new_designations:
            FacultyDesignation.objects.filter(designation='prncpl').delete()
        if 'pgdean' in new_designations:
            FacultyDesignation.objects.filter(designation='pgdean').delete()
        if 'ugdean' in new_designations:
            FacultyDesignation.objects.filter(designation='ugdean').delete()
        if 'sadean' in new_designations:
            FacultyDesignation.objects.filter(designation='sadean').delete()
        if 'stfadv' in new_designations:
            FacultyDesignation.objects.filter(designation='stfadv').delete()

        # if hod in old designations and not in new designations then set hod null in department
        hod_in_old_des = list(filter(lambda fac: fac['designation'] == 'hod', old_designations))
        if hod_in_old_des and 'hod' not in new_designations:
            hod_dept = department
            hod_dept.hod = None
            hod_dept.save()

        if 'hod' in new_designations:
            # delete old hod of selected department in designations
            dept_faculty = FacultyDetails.objects.filter(department=department)
            FacultyDesignation.objects.filter(designation='hod', faculty__in=dept_faculty).delete()
            # update hod in department
            hod_dept = Department.objects.get(pk=dept_id)
            hod_dept.hod = faculty
            hod_dept.save()

        # add new designations
        for des in new_designations:
            new_des = FacultyDesignation(faculty=faculty, designation=des)
            new_des.save()

    return render(request, 'RITSOFT_APP/admin/desig.html', {'title': "Designation", 'departments': departments})


@login_required
def fetch_faculty_of_dept(request):
    if request.is_ajax() and request.method == 'POST':
        dept_id = request.POST['dept_id']
        faculties = list(FacultyDetails.objects.filter(department_id=dept_id).values('pk', 'name'))
        # for fac in faculties:
        #     options += f"<option value=\"{fac['pk']}\">{fac['name']}</option>"
        # return JsonResponse({"faculties": options}, status=200)
        return JsonResponse({'faculties': faculties})
    else:
        return HttpResponse("Error in Request")


@login_required
def fetch_designation_of_faculty(request):
    if request.is_ajax() and request.method == 'POST':
        fac_id = request.POST['fac_id']
        desig = FacultyDesignation.objects.filter(faculty=fac_id)
        return render(request, 'RITSOFT_APP/admin/fetchdesig.html', {'designation': desig})
    else:
        return HttpResponse("Error in Request")


@login_required
def add_academic_year(request):
    academic_years = AcademicYear.objects.all()
    cur_acd_yr = academic_years.get(status=1).acd_year
    start = datetime.datetime.now().strftime("%Y")
    end = int(start) + 1
    new_acd_yr = str(start) + "-" + str(end)

    if request.method == 'POST':
        acd_yr = request.POST['acd']
        try:
            acd_yr_obj = academic_years.get(acd_year=acd_yr)
            academic_years.update(status=0)  # set all status to 0
            acd_yr_obj.status = 1
            acd_yr_obj.save()
            return redirect('add_academic_year')
        except AcademicYear.DoesNotExist:
            academic_years.update(status=0)  # set all status to 0
            AcademicYear(acd_year=acd_yr, status=1).save()
            return redirect('add_academic_year')

    return render(request,
                  'RITSOFT_APP/admin/acdmc_yr_add.html', {
                      'cur_acd_yr': cur_acd_yr,
                      'new_acd_yr': new_acd_yr,
                      'title': "add Academic Year"
                  })


@login_required
def change_academic_year(request):
    academic_years = AcademicYear.objects.all()
    cur_acd_yr = academic_years.get(status=1).acd_year
    # todo: manage exceptions DoesNotExist and MultipleObjectsReturned

    if request.method == 'POST':
        acd_yr = request.POST['acd']
        acd_yr_obj = AcademicYear.objects.get(pk=acd_yr)
        academic_years.update(status=0)  # set all status to 0
        acd_yr_obj.status = 1  # set selected status to 1
        acd_yr_obj.save()
        return redirect('change_academic_year')

    return render(request,
                  'RITSOFT_APP/admin/acdmc_yr_change.html', {
                      'academic_years': academic_years,
                      'cur_acd_yr': cur_acd_yr,
                      'title': "Change Academic Year"
                  })
