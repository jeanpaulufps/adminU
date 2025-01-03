from django.contrib import admin
from api.models import (
    Pensum,
    Departamento,
    Profesor,
    Horario,
    Carrera,
    HorarioAsesoria,
    Estudiante,
    Materia,
    Grupo,
    Nota,
    Semestre,
    TipoDocumento,
    Aula,
    Publicacion,
    Foro,
    Comentario,
)
from django.contrib.auth.hashers import make_password
from django import forms

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


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and not password.startswith("pbkdf2_"):
            return make_password(password)
        return password


class EstudianteAdmin(admin.ModelAdmin):
    form = EstudianteForm
    list_display = ['codigo', 'nombres', 'apellidos', 'correoInstitucional']
    search_fields = ['nombres', 'apellidos', 'codigo']
    inlines = [NotaInline]


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1
    # fields = ['grupo', 'horaInicio', 'horaFin', 'dia', 'aula']
    fields = ['horaInicio', 'horaFin', 'dia', 'aula']
    ordering = ['dia', 'horaInicio']


class HorarioAsesoriaInline(admin.TabularInline):
    model = HorarioAsesoria
    extra = 1


class MateriaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre',
        'creditos',
        "codigo",
        "intensidadHoraria",
    ]

    inlines = [HorarioInline, HorarioAsesoriaInline]


class HorarioAdmin(admin.ModelAdmin):
    # list_display = ['materia', 'grupo', 'dia', 'horaInicio', 'horaFin', 'aula']
    list_display = ['materia', 'dia', 'horaInicio', 'horaFin', 'aula']
    list_filter = ['dia', 'materia']
    # search_fields = ['materia__nombre', 'grupo', 'aula__nombre']
    search_fields = ['materia__nombre', 'aula__nombre']


class HorarioAsesoriaAdmin(admin.ModelAdmin):
    list_display = ("materia", "dia", "hora_inicio", "hora_fin", "lugar")
    list_filter = ("dia", "materia")


admin.site.register(HorarioAsesoria, HorarioAsesoriaAdmin)
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
admin.site.register(Publicacion)
admin.site.register(Foro)
admin.site.register(Comentario)
