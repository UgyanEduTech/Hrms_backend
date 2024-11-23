from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Holiday
import json

def get_holidays(request):
    holidays = Holiday.objects.all()
    holidays_data = [
        {
            'id': holiday.id,
            'name': holiday.name,
            'date': holiday.date.strftime('%Y-%m-%d'),
        }
        for holiday in holidays
    ]
    return JsonResponse(holidays_data, safe=False)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Holiday
import json

@csrf_exempt
def add_holiday(request):
    if request.method == 'POST':
        try:
            # Load the request body and extract the necessary fields
            data = json.loads(request.body)
            name = data.get('name')
            date = data.get('date')

            # Validate if both name and date are provided
            if name and date:
                # Ensure the date is in the correct format
                # Parse the date string to a Python datetime object
                holiday_date = datetime.strptime(date, '%Y-%m-%d').date()

                # Create the new holiday entry in the database
                holiday = Holiday.objects.create(name=name, date=holiday_date)

                # Return success response with the holiday details
                return JsonResponse({
                    'message': 'Holiday added successfully!',
                    'holiday': {
                        'id': holiday.id,
                        'name': holiday.name,
                        'date': holiday.date.strftime('%Y-%m-%d')  # Format date as 'YYYY-MM-DD'
                    }
                })
            else:
                return JsonResponse({'message': 'Invalid data, name and date are required.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'Invalid date format, should be YYYY-MM-DD'}, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Holiday
# import json

@csrf_exempt
def delete_holiday(request, holiday_id):  # Get the holiday_id from URL
    if request.method == 'DELETE':
        try:
            holiday = Holiday.objects.get(id=holiday_id)
            holiday.delete()
            return JsonResponse({'message': 'Holiday deleted successfully!'}, status=200)
        except Holiday.DoesNotExist:
            return JsonResponse({'error': 'Holiday not found!'}, status=404)
    return JsonResponse({'error': 'Invalid request method!'}, status=405)
