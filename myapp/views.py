# from django.shortcuts import render
from django.http import JsonResponse
from myapp.models import Estudiante
from django.forms.models import model_to_dict
from .models import Estudiante

# Create your views here.


def get_estudiantes(request):
    estudiantes = Estudiante.objects.all().values()
    return JsonResponse(list(estudiantes), safe=False)


def get_estudiante_por_id(request, estudiante_id):
    try:
        estudiante = Estudiante.objects.get(id=estudiante_id)
        return JsonResponse(model_to_dict(estudiante))
    except Estudiante.DoesNotExist:
        return JsonResponse({'error': 'Estudiante no encontrado'}, status=404)
