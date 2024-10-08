from django.contrib import admin
from myapp.models import (
    Pensum,
    Departamento,
    Profesor,
    Horario,
    Carrera,
    Estudiante,
    Materia,
    Grupo,
    Nota,
    Semestre,
)

# from myapp import models

# Register your models here.

admin.site.register(Pensum)
admin.site.register(Departamento)
admin.site.register(Profesor)
admin.site.register(Horario)
admin.site.register(Carrera)
admin.site.register(Estudiante)
admin.site.register(Materia)
admin.site.register(Grupo)
admin.site.register(Nota)
admin.site.register(Semestre)
