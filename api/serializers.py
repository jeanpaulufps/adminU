from rest_framework import serializers
from api import models

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode


class IncluirCancelarMateriaSerializer(serializers.Serializer):
    estudiante_id = serializers.IntegerField()
    materia_id = serializers.IntegerField()

    def validate(self, data):
        estudiante_id = data.get('estudiante_id')
        materia_id = data.get('materia_id')

        try:
            estudiante = models.Estudiante.objects.get(id=estudiante_id)
            data['estudiante'] = estudiante
        except models.Estudiante.DoesNotExist:
            raise serializers.ValidationError("El estudiante no existe.")

        try:
            materia = models.Materia.objects.get(id=materia_id)
            data['materia'] = materia
        except models.Materia.DoesNotExist:
            raise serializers.ValidationError("La materia no existe.")

        return data


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
    materia = serializers.CharField(source="materia.nombre")
    aula = serializers.CharField(source="aula.codigo", default=None)

    dia_nombre = serializers.SerializerMethodField()

    class Meta:
        model = models.Horario
        fields = ["materia", "horaInicio", "horaFin", "dia", "dia_nombre", "aula"]

    def get_dia_nombre(self, obj):
        dias = {
            1: "Lunes",
            2: "Martes",
            3: "Miércoles",
            4: "Jueves",
            5: "Viernes",
            6: "Sábado",
            7: "Domingo",
        }
        return dias.get(obj.dia, "Desconocido")


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Carrera
        fields = '__all__'


class MateriaHorarioSerializer(serializers.ModelSerializer):
    horarios = HorarioSerializer(many=True)

    class Meta:
        model = models.Materia
        fields = '__all__'


class HorarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Horario
        fields = ['materia', 'horaInicio', 'horaFin', 'dia', 'aula']


class EstudianteHorarioSerializer(serializers.ModelSerializer):
    materias_matriculadas = MateriaHorarioSerializer(
        many=True, source='materiasMatriculadas'
    )

    class Meta:
        model = models.Estudiante
        fields = ['id', 'materias_matriculadas']


class MateriaSerializer(serializers.ModelSerializer):
    notas = serializers.SerializerMethodField()
    horarios = HorarioSerializer(many=True, read_only=True)

    class Meta:
        model = models.Materia
        fields = '__all__'

    def get_notas(self, obj):

        estudiante = self.context.get('estudiante')
        notas = models.Nota.objects.filter(materia=obj, estudiante=estudiante)
        return NotaSerializer(notas, many=True).data


class EstudianteMateriasSerializer(serializers.ModelSerializer):

    materiasMatriculadas = serializers.SerializerMethodField()

    class Meta:
        model = models.Estudiante
        fields = ['materiasMatriculadas']

    def get_materiasMatriculadas(self, obj):
        materias = obj.materiasMatriculadas.all()
        return MateriaSerializer(materias, many=True, context={'estudiante': obj}).data


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Estudiante
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        estudiante = models.Estudiante(**validated_data)
        estudiante.set_password(validated_data['password'])
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
    promedio = serializers.SerializerMethodField()

    class Meta:
        model = models.Nota
        fields = ['primera', 'segunda', 'tercera', 'cuarta', 'promedio']

    def get_promedio(self, obj):
        return (obj.primera + obj.segunda + obj.tercera + obj.cuarta) / 4


class SemestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Semestre
        fields = '__all__'


class PasswordResetSerializer(serializers.Serializer):
    correoInstitucional = serializers.EmailField()

    def validate_correoInstitucional(self, value):

        try:

            user = models.Estudiante.objects.get(correoInstitucional=value)
        except models.Estudiante.DoesNotExist:
            try:

                user = models.Profesor.objects.get(correoInstitucional=value)
            except models.Profesor.DoesNotExist:
                raise serializers.ValidationError(
                    "No existe un usuario con este correo institucional."
                )
        self.user = user
        return value

    def save(self):

        user = self.user
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = token_generator.make_token(user)

        # reset_url = f"http://{get_current_site(self.context['request']).domain}/api/password_reset/confirm?uid={uid}&token={token}"
        reset_url = f"http://localhost:5173/reset-password?uid={uid}&token={token}"

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
            from_email='admin@tusitio.com',
            recipient_list=[user.correoInstitucional],
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):

        try:

            uid = urlsafe_base64_decode(data['uid']).decode()
            user = models.Estudiante.objects.get(pk=uid)
        except (TypeError, ValueError, models.Estudiante.DoesNotExist):
            try:
                user = models.Profesor.objects.get(pk=uid)
            except models.Profesor.DoesNotExist:
                raise serializers.ValidationError(
                    "El enlace de recuperación es inválido."
                )

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("El token de recuperación es inválido.")

        self.user = user
        return data

    def save(self):

        user = self.user
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()


class ComentarioSerializer(serializers.ModelSerializer):
    estudiante = serializers.CharField(source="estudiante.nombres")

    class Meta:
        model = models.Comentario
        fields = '__all__'


class PublicacionSerializer(serializers.ModelSerializer):
    estudiante = serializers.CharField(source="estudiante.nombres")
    # comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = models.Publicacion
        fields = '__all__'


class ForoSerializer(serializers.ModelSerializer):
    materia = serializers.CharField(source="materia.nombre")
    # publicaciones = PublicacionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Foro
        fields = '__all__'


class PublicacionComentariosSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source="estudiante.nombres", read_only=True)
    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = models.Publicacion
        fields = [
            "id",
            "titulo",
            "contenido",
            "fecha_creacion",
            "fecha_actualizacion",
            "estudiante_nombre",
            "comentarios",  # Incluye los comentarios relacionados
        ]