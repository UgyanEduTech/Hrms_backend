from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import *
from datetime import timedelta
from django.utils.timezone import now,timedelta
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from datetime import datetime
from .decorators import *
from calendar import monthrange

# Set up logging
logger = logging.getLogger(__name__)


@csrf_exempt
def clock_in_view(request):
    if request.method != 'POST':
        return JsonResponse({"status": "failed", "message": "Only POST method is allowed."}, status=405)

    try:
        # Parse the JSON body
        body = json.loads(request.body)
        E_id = body.get('E_id')

        # Check if E_id is provided
        if not E_id:
            return JsonResponse({"status": "failed", "message": "Employee ID (E_id) is required."}, status=400)

        print(f"Employee ID in Clock-in: {E_id}")

        # Get or create ClockInOut object for today
        clock_entry, created = ClockInOut.objects.get_or_create(
            E_id=E_id,
            date=timezone.now().date()
        )

        if created or clock_entry.login_time is None:
            # First time clock-in for the day
            clock_entry.login_time = timezone.now()
            clock_entry.shift_end_time = clock_entry.login_time + timedelta(hours=8)
            clock_entry.logout_time = None
            clock_entry.login_attempts += 1
            clock_entry.save()

            return JsonResponse({
                "status": "success",
                "message": "Clock-in successful.",
                "login_time": clock_entry.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                "shift_end_time": clock_entry.shift_end_time.strftime('%Y-%m-%d %H:%M:%S'),
                "login_attempts": clock_entry.login_attempts,
            }, status=200)

        else:
            # Already clocked in today
            if not clock_entry.shift_end_time:
                # Ensure shift_end_time is set if missing
                clock_entry.shift_end_time = clock_entry.login_time + timedelta(hours=8)

            clock_entry.login_attempts += 1
            clock_entry.save()

            return JsonResponse({
                "status": "info",
                "message": "Already clocked in today.",
                "login_time": clock_entry.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                "shift_end_time": clock_entry.shift_end_time.strftime('%Y-%m-%d %H:%M:%S'),
                "login_attempts": clock_entry.login_attempts,
            }, status=200)

    except Exception as e:
        print(f"Error during clock-in: {e}")
        return JsonResponse({"status": "failed", "message": f"An error occurred during clock-in. Error: {str(e)}"}, status=500)


@csrf_exempt
def clock_out_view(request):
    if request.method != 'POST':
        return JsonResponse({"status": "failed", "message": "Only POST method is allowed."}, status=405)

    try:
        # Parse the JSON body
        body = json.loads(request.body)
        E_id = body.get('E_id')

        # Check if E_id is provided
        if not E_id:
            return JsonResponse({"status": "failed", "message": "Employee ID (E_id) is required."}, status=400)

        # Try to get the ClockInOut object for today
        clock_entry = ClockInOut.objects.filter(E_id=E_id, date=now().date()).first()
        if not clock_entry:
            return JsonResponse({"status": "failed", "message": "No clock-in entry found for today."}, status=200)

        # Check if the employee has already checked out
        if clock_entry.logout_time:
            return JsonResponse({
                "status": "success",
                "message": "Already checked out today.",
                "logout_time": clock_entry.logout_time.strftime('%Y-%m-%d %H:%M:%S')
            }, status=200)

        # Check if the employee clocked in today
        if not clock_entry.login_time:
            return JsonResponse({"status": "success", "message": "Cannot check out without clocking in first."}, status=200)

        # Enforce minimum working hours restriction
        required_working_time = timedelta(hours=8)
        actual_working_time = now() - clock_entry.login_time
        remaining_time = required_working_time - actual_working_time

        if actual_working_time < required_working_time:
            # Calculate the expected logout time
            expected_logout_time = clock_entry.login_time + required_working_time
            return JsonResponse({
                "status": "success",
                "message": f"Cannot log out yet. You need to work {remaining_time} more to complete your working hours.",
                "logout_time": expected_logout_time.strftime('%Y-%m-%d %H:%M:%S')
            }, status=200)

        # If 8 hours have passed, record the logout time automatically
        clock_entry.logout_time = now()
        clock_entry.save()

        return JsonResponse({
            "status": "success",
            "message": "Logout successful.",
            "logout_time": clock_entry.logout_time.strftime('%Y-%m-%d %H:%M:%S')
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"status": "failed", "message": "Invalid JSON format."}, status=400)
    except Exception as e:
        print(f"Error during clock-out: {e}")
        return JsonResponse({"status": "failed", "message": "An error occurred during clock-out."}, status=500)


