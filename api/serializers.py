from rest_framework import serializers
from api import models


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoDocumento
        fields = '__all__'


class PensumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pensum
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Departamento
        fields = '__all__'


class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profesor
        fields = '__all__'


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Horario
        fields = '__all__'


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Carrera
        fields = '__all__'


class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Materia
        fields = '__all__'


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Estudiante
        fields = [
            'nombres',
            'apellidos',
            'codigo',
            'fechaNacimiento',
            'direccion',
            'telefono',
            'correoElectronico',
            'correoInstitucional',
            'fechaIngreso',
            'numeroDocumento',
            'tipoDocumento',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }  # Asegúrate de que la contraseña no se devuelva

    def create(self, validated_data):
        estudiante = models.Estudiante(**validated_data)
        estudiante.set_password(validated_data['password'])  # Encriptar la contraseña
        estudiante.save()
        return estudiante


class LoginSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    numeroDocumento = serializers.CharField()
    password = serializers.CharField()


class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grupo
        fields = '__all__'


class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nota
        fields = '__all__'


class SemestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Semestre
        fields = '__all__'
