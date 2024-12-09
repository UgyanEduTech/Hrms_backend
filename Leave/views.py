from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now
from .decorators import *

# Create a new leave request

@csrf_exempt
def create_leave_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        leave_type = data.get('leave_type', 'CASUAL')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        email = data.get('email')
        reason = data.get('reason')
        status = data.get('status','Pending')

        leave_request = LeaveRequest.objects.create(
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            email=email,
            reason=reason,
            status=status
        )
        return JsonResponse({
            "id": leave_request.id,
            "message": "Leave request created successfully."
        })

    return JsonResponse({"error": "Invalid method."}, status=400)

# Retrieve a specific leave request

def leave_request_detail(request):
    # Retrieve pk from query parameters
    pk = request.GET.get('pk')
    if not pk:
        return JsonResponse({"error": "Missing pk parameter"}, status=400)

    # Fetch the LeaveRequest object using pk
    leave_request = get_object_or_404(LeaveRequest, pk=pk)

    # Return the leave request details as a JSON response
    return JsonResponse({
        "id": leave_request.id,
        "leave_type": leave_request.leave_type,
        "start_date": leave_request.start_date,
        "end_date": leave_request.end_date,
        "email": leave_request.email,
        "reason": leave_request.reason,
        "status": leave_request.status,
        "created_at": leave_request.created_at,
        "updated_at": leave_request.updated_at
    })

# Update an existing leave request

@csrf_exempt
def update_leave_request(request, id):
    # Fetch the LeaveRequest object using the id parameter
    leave_request = get_object_or_404(LeaveRequest, pk=id)

    if request.method == 'GET':
        # Return the leave request data as JSON
        return JsonResponse({
            "id": leave_request.id,
            "leave_type": leave_request.leave_type,
            "start_date": leave_request.start_date,
            "end_date": leave_request.end_date,
            "email": leave_request.email,
            "reason": leave_request.reason,
            "status":leave_request.status
        }, encoder=DjangoJSONEncoder, safe=False)

    if request.method == 'POST':  # Or use 'PUT'/'PATCH' if preferred
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

        # Update fields with provided values or retain the current ones
        leave_request.leave_type = data.get('leave_type', leave_request.leave_type)
        leave_request.start_date = data.get('start_date', leave_request.start_date)
        leave_request.end_date = data.get('end_date', leave_request.end_date)
        leave_request.email = data.get('email', leave_request.email)
        leave_request.reason = data.get('reason', leave_request.reason)
        leave_request.status = data.get('status', leave_request.status)
        leave_request.save()

        return JsonResponse({
            "id": leave_request.id,
            "message": "Leave request updated successfully."
        })

    return JsonResponse({"error": "Invalid method."}, status=405)

# Delete a leave request

@csrf_exempt
def delete_leave_request(request, id):
    """
    Delete a leave request by ID.
    """
    leave_request = get_object_or_404(LeaveRequest, pk=id)

    if request.method in ['DELETE', 'GET']:  # Allow GET for testing purposes
        leave_request.delete()
        return JsonResponse({"message": "Leave request deleted successfully."})

    return JsonResponse({"error": "Invalid method."}, status=400)


# List all leave requests

def leave_request_list(request):
    leave_requests = LeaveRequest.objects.all()
    data = serialize('json', leave_requests)
    return JsonResponse({'leave_requests': data})

def get_leave_requests(request):
    """
    Fetch all leave requests from the database and return them as JSON.
    """
    leave_requests = LeaveRequest.objects.all()
    # Use serializers to convert QuerySet to JSON
    data = [
        {
            "id": leave.id,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "email": leave.email,
            "reason": leave.reason,
            "status": leave.status,
            "created_at": leave.created_at,
            "updated_at": leave.updated_at,
        }
        for leave in leave_requests
    ]
    return JsonResponse(data, safe=False)



@csrf_exempt
def approve_leave(request):
    if request.method == "POST":
        data = json.loads(request.body)
        leave_id = data.get("id")
        try:
            leave_request = LeaveRequest.objects.get(id=leave_id)
            leave_request.status = "Approved"
            leave_request.save()
            return JsonResponse({"message": "Leave approved successfully."}, status=200)
        except LeaveRequest.DoesNotExist:
            return JsonResponse({"error": "Leave request not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def deny_leave(request):
    if request.method == "POST":
        data = json.loads(request.body)
        leave_id = data.get("id")
        try:
            leave_request = LeaveRequest.objects.get(id=leave_id)
            leave_request.status = "Denied"
            leave_request.save()
            return JsonResponse({"message": "Leave denied successfully."}, status=200)
        except LeaveRequest.DoesNotExist:
            return JsonResponse({"error": "Leave request not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)



def get_leave_count(request):
    # Get the current date
    current_date = now().date()

    # Filter leaves where status is "Approved" and the current date falls within the leave range
    leave_count = LeaveRequest.objects.filter(
        status='Approved',
        start_date__lte=current_date,
        end_date__gte=current_date
    ).count()

    # Return the count as JSON response
    return JsonResponse({'leave_count': leave_count})


@csrf_exempt
def add_leave_balance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract data from request
            E_id = data.get("E_id")
            total_sick_leave = data.get("total_sick_leave", 0)
            total_casual_leave = data.get("total_casual_leave", 0)
            taken_sick_leave = data.get("taken_sick_leave", 0)
            taken_casual_leave = data.get("taken_casual_leave", 0)

            if not E_id:
                return JsonResponse({"message": "Employee ID is required."}, status=400)

            # Create or update the record
            leave_balance, created = LeaveBalance.objects.get_or_create(E_id=E_id)
            leave_balance.total_sick_leave = total_sick_leave
            leave_balance.total_casual_leave = total_casual_leave
            leave_balance.taken_sick_leave = taken_sick_leave
            leave_balance.taken_casual_leave = taken_casual_leave

            # Calculate and update the differences
            difference_sick, difference_casual = calculate_leave_differences(
                total_sick_leave, taken_sick_leave, total_casual_leave, taken_casual_leave
            )
            leave_balance.difference_sick = difference_sick
            leave_balance.difference_casual = difference_casual

            # Save the updated data
            leave_balance.save()

            message = "Leave balance added successfully." if created else "Leave balance updated successfully."
            return JsonResponse({"message": message, "difference_sick": difference_sick, "difference_casual": difference_casual}, status=200)

        except Exception as e:
            return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=400)



def calculate_leave_differences(total_sick_leave, taken_sick_leave, total_casual_leave, taken_casual_leave):

    difference_sick = total_sick_leave - taken_sick_leave
    difference_casual = total_casual_leave - taken_casual_leave

    return max(difference_sick, 0), max(difference_casual, 0)  # Ensure no negative values



def get_leave_balances(request):
    if request.method == "GET":
        leave_balances = LeaveBalance.objects.all().values(
            'E_id',
            'total_sick_leave',
            'total_casual_leave',
            'taken_sick_leave',
            'taken_casual_leave',
            'difference_sick',
            'difference_casual',
            'others'
        )
        return JsonResponse(list(leave_balances), safe=False)
    return JsonResponse({"message": "Invalid request method"}, status=400)