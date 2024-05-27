from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import UserType
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model() 
AUTH_USER_MODEL = 'attendance_app.User'
from master.models import *
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.timezone import localtime

def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('admin_index')
    return redirect('login')


@login_required
def AdminIndex(request):
    return render(request,'index.html')

@login_required
def UserAdd(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        repeat_password = request.POST['rpass']
        email = request.POST['email']
        contact_no = request.POST['mobno']
        usertype_id = request.POST['usertype']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address1 = request.POST['address1']
        # address2 = request.POST['address2']
        city_id = request.POST['city']
        # pincode = request.POST['pno']
        state_id = request.POST['state']
        nation_id = request.POST['country']
        department_id = request.POST['department']
        designation_id = request.POST['designation']
        employee_image = request.FILES['profile_pic']
        employee_code = request.POST['employee_card_id']

        if password != repeat_password:
            messages.error(request, "Passwords do not match")
            return redirect('user_add')

        usertype = UserType.objects.get(id=usertype_id)
        city = CityMaster.objects.get(id=city_id)
        state = StateMaster.objects.get(id=state_id)
        nation = NationMaster.objects.get(id=nation_id)
        department = DepartmentMaster.objects.get(id=department_id)
        designation = DesignationMaster.objects.get(id=designation_id)
    
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            contact_no=contact_no,
            usertype=usertype,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Save additional details
        employee = EmployeeMaster.objects.create(
            employee_code = employee_code,
            user=user,
            employee_name=f"{first_name} {last_name}",
            address=f"{address1}",
            city=city
        )
        EmployeeDepartment.objects.create(
            employee=employee,
            company=None,  # Assign the appropriate company if applicable
            department=department
        )
        EmployeeDesignation.objects.create(
            employee=employee,
            company=None,  # Assign the appropriate company if applicable
            designation=designation
        )
        EmployeeImage.objects.create(
            employee=employee,
            employee_image = employee_image
            
        )

        messages.success(request, "User created successfully")
        return redirect('useradd')

    usertypes = UserType.objects.all()
    nations = NationMaster.objects.all()
    states = StateMaster.objects.all()
    cities = CityMaster.objects.all()
    departments = DepartmentMaster.objects.all()
    designations = DesignationMaster.objects.all()
    
    return render(request, 'user-add.html', {
        'usertypes': usertypes,
        'nations': nations,
        'states': states,
        'cities': cities,
        'departments': departments,
        'designations': designations
    })

@login_required
def UserList(request):
    users = User.objects.all().prefetch_related(
        'employees__city__state__nation',
    
    )
    return render(request, 'user-list.html', {'users': users})

@login_required
def AttendanceOverview(request):
    attendance_records = AttendanceMaster.objects.all().select_related('employee')

    # Create a dictionary to store employee designations
    designations = {}
    for record in attendance_records:
        # Retrieve the designation for each employee
        emp_designation = EmployeeDesignation.objects.filter(employee=record.employee).first()
        print("Employee:", record.employee.employee_name)  # Debug print
        print("Designation:", emp_designation)  # Debug print
        # Check if there is a designation for the employee
        if emp_designation:
            designation = emp_designation.designation.designation
        else:
            # If no designation found, set it to None or any default value
            designation = "No Designation"  # Example default value
        designations[record.employee.id] = designation

    context = {
        'attendance_records': attendance_records,
        'designations': designations,
    }

    return render(request, 'attendance.html', context)


def employee_login(request):
    error_message = None
    if request.method == 'POST':
        mailid = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=mailid, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('employee_index')  # Redirect to a desired page after login
        else:
            error_message = 'Invalid email or password.'
    return render(request, 'employee/login.html', {'error_message': error_message})

def employee_logout(request):
    logout(request)
    messages.success(request,'You Have Successfully Logged Out.')
    return redirect('employee_login')


import requests

def get_location_from_ip(ip_address):
    try:
        response = requests.get(f'http://ipinfo.io/{ip_address}/json')
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        location = {
            'city': data.get('city', 'Unknown'),
            'region': data.get('region', 'Unknown'),
            'country': data.get('country', 'Unknown'),
        }
        return location
    except requests.RequestException as e:
        # Handle any request exceptions
        return {'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown'}

@login_required(login_url='employee_login')
def employee_index(request):
    user = request.user
    try:
        employee = EmployeeMaster.objects.select_related('user').prefetch_related('employeedesignation_set__designation').get(user=user)
        employee_image = EmployeeImage.objects.filter(employee=employee).first()
    except EmployeeMaster.DoesNotExist:
        employee = None
        employee_image = None

    if request.method == 'POST':
        action = request.POST.get('action')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        ip_address = request.META.get('REMOTE_ADDR')
        location = get_location_from_ip(ip_address)
        print(f"Location for IP address {ip_address}: {location['city']}, {location['region']}, {location['country']}")

        if action == 'checkin':
            AttendanceMaster.objects.create(
                employee=employee,
                company=None,  # Assuming EmployeeMaster has a related company field
                login_datetime=timezone.now(),
                login_ipaddress=ip_address
            )
        elif action == 'checkout':
            latest_attendance = AttendanceMaster.objects.filter(employee=employee).order_by('-login_datetime').first()
            if latest_attendance and not latest_attendance.logout_datetime:
                latest_attendance.logout_datetime = timezone.now()
                latest_attendance.logout_ipaddress = ip_address
                latest_attendance.save()

    latest_attendance = AttendanceMaster.objects.filter(employee=employee).order_by('-login_datetime').first()

    checkin_time = localtime(latest_attendance.login_datetime) if latest_attendance and latest_attendance.login_datetime else None
    checkout_time = localtime(latest_attendance.logout_datetime) if latest_attendance and latest_attendance.logout_datetime else None

    return render(request, 'employee/landing.html', {
        'employee': employee,
        'employee_image': employee_image,
        'latest_attendance': latest_attendance,
        'checkin_time': DateFormat(checkin_time).format('g:i A') if checkin_time else '',
        'checkout_time': DateFormat(checkout_time).format('g:i A') if checkout_time else ''
    })
    
