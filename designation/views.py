from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Designation
from django.db.models import Q

 # Only if you want to bypass CSRF token validation (for testing purposes)
@csrf_exempt  
def add_designation(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract data from the request (use get() to handle missing fields)
            E_id=data.get('E_id')
            name = data.get('name')
            designation = data.get('designation')
            department = data.get('department')
            reports_to = data.get('reports_to')  # This will now be a string

            # Create a new Designation instance
            new_designation = Designation.objects.create(
                E_id=E_id,
                name=name,
                designation=designation,
                department=department,
                reports_to=reports_to
            )

            # Return a success JSON response with the newly created object details
            response_data = {
                'status': 'success',
                'message': 'Designation created successfully',
                'data': {
                    'E_id': new_designation.E_id,
                    'name': new_designation.name,
                    'designation': new_designation.designation,
                    'department': new_designation.department,
                    'reports_to': new_designation.reports_to
                }
            }

            return JsonResponse(response_data, status=201)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_designation(request):
    
    if request.method == "DELETE":
        try:
            # Parse the request body
            body = json.loads(request.body)
            e_id = body.get("E_id")

            if not e_id:
                return JsonResponse(
                    {"error": "E_id is required in the request body."},
                    status=400
                )

            # Retrieve the designation by E_id
            designation = Designation.objects.get(E_id=e_id)

            # Delete the record
            designation.delete()

            return JsonResponse(
                {"message": "Designation deleted successfully."},
                status=200
            )
        except Designation.DoesNotExist:
            return JsonResponse(
                {"error": "Designation not found for the given E_id."},
                status=404
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON in request body."},
                status=400
            )
    else:
        return JsonResponse(
            {"error": "Invalid request method. Only DELETE is allowed."},
            status=405
        )


# ------------------floor-managers-------------------------------------------------------------------
@csrf_exempt
def get_floormanagers(request):
    # Filter designations case-insensitively for "floormanager"
    floormanagers = Designation.objects.filter(designation__icontains="Floor-Manager")
    data = list(floormanagers.values("E_id", "name", "designation", "department", "reports_to"))
    return JsonResponse(data, safe=False)

#----------------------get vertical-managers---------------------------------------------------------


def get_vertical_managers_byId(request):
    e_id = request.GET.get('e_id')
    print(e_id)
    # Filter designations where `reports_to` matches the given `e_id`
    vertical_managers = Designation.objects.filter(reports_to=e_id)
    print("vertical managers -",vertical_managers)
    data = list(vertical_managers.values("E_id", "name", "designation", "department", "reports_to"))
    return JsonResponse(data, safe=False)

#-------------------------get team-leaders by id-----------------------------------------------------------

def get_team_leaders_byId(request):
    e_id = request.GET.get('e_id')
    print(e_id)
    # Filter designations where `reports_to` matches the given `e_id` (vertical manager's ID)
    team_leaders = Designation.objects.filter(reports_to=e_id)
    data = list(team_leaders.values("E_id", "name", "designation", "department", "reports_to"))
    print("data -",data)
    return JsonResponse(data, safe=False)

#-------------------------get vertical managers---------------------------------------------------------------

@csrf_exempt
def get_verticalmanagers(request):
    # Filter designations case-insensitively for "floormanager"
    vmanagers = Designation.objects.filter(designation__icontains="vertical-manager")
    data = list(vmanagers.values("E_id", "name", "designation", "department", "reports_to"))
    return JsonResponse(data, safe=False)

#----------------------------get-teamleader-------------------------------------------------------------------

@csrf_exempt
def get_team_lead(request):
    # Filter designations containing "team-leader" but not "assistant-team-leader"
    team_leaders = Designation.objects.filter(
        Q(designation__icontains="team-leader") & ~Q(designation__icontains="assistant-team-leader")
    )
    data = list(team_leaders.values("E_id", "name", "designation", "department", "reports_to"))
    return JsonResponse(data, safe=False)


#------------------------------------get atl by ID------------------------------------------------

def get_Atl_byId(request):
    e_id = request.GET.get('e_id')
    print(e_id)
    Atl = Designation.objects.filter(reports_to=e_id)
    data = list(Atl.values("E_id", "name", "designation", "department", "reports_to"))
    print("data -",data)
    return JsonResponse(data, safe=False)

#-------------------------------------------------------------------------------
@csrf_exempt
def get_Atls(request):
    # Filter designations containing "team-leader" but not "assistant-team-leader"
    team_leaders = Designation.objects.filter(
        Q(designation__icontains="assistant-team-leader")
    )
    data = list(team_leaders.values("E_id", "name", "designation", "department", "reports_to"))
    return JsonResponse(data, safe=False)
#----------------------------------------------------------------------------
def get_bda_byId(request):
    e_id = request.GET.get('e_id')
    print(e_id)
    bda = Designation.objects.filter(reports_to=e_id)
    data = list(bda.values("E_id", "name", "designation", "department", "reports_to"))
    print("data -",data)
    return JsonResponse(data, safe=False)

def get_ceo(request):
        ceo=Designation.objects.filter(designation__icontains="ceo")
        data=list(ceo.values("E_id","name","designation"))
        return JsonResponse(data,safe=False)

def get_cto(request):
    cto = Designation.objects.filter(designation__icontains="cto")
    data = list(cto.values("E_id", "name", "designation"))
    return JsonResponse(data, safe=False)

def get_coo(request):
    coo = Designation.objects.filter(designation__icontains="coo")
    data = list(coo.values("E_id", "name", "designation"))
    return JsonResponse(data, safe=False)

def get_cfo(request):
    cfo = Designation.objects.filter(designation__icontains="cfo")
    data = list(cfo.values("E_id", "name", "designation"))
    return JsonResponse(data, safe=False)


#-----------------------------------------------------------------------

@csrf_exempt
def get_BDA(request):
    # Filter designations containing "team-leader" but not "assistant-team-leader"
    BDA = Designation.objects.filter(
        Q(designation__icontains="bussiness-development-associate") 
    )
    data = list(BDA.values("E_id", "name", "designation", "department", "reports_to"))
    return JsonResponse(data, safe=False)