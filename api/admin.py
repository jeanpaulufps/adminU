from django.contrib import admin
from api.models import (
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
    TipoDocumento,
    Aula,
)

# from api import models
# Register your models here.


class NotaAdmin(admin.ModelAdmin):
    list_display = [
        'estudiante',
        'materia',
        'primera',
        'segunda',
        'tercera',
        'cuarta',
        'promedio',
    ]
    # search_fields = ['estudiante__nombres', 'materia__nombre']
    # list_filter = ['materia']
    # autocomplete_fields = ['estudiante', 'materia']

    def promedio(self, obj):
        primera = obj.primera or 0
        segunda = obj.segunda or 0
        tercera = obj.tercera or 0
        cuarta = obj.cuarta or 0
        return (primera + segunda + tercera + cuarta) / 4

    promedio.short_description = 'Promedio'


class NotaInline(admin.TabularInline):
    model = Nota
    extra = 1  # Número de formularios extra en blanco
    fields = ['materia', 'primera', 'segunda', 'tercera', 'cuarta', 'promedio']
    readonly_fields = ['promedio']

    def promedio(self, obj):
        primera = obj.primera or 0
        segunda = obj.segunda or 0
        tercera = obj.tercera or 0
        cuarta = obj.cuarta or 0
        return (primera + segunda + tercera + cuarta) / 4

    promedio.short_description = 'Promedio'


class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombres', 'apellidos', 'correoInstitucional']
    search_fields = ['nombres', 'apellidos', 'codigo']
    inlines = [NotaInline]


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1
    # fields = ['grupo', 'horaInicio', 'horaFin', 'dia', 'aula']
    fields = ['horaInicio', 'horaFin', 'dia', 'aula']
    ordering = ['dia', 'horaInicio']


class MateriaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre',
        'creditos',
    ]
    inlines = [HorarioInline]


class HorarioAdmin(admin.ModelAdmin):
    # list_display = ['materia', 'grupo', 'dia', 'horaInicio', 'horaFin', 'aula']
    list_display = ['materia', 'dia', 'horaInicio', 'horaFin', 'aula']
    list_filter = ['dia', 'materia']
    # search_fields = ['materia__nombre', 'grupo', 'aula__nombre']
    search_fields = ['materia__nombre', 'aula__nombre']


admin.site.register(Materia, MateriaAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Nota, NotaAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(TipoDocumento)
admin.site.register(Pensum)
admin.site.register(Departamento)
admin.site.register(Profesor)
admin.site.register(Carrera)
admin.site.register(Grupo)
admin.site.register(Semestre)
admin.site.register(Aula)
