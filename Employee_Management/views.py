from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json, logging
from django.utils.crypto import get_random_string
from datetime import datetime,timedelta
from django.utils import timezone
from django.core.mail import send_mail
from Employee_Management import *
from django.contrib.auth.hashers import check_password,make_password
from django.conf import settings
import random
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

logger=logging.getLogger(__name__)
# ------------------List all employees-------------------
def get_all_employees(request):
    employees = Employee.objects.all().values('E_id', 'first_name', 'last_name', 'email', 'phone_number')
    return JsonResponse(list(employees), safe=False)

# ---------------------View employee details------------------------


def employee_detail(request):
    employee_id = request.GET.get('id')
    email_id = request.GET.get('emailid')

    if employee_id:
        employee = get_object_or_404(Employee, E_id=employee_id)
    elif email_id:
        employee = get_object_or_404(Employee, email=email_id)
    else:
        return JsonResponse({'error': 'No valid identifier provided'}, status=400)

    employee_data = {
        'id': employee.id,
        'E_id': employee.E_id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'email': employee.email,
        'phone_number': employee.phone_number,
        'age': employee.age,
        'gender': employee.gender,
        'Designation': employee.Designation,
        'department': employee.department,
        'date_of_birth': employee.date_of_birth,
        'date_joined': employee.date_joined,
        'is_HR': employee.is_HR,
        'is_emp': employee.is_emp,
        'is_admin': employee.is_admin,
    }
    return JsonResponse(employee_data)


#------------------ Create a new employee------------------------


@csrf_exempt
def create_employee(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Check if an employee with the given E_id already exists
            if Employee.objects.filter(E_id=data['E_id']).exists():
                return JsonResponse({"message": "User with this ID already exists"}, status=400)

            # Create the employee with all string fields in uppercase
            employee = Employee.objects.create(
                E_id=str(data['E_id']).upper(),
                first_name=str(data['first_name']).upper(),
                last_name=str(data['last_name']).upper(),
                email=data['email'],
                phone_number=data['phone_number'],
                age=data['age'],  # Age remains unchanged
                gender=str(data['gender']).upper() if data.get('gender') else None,
                Designation=str(data['Designation']).upper(),
                department=str(data['department']).upper(),
                date_of_birth=data['date_of_birth'],  # Date of birth remains unchanged
                is_HR=data.get('is_HR', False),
                is_emp=data.get('is_emp', False),
                is_admin=data.get('is_admin', False)
            )

            return JsonResponse({'id': employee.id, 'name': employee.first_name, 'message': 'Employee created successfully'}, status=201)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e.args[0]}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#------------------- Update an existing employee-----------------------
