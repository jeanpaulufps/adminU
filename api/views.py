# from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import (
    TipoDocumentoSerializer,
    PensumSerializer,
    DepartamentoSerializer,
    ProfesorSerializer,
    HorarioSerializer,
    CarreraSerializer,
    MateriaSerializer,
    EstudianteSerializer,
    NotaSerializer,
    SemestreSerializer,
    GrupoSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    EstudianteMateriasSerializer,
)
from rest_framework.views import APIView
from .models import Estudiante, Profesor
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# from rest_framework.permissions import IsAuthenticated


from api import models

# Create your views here.


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            codigo = serializer.validated_data['codigo']
            numero_documento = serializer.validated_data['numeroDocumento']
            password = serializer.validated_data['password']

            # Buscar al estudiante o profesor
            usuario = (
                Estudiante.objects.filter(
                    codigo=codigo, numeroDocumento=numero_documento
                ).first()
                or Profesor.objects.filter(
                    codigo=codigo, numeroDocumento=numero_documento
                ).first()
            )

            if usuario and usuario.check_password(password):
                # Serializar el objeto de usuario
                if isinstance(usuario, Estudiante):
                    usuario_serializado = EstudianteSerializer(usuario).data
                else:
                    usuario_serializado = ProfesorSerializer(usuario).data

                return Response(
                    {'message': 'Login exitoso', 'usuario': usuario_serializado},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {'error': 'Credenciales inválidas'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = models.TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer


class PensumViewSet(viewsets.ModelViewSet):
    queryset = models.Pensum.objects.all()
    serializer_class = PensumSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = models.Profesor.objects.all()
    serializer_class = ProfesorSerializer


class HorarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Horario.objects.all()
    serializer_class = HorarioSerializer


class CarreraViewSet(viewsets.ModelViewSet):
    queryset = models.Carrera.objects.all()
    serializer_class = CarreraSerializer


class MateriaViewSet(viewsets.ModelViewSet):
    queryset = models.Materia.objects.all()
    serializer_class = MateriaSerializer


class EstudianteMateriasView(generics.RetrieveAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteMateriasSerializer
    # permission_classes = [IsAuthenticated]  # Ajusta los permisos según tus necesidades

    def get_object(self):
        estudiante_id = self.kwargs['pk']
        return Estudiante.objects.get(id=estudiante_id)

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = models.Estudiante.objects.all()
    serializer_class = EstudianteSerializer


class GrupoViewSet(viewsets.ModelViewSet):
    queryset = models.Grupo.objects.all()
    serializer_class = GrupoSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = models.Departamento.objects.all()
    serializer_class = DepartamentoSerializer


class NotaViewSet(viewsets.ModelViewSet):
    queryset = models.Nota.objects.all()
    serializer_class = NotaSerializer


class SemestreViewSet(viewsets.ModelViewSet):
    queryset = models.Semestre.objects.all()
    serializer_class = SemestreSerializer


class PasswordResetView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Te hemos enviado un enlace para restablecer tu contraseña."
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    Endpoint para confirmar el restablecimiento de la contraseña.
    """

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contraseña restablecida exitosamente."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
