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
)

# from api import models

# Register your models here.

admin.site.register(TipoDocumento)
admin.site.register(Pensum)
admin.site.register(Departamento)
admin.site.register(Profesor)
admin.site.register(Horario)
admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Grupo)
admin.site.register(Semestre)


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


admin.site.register(Nota, NotaAdmin)


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


admin.site.register(Estudiante, EstudianteAdmin)
