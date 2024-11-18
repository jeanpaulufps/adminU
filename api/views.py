# from django.shortcuts import render
from rest_framework import viewsets
from api import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# from rest_framework.permissions import IsAuthenticated
from api import models

# Create your views here.


class MateriasNoMatriculadasView(APIView):
    def get(self, request, estudiante_id, *args, **kwargs):
        try:
            estudiante = models.Estudiante.objects.get(id=estudiante_id)
        except models.Estudiante.DoesNotExist:
            return Response(
                {"detail": "El estudiante no existe."},
                status=status.HTTP_404_NOT_FOUND,
            )

        todas_materias = models.Materia.objects.all()
        materias_matriculadas = estudiante.materiasMatriculadas.all()
        materias_no_matriculadas = todas_materias.difference(materias_matriculadas)

        serializer = serializers.MateriaSerializer(materias_no_matriculadas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MateriasMatriculadasView(APIView):
    def get(self, request, estudiante_id, *args, **kwargs):
        try:
            estudiante = models.Estudiante.objects.get(id=estudiante_id)
        except models.Estudiante.DoesNotExist:
            return Response(
                {"detail": "El estudiante no existe."},
                status=status.HTTP_404_NOT_FOUND,
            )

        materias_matriculadas = estudiante.materiasMatriculadas.all()
        serializer = serializers.MateriaSerializer(materias_matriculadas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GestionMateriasView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.IncluirCancelarMateriaSerializer(data=request.data)
        if serializer.is_valid():
            estudiante = serializer.validated_data['estudiante']
            materia = serializer.validated_data['materia']

            if materia in estudiante.materiasMatriculadas.all():
                return Response(
                    {"detail": "La materia ya está incluida."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            estudiante.materiasMatriculadas.add(materia)
            return Response(
                {"detail": f"Materia '{materia.nombre}' incluida exitosamente."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        serializer = serializers.IncluirCancelarMateriaSerializer(data=request.data)
        if serializer.is_valid():
            estudiante = serializer.validated_data['estudiante']
            materia = serializer.validated_data['materia']

            if materia not in estudiante.materiasMatriculadas.all():
                return Response(
                    {"detail": "La materia no está incluida."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            estudiante.materiasMatriculadas.remove(materia)
            return Response(
                {"detail": f"Materia '{materia.nombre}' cancelada exitosamente."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrearHorarioView(generics.CreateAPIView):
    queryset = models.Horario.objects.all()
    serializer_class = serializers.HorarioCreateSerializer


class EstudianteHorarioView(generics.RetrieveAPIView):
    queryset = models.Estudiante.objects.all()
    serializer_class = serializers.EstudianteHorarioSerializer
    # permission_classes = [IsAuthenticated]


class LoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            codigo = serializer.validated_data['codigo']
            numero_documento = serializer.validated_data['numeroDocumento']
            password = serializer.validated_data['password']

            usuario = (
                models.Estudiante.objects.filter(
                    codigo=codigo, numeroDocumento=numero_documento
                ).first()
                or models.Profesor.objects.filter(
                    codigo=codigo, numeroDocumento=numero_documento
                ).first()
            )

            if usuario and usuario.check_password(password):

                if isinstance(usuario, models.Estudiante):
                    usuario_serializado = serializers.EstudianteSerializer(usuario).data
                else:
                    usuario_serializado = serializers.ProfesorSerializer(usuario).data

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
    serializer_class = serializers.TipoDocumentoSerializer


class PensumViewSet(viewsets.ModelViewSet):
    queryset = models.Pensum.objects.all()
    serializer_class = serializers.PensumSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = models.Profesor.objects.all()
    serializer_class = serializers.ProfesorSerializer


class HorarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Horario.objects.all()
    serializer_class = serializers.HorarioSerializer


class CarreraViewSet(viewsets.ModelViewSet):
    queryset = models.Carrera.objects.all()
    serializer_class = serializers.CarreraSerializer


class MateriaViewSet(viewsets.ModelViewSet):
    queryset = models.Materia.objects.all()
    serializer_class = serializers.MateriaSerializer


class EstudianteMateriasView(generics.RetrieveAPIView):
    queryset = models.Estudiante.objects.all()
    serializer_class = serializers.EstudianteMateriasSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        estudiante_id = self.kwargs['pk']
        return models.Estudiante.objects.get(id=estudiante_id)


class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = models.Estudiante.objects.all()
    serializer_class = serializers.EstudianteSerializer


class GrupoViewSet(viewsets.ModelViewSet):
    queryset = models.Grupo.objects.all()
    serializer_class = serializers.GrupoSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = models.Departamento.objects.all()
    serializer_class = serializers.DepartamentoSerializer


class NotaViewSet(viewsets.ModelViewSet):
    queryset = models.Nota.objects.all()
    serializer_class = serializers.NotaSerializer


class SemestreViewSet(viewsets.ModelViewSet):
    queryset = models.Semestre.objects.all()
    serializer_class = serializers.SemestreSerializer


class PasswordResetView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = serializers.PasswordResetSerializer(
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

    def post(self, request, *args, **kwargs):
        serializer = serializers.PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contraseña restablecida exitosamente."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