@csrf_exempt
def reset_login_attempts_view(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Only POST method is allowed."}, status=405)
    
    try:
        # Parse the JSON body
        print(f"Request body: {request.body}")  # Log raw request body for debugging
        body = json.loads(request.body)
        
        employee_id = body.get('E_id')  # Retrieve E_id from the request body
        print(f"Employee ID: {employee_id}")  # Log E_id to see if it's coming correctly
        
        # Check if E_id is provided
        if not employee_id:
            return JsonResponse({"status": "error", "message": "Employee ID (E_id) is required."}, status=400)
        
        # Get or create a ClockInOut entry for today
        today = timezone.now().date()
        clock_entry, created = ClockInOut.objects.get_or_create(E_id=employee_id, date=today)
        
        # Check if the reset attempts limit has been reached
        if clock_entry.reset_attempts >= 3:
            return JsonResponse({
                "status": "error",
                "message": "Reset attempts limit reached for today. Only 3 resets are allowed per day.",
            }, status=403)

        # Reset login attempts and increment reset attempts count
        clock_entry.login_attempts = 0
        clock_entry.reset_attempts += 1
        clock_entry.save()

        return JsonResponse({
            "status": "success",
            "message": "Login attempts have been reset.",
            "remaining_resets": 3 - clock_entry.reset_attempts,
            "reset_attempts_used": clock_entry.reset_attempts
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)
    except Exception as e:
        print(f"Error during reset: {e}")
        return JsonResponse({"status": "error", "message": "An error occurred during reset."}, status=500)
    



@csrf_exempt
def get_clock_in_out_data(request):
    if request.method == 'POST':
        try:
            # Load data from the body of the request
            data = json.loads(request.body)
            E_id = data.get('E_id')  # Use 'E_id' as the key in the JSON body
            
            # Ensure 'E_id' is provided
            if not E_id:
                return JsonResponse({'error': 'E_id is required'}, status=400)

            # Get the current date to filter data for the current month
            current_date = timezone.now()
            start_of_month = current_date.replace(day=1)

            # Calculate the last day of the current month
            last_day_of_month = monthrange(current_date.year, current_date.month)[1]
            end_of_month = current_date.replace(day=last_day_of_month)

            # Query clock-in/out data for the employee within the current month
            clock_data = ClockInOut.objects.filter(
                E_id=E_id,  # Directly filter by 'E_id' field in ClockInOut
                date__gte=start_of_month.date(),
                date__lte=end_of_month.date()
            )

            # Prepare data to send as JSON
            response_data = []
            for record in clock_data:
                response_data.append({
                    'date': record.date,
                    'login_time': record.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'logout_time': record.logout_time.strftime('%Y-%m-%d %H:%M:%S') if record.logout_time else '',
                    'shift_end_time': record.shift_end_time.strftime('%Y-%m-%d %H:%M:%S') if record.shift_end_time else '',
                    'login_attempts': record.login_attempts,
                    'reset_attempts': record.reset_attempts,
                })

            return JsonResponse(response_data, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)






def timer_view(request):
    employee_id = request.GET.get('id')
    
    # Fetch today's clock entry for the employee
    clock_entry = get_object_or_404(ClockInOut, E_id=employee_id, date=timezone.now().date())
    
    # Check if the employee has clocked in
    if not clock_entry.login_time:
        return JsonResponse({"status": "failed", "message": "Clock-in not recorded for today."})
    
    # Calculate remaining time
    now = timezone.now()
    if clock_entry.shift_end_time and now < clock_entry.shift_end_time:
        remaining_time = clock_entry.shift_end_time - now
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        remaining_time_str = f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"
    else:
        remaining_time_str = "Shift complete!"

    return JsonResponse({
        "status": "success",
        "remaining_time": remaining_time_str,
        "shift_end_time": clock_entry.shift_end_time
    })


def check_reminders_view(request):
    current_time = timezone.now()
    reminder_5_min = timedelta(minutes=5)  # 5 minutes before expected logout

    reminder_message = None  # To store the reminder message, not a list

    # Fetch today's active clock-in entries without logout time
    clock_entries = ClockInOut.objects.filter(
        date=current_time.date(),
        logout_time__isnull=True
    )

    for entry in clock_entries:
        if entry.login_time:
            # Set a very short required working time for testing, e.g., 36 seconds (0.01 hours)
            required_working_time = timedelta(hours=8)
            expected_logout_time = entry.login_time + required_working_time
            time_remaining = expected_logout_time - current_time

            # Check for the 5-minute reminder
            if time_remaining <= reminder_5_min and not entry.reminder_5_min_sent:
                reminder_message = {
                    "employee_id": entry.E_id,
                    "message": f"Reminder for Employee {entry.E_id}, only 5 minutes are left for logout."
                }
                entry.reminder_5_min_sent = True
                entry.save()

                break  # Exit loop once reminder is triggered for the employee

    if reminder_message:
        return JsonResponse({
            "status": "success",
            "message": "Reminders checked.",
            "reminder": reminder_message  # Return the reminder as a single dictionary
        })
    else:
        return JsonResponse({
            "status": "success",
            "message": "No reminders triggered."
        })



def reset_reminders_view(request):
    employee_id = request.GET.get('id')  # Get the employee ID from the query parameters

    if not employee_id:
        return JsonResponse({"status": "failed", "message": "Employee ID is required."})

    # Get today's clock entry for the specified employee without a logout time
    clock_entry = ClockInOut.objects.filter(
        E_id=employee_id, 
        date=timezone.now().date(),
        logout_time__isnull=True
    ).first()

    if not clock_entry:
        return JsonResponse({"status": "failed", "message": "No active clock-in entry found for this employee today."})

    # Reset reminder flags for this entry
    clock_entry.reminder_5_min_sent = False
    clock_entry.save()

    return JsonResponse({"status": "success", "message": f"Reminder flags reset for employee {employee_id}."})



# -----------this view function is for text-messages which is in dashboard--------------




@csrf_exempt
def save_message(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            text = data.get('message')

            if text:
                timestamp = datetime.now()
                # Create and save the message
                message = Message.objects.create(text=text, timestamp=timestamp)
                # Return the saved message with formatted timestamp
                return JsonResponse({
                    'message': message.text,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')  # 12-hour format
                })
            else:
                return JsonResponse({'error': 'Message text is required'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def get_messages(request):
    one_month_ago = datetime.now() - timedelta(days=30)
    messages = Message.objects.filter(timestamp__gte=one_month_ago).order_by('-timestamp')  # Order by timestamp descending
    message_list = []
    
    for msg in messages:
        message_list.append({
            'text': msg.text,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %I:%M:%S %p')  # Format in 12-hour format
        })
    return JsonResponse({'messages': message_list})



@csrf_exempt
def add_monthly_target(request):
    if request.method == "POST":
        emp_id = request.GET.get('emp_ID')
        try:
            data = json.loads(request.body.decode("utf-8"))
            month = data.get("month")
            year = data.get("year")
            target_value = data.get("target_value", 0.0)
            actual_value = data.get("actual_value", 0.0)
            status = data.get("status", "Pending")
            difference = int(target_value) -int(actual_value)

            if not month or not year or not target_value or not actual_value:
                return JsonResponse({"status": "error", "message": "Missing required fields."}, status=400)

            monthly_target = MonthlyTarget.objects.create(
                emp_id=emp_id,
                month=month,
                year=year,
                target_value=target_value,
                actual_value=actual_value,
                difference=difference,
                status=status
            )
            return JsonResponse({"status": "success", "message": "Monthly target added successfully."}, status=201)

        except Exception as e:
            print("exec in add target",e)
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

# Update a monthly target
@csrf_exempt
def update_monthly_target(request):
    if request.method == "PUT":
        emp_id = request.GET.get('emp_ID')
        try:
            print("inside try")
            data = json.loads(request.body.decode("utf-8"))
            # Fetch the target using empId instead of target_id
            target = MonthlyTarget.objects.get(emp_id=emp_id)

            # Update the target fields
            target.target_value = data.get("target_value", target.target_value)
            target.actual_value = data.get("actual_value", target.actual_value)
            target.difference = int(target.target_value) - int(target.actual_value)
            target.save()

            return JsonResponse({"status": "success", "message": "Monthly target updated successfully."}, status=200)

        except MonthlyTarget.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Target not found."}, status=404)
        except Exception as e:
            print("exec in updatre target",e)
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

# Reset targets on the 1st of each month
def reset_monthly_targets():
    current_month = now().strftime("%B")
    current_year = now().year
    MonthlyTarget.objects.filter(month=current_month, year=current_year).update(
        target_value=0, actual_value=0, difference=0, status="Pending"
    )


@csrf_exempt
def get_monthly_target(request):
    current_month = now().strftime("%B")  # Full month name (e.g., "December")
    current_year = now().year

    # Log all query parameters
    logger.info(f"Request query parameters: {request.GET}")

    # Fetch the emp_id using the correct query parameter name
    emp_id = request.GET.get("empId")  # Match the front-end parameter name
    logger.info(f"Fetching target for emp_id={emp_id}, month={current_month}, year={current_year}")

    try:
        # Use __iexact for case-insensitive comparison
        target = MonthlyTarget.objects.get(month__iexact=current_month, year=current_year, emp_id=emp_id)
        logger.info(f"Target found: {target}")
        return JsonResponse({
            "target_id": target.target_id,
            "month": target.month,
            "year": target.year,
            "target_value": target.target_value,
            "actual_value": target.actual_value,
            "difference": target.difference,
            "status": target.status
        })
    except MonthlyTarget.DoesNotExist:
        logger.warning(f"No target found for emp_id={emp_id}, month={current_month}, year={current_year}")
        return JsonResponse({"message": "No target found for this month."}, status=404)