@csrf_exempt
def update_employee_byId(request):
    E_id = request.GET.get('id')
    employee = get_object_or_404(Employee, E_id=E_id)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Ensure the fields are strings before calling upper() and apply upper() for string fields
            employee.E_id = str(data.get('E_id', employee.E_id)).upper()
            employee.first_name = str(data.get('first_name', employee.first_name)).upper()
            employee.last_name = str(data.get('last_name', employee.last_name)).upper()
            employee.email = data.get('email', employee.email)
            employee.phone_number =data.get('phone_number', employee.phone_number)
            employee.age = data.get('age', employee.age+1)  # Assuming age is an integer, no need for upper()
            employee.gender = str(data.get('gender', employee.gender)).upper() if data.get('gender') else employee.gender
            employee.Designation = str(data.get('Designation', employee.Designation)).upper()
            employee.department = str(data.get('department', employee.department)).upper()
            employee.date_of_birth = data.get('date_of_birth', employee.date_of_birth)  # No need for upper() on dates
            employee.is_HR = data.get('is_HR', employee.is_HR)
            employee.is_emp = data.get('is_emp', employee.is_emp)
            employee.is_admin = data.get('is_admin', employee.is_admin)
            
            # Save the updated employee data
            employee.save()
            return JsonResponse({'id': employee.id, 'message': 'Employee updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# ---------------------Delete an employee----------------
@csrf_exempt
def delete_employee_byId(request):
    if request.method == "DELETE":
        E_id=request.GET.get('id')
        try:
            # print("before employees list",E_id)
            employees = Employee.objects.filter(E_id=E_id)

            # employee = get_object_or_404(Employee, E_id=E_id).all()
            # print("after employees list",employees)
            names=[]
            for employee in employees:
                employee.delete()
                names.append(employee.first_name)
                # print("after employees deletion")
            return JsonResponse({"deleted":names,"message":"Deleted the emp successfully"},status=204)
        except Exception as e:
            # print("in exception while deleting",e)
            return JsonResponse({"error":f'Raised exception {e}'})
    else:
        print("in else method type list",e)
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

# -------------to know total number of employees----------------

def total_employees(request):
    try:
        total = Employee.objects.count()  # Count all employees
        current_month = datetime.now().strftime("%B")  # Get current month name, e.g., "November"
        return JsonResponse({"total": total, "month": current_month}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

# -------------to know new joined employee in current month----------------

def new_joiners(request):
    try:
        # Get the current month as a number (e.g., "11" for November)
        current_month = datetime.now().month

        # Filter employees who joined in the current month
        new_joiners_count = Employee.objects.filter(date_joined__month=current_month).count()

        # Get the current month name (e.g., "November")
        current_month_name = datetime.now().strftime("%B")

        return JsonResponse({"new_joiners": new_joiners_count, "month": current_month_name}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ------------------------to get user-details for profile -------------------

def employee_detail_for_profile(request):
    try:
        email_id = request.GET.get('emailid')  # Only consider email

        if not email_id:
            return JsonResponse({'error': 'Email not provided'}, status=400)

        # Fetch employee details based on email
        employee = get_object_or_404(Employee, email=email_id)

        # Prepare profile picture URL
        profile_picture_url = None
        if employee.profile_picture:
            # If the employee has a profile picture, construct the full URL
            profile_picture_url = settings.MEDIA_URL + str(employee.profile_picture)

        # Serialize employee details
        employee_data = {
            'E_id': employee.E_id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email,
            'phone_number': employee.phone_number,
            'age': employee.age,
            'gender': employee.gender,
            'Designation': employee.Designation,
            'department': employee.department,
            'date_of_birth': employee.date_of_birth,
            'date_joined': employee.date_joined,
            'profile_picture': profile_picture_url,  # Include profile picture URL
        }

        return JsonResponse(employee_data)

    except ObjectDoesNotExist:
        # Handle the case when no matching employee is found
        return JsonResponse({'error': 'Employee not found'}, status=404)

    except Exception as e:
        # Handle unexpected exceptions
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)


# ---------------------------allow loged-in user to edit some details----------

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
import json
from .decorators import *


@csrf_exempt
def update_employee_details_byLoginUser(request):
    if request.method == 'GET':
        # Fetch user details
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        employee = Employee.objects.filter(email=email).first()
        if not employee:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        return JsonResponse({
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'phone_number': employee.phone_number,
            'age': employee.age,
            'date_of_birth': employee.date_of_birth.isoformat() if employee.date_of_birth else None,
            'profile_picture': employee.profile_picture.url if employee.profile_picture and employee.profile_picture.name else None,
        })

    elif request.method == 'POST':
        # Update user details
        try:
            email = request.POST.get('email')
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)

            employee = Employee.objects.filter(email=email).first()
            if not employee:
                return JsonResponse({'error': 'Employee not found'}, status=404)

            # Update allowed fields
            employee.first_name = request.POST.get('first_name', employee.first_name)
            employee.last_name = request.POST.get('last_name', employee.last_name)
            employee.phone_number = request.POST.get('phone_number', employee.phone_number)
            employee.age = request.POST.get('age', employee.age)
            employee.date_of_birth = request.POST.get('date_of_birth', employee.date_of_birth)

            # Handle profile picture
            if 'profile_picture' in request.FILES:
                employee.profile_picture = request.FILES['profile_picture']

            employee.save()
            return JsonResponse({'message': 'Employee details updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
def verify_email_and_send_otp(request):
    # Initialize variables
    email = None

    # Handle JSON payload
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body)
            email = data.get("email")
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)

    # Handle form-data payload
    elif request.content_type == "application/x-www-form-urlencoded" or request.content_type.startswith("multipart/form-data"):
        email = request.POST.get("email")

    else:
        return JsonResponse({"status": "error", "message": "Unsupported content type. Use JSON or form-data."}, status=400)

    if not email:
        return JsonResponse({"status": "error", "message": "Email is required."}, status=400)

    # Check if email exists in Employee table
    try:
        employee = Employee.objects.get(email=email)
        print(employee.E_id)
        print(employee)
    except Employee.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User does not exist."}, status=404)

    # Generate a 6-digit OTP
    otp = get_random_string(length=6, allowed_chars='0123456789')

    # Save the OTP and its creation time
    login_details, created = LoginDetails.objects.get_or_create(employee_id=employee.E_id)
    login_details.otp_code = otp
    login_details.otp_created_at = timezone.now()
    login_details.save()

    # Send the OTP to the email
    try:
        send_mail(
            subject="Confirmation OTP UGyan",
            message=f"A sign in attempt requires further verification because we did not recognize your device.\nTo complete the sign in, enter the verification code on the unrecognized device. \n\n Verification code : {otp}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Failed to send OTP. Error: {e}"}, status=500)

    return JsonResponse({"status": "success", "message": "OTP has been sent to your email."}, status=200)


@csrf_exempt
def verify_otp(request):
    # Initialize variables
    email = None
    otp = None

    # Handle JSON payload
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            otp = data.get("otp")
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)

    # Handle form-data payload
    elif request.content_type == "application/x-www-form-urlencoded" or request.content_type.startswith("multipart/form-data"):
        email = request.POST.get("email")
        otp = request.POST.get("otp")
    else:
        return JsonResponse({"status": "error", "message": "Unsupported content type. Use JSON or form-data."}, status=400)

    if not email or not otp:
        return JsonResponse({"status": "error", "message": "Email and OTP are required."}, status=400)

    try:
        employee = Employee.objects.get(email=email)
        login_details = LoginDetails.objects.get(employee_id=employee.id)
    except (Employee.DoesNotExist, LoginDetails.DoesNotExist):
        return JsonResponse({"status": "error", "message": "User or login details not found."}, status=404)

    # Check if the OTP matches and is valid
    time_diff = timezone.now() - login_details.otp_created_at
    otp_valid_duration = 300  # 5 minutes
    if login_details.otp_code == otp and time_diff.total_seconds() < otp_valid_duration:
        # OTP is valid, so mark it as verified and update the details
        login_details.otp_verified = True  # Mark OTP as verified
        login_details.save()  # Save changes to the database

        return JsonResponse({"status": "success", "message": "OTP verified successfully."}, status=200)
    elif time_diff.total_seconds() >= otp_valid_duration:
        return JsonResponse({"status": "error", "message": "OTP has expired. Please request a new OTP."}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid OTP."}, status=400)

    
    
 
@csrf_exempt
def resend_otp(request):
    # Check for valid content type
    if request.content_type != "application/json":
        return JsonResponse({"status": "error", "message": "Unsupported content type. Use JSON."}, status=400)

    try:
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse({"status": "error", "message": "Email is required."}, status=400)

        # Validate if the email exists
        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User with this email does not exist."}, status=404)

        # Generate new OTP
        new_otp = generate_otp()  # Call your OTP generation logic
        login_details, created = LoginDetails.objects.get_or_create(employee_id=employee.id)
        login_details.otp_code = new_otp
        login_details.otp_created_at = timezone.now()
        login_details.otp_verified = False
        logger.info("Before save: %s", vars(login_details))
        login_details.save()
        logger.info("After save: %s", vars(login_details))

        # Send the new OTP to the user's email
        try:
            send_otp_email(email, new_otp)  # Call your email sending logic
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Failed to send email: {str(e)}"}, status=500)

        return JsonResponse({"status": "success", "message": "A new OTP has been sent to your email."}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    """Send the OTP to the user's email."""
    from django.core.mail import send_mail
    subject = "Another Attempt of OTP UGyan"
    message = f"A sign in attempt requires further verification because we did not recognize your device.\nTo complete the sign in, enter the verification code on the unrecognized device. \n\n Verification code :{otp}"
    from_email = settings.EMAIL_HOST_USER  # Replace with your sender email
    send_mail(subject, message, from_email, [email])



@csrf_exempt
def change_password(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Invalid request method. Use POST."}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        otp = data.get("otp")
        new_password = data.get("new_password")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)

    if not email or not otp or not new_password:
        return JsonResponse({"status": "error", "message": "Email, OTP, and new password are required."}, status=400)

    try:
        employee = Employee.objects.get(email=email)
    except Employee.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User not found."}, status=404)

    try:
        login_details = LoginDetails.objects.get(employee_id=employee.id)
    except LoginDetails.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Login details not found."}, status=404)

    otp_valid_duration = 300  # 5 minutes in seconds
    time_diff = timezone.now() - login_details.otp_created_at

    if login_details.otp_code != otp:
        return JsonResponse({"status": "error", "message": "Invalid OTP."}, status=400)

    if time_diff.total_seconds() > otp_valid_duration:
        return JsonResponse({"status": "error", "message": "OTP expired."}, status=400)

    try:
        # Encrypt the new password and save it in the Employee model
        employee.password = make_password(new_password)
        employee.save()

        # Update the login details
        login_details.change_password_attempts += 1
        login_details.change_password_attempts_date = timezone.now()

        expiration_time=timezone.now()+timedelta(seconds=otp_valid_duration)
        login_details.otp_expiration_time=expiration_time
        login_details.save()

        return JsonResponse({"status": "success", "message": "Password updated successfully."}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Failed to reset password. Please try again."}, status=500)


# ----------------------login--------------------------
from .decorators import *


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Invalid request method. Use POST."}, status=405)

    # Parse JSON input
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)

    # Validate username and password
    if not username or not password:
        return JsonResponse({"status": "error", "message": "Username and password are required."}, status=400)

    try:
        # Assuming username is the email field
        employee = Employee.objects.get(email=username)
    except Employee.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invalid username or password."}, status=401)

    # Check password
    if check_password(password, employee.password):
        # Determine role
        role = None
        if employee.is_emp:
            role = 'employee'
        elif employee.is_HR:
            role = 'HR'
        elif employee.is_admin:
            role = 'admin'

        # Store user data in session
        request.session['is_logged_in'] = True
        request.session['user_id'] = employee.E_id
        request.session['user_role'] = 'employee' if employee.is_emp else 'HR' if employee.is_HR else 'admin'

        user_data = {
            "id": employee.E_id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "role": role,
        }

        logger.info(f"Login successful: {username} - Role: {role}")
        
        return JsonResponse({"status": "success", "message": "Login successful.", "data": user_data}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid username or password."}, status=401)