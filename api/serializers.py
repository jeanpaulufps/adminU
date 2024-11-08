from rest_framework import serializers
from api import models

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode


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
        fields = ['horaInicio', 'horaFin', 'dia', 'materia', 'grupo', 'aula']

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
        fields = '__all__'
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


class PasswordResetSerializer(serializers.Serializer):
    correoInstitucional = serializers.EmailField()

    def validate_correoInstitucional(self, value):
        """
        Validar si el correo institucional existe en los modelos Estudiante o Profesor.
        """
        try:
            # Intentamos buscar el correo en Estudiante
            user = models.Estudiante.objects.get(correoInstitucional=value)
        except models.Estudiante.DoesNotExist:
            try:
                # Intentamos buscar el correo en Profesor
                user = models.Profesor.objects.get(correoInstitucional=value)
            except models.Profesor.DoesNotExist:
                raise serializers.ValidationError(
                    "No existe un usuario con este correo institucional."
                )
        self.user = user
        return value

    def save(self):
        """
        Enviar el correo de recuperación con el enlace de restablecimiento de contraseña.
        """
        user = self.user
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = token_generator.make_token(user)

        # Crear el enlace de recuperación
        # reset_url = f"http://{get_current_site(self.context['request']).domain}/api/password_reset/confirm?uid={uid}&token={token}"
        reset_url = f"http://localhost:5173/reset-password?uid={uid}&token={token}"

        # Enviar el correo de recuperación
        email_subject = 'Recuperación de contraseña'
        email_body = render_to_string(
            'password_reset_email.html',
            {
                'user': user,
                'reset_url': reset_url,
            },
        )
        send_mail(
            subject=email_subject,
            message='',
            html_message=email_body,
            from_email='admin@tusitio.com',  # Cambia este correo por el de tu administración
            recipient_list=[user.correoInstitucional],
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        """
        Validar si el token es válido y si el enlace es correcto.
        """
        try:
            # Decodificar el UID para obtener el ID del usuario
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = models.Estudiante.objects.get(pk=uid)
        except (TypeError, ValueError, models.Estudiante.DoesNotExist):
            try:
                user = models.Profesor.objects.get(pk=uid)
            except models.Profesor.DoesNotExist:
                raise serializers.ValidationError(
                    "El enlace de recuperación es inválido."
                )

        # Validar el token
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("El token de recuperación es inválido.")

        self.user = user
        return data

    def save(self):
        """
        Restablecer la contraseña del usuario.
        """
        user = self.user
        password = self.validated_data['new_password']
        user.set_password(password)  # Establecer la nueva contraseña encriptada
        user.save()
