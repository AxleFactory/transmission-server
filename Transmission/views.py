from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Assignment


@cache_page(60 * 15)  # cache view for 15 minutes
def assignments(request):
    active_contact_assignments = [a.get_json() for a in Assignment.objects.all().filter(active=True) if not a.expired]
    return JsonResponse(
        active_contact_assignments,
        safe=False,
        json_dumps_params={
            'separators': (',', ':')
        }
    )


def all_assignments(request):
    all_contact_assignments = [a.get_json() for a in Assignment.objects.all()]
    return JsonResponse(
        all_contact_assignments,
        safe=False,
        json_dumps_params={
            'indent': 4,
            'sort_keys': True,
        }
    )


def assignments_redirect(request):
    return redirect('assignments.json')
