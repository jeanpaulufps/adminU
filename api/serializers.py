from rest_framework import serializers
from .models import (
    TipoDocumento,
    Pensum,
    Carrera,
    Departamento,
    Estudiante,
    Grupo,
    Horario,
    Materia,
    Nota,
    Profesor,
    Usuario,
    Semestre,
)


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'


class PensumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pensum
        fields = '__all__'
