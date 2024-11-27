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


class ForoView(APIView):
    def get(self, request, materia_id, *args, **kwargs):
        try:
            foro = models.Foro.objects.get(materia_id=materia_id)
        except models.Foro.DoesNotExist:
            return Response(
                {"detail": "El foro de esta materia no existe."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = serializers.ForoSerializer(foro)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, materia_id, *args, **kwargs):
        try:
            materia = models.Materia.objects.get(id=materia_id)
        except models.Materia.DoesNotExist:
            return Response(
                {"detail": "Materia no encontrada."}, status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        data["materia"] = materia.id

        serializer = serializers.ForoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicacionView(APIView):
    def get(self, request, foro_id, *args, **kwargs):
        try:
            foro = models.Foro.objects.get(id=foro_id)
        except models.Foro.DoesNotExist:
            return Response(
                {"detail": "Foro no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        publicaciones = foro.publicaciones.all()
        serializer = serializers.PublicacionSerializer(publicaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, foro_id, *args, **kwargs):
        try:
            foro = models.Foro.objects.get(id=foro_id)
        except models.Foro.DoesNotExist:
            return Response(
                {"detail": "Foro no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        data["foro"] = foro.id
        data["estudiante"] = request.user.id

        serializer = serializers.PublicacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, publicacion_id, *args, **kwargs):
        try:
            publicacion = models.Publicacion.objects.get(id=publicacion_id)
        except models.Publicacion.DoesNotExist:
            return Response(
                {"detail": "Publicación no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if publicacion.estudiante != request.user:
            return Response(
                {"detail": "No tienes permiso para editar esta publicación."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = serializers.PublicacionSerializer(
            publicacion, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, publicacion_id, *args, **kwargs):
        try:
            publicacion = models.Publicacion.objects.get(id=publicacion_id)
        except models.Publicacion.DoesNotExist:
            return Response(
                {"detail": "Publicación no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if publicacion.estudiante != request.user:
            return Response(
                {"detail": "No tienes permiso para eliminar esta publicación."},
                status=status.HTTP_403_FORBIDDEN,
            )

        publicacion.delete()
        return Response(
            {"detail": "Publicación eliminada."}, status=status.HTTP_204_NO_CONTENT
        )


class ComentarioView(APIView):
    def post(self, request, publicacion_id, *args, **kwargs):
        try:
            publicacion = models.Publicacion.objects.get(id=publicacion_id)
        except models.Publicacion.DoesNotExist:
            return Response(
                {"detail": "Publicación no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data
        data["publicacion"] = publicacion.id
        data["estudiante"] = request.user.id

        serializer = serializers.ComentarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForosEstudianteView(APIView):
    def get(self, request, estudiante_id):
        try:
            estudiante = models.Estudiante.objects.get(id=estudiante_id)
            materias_ids = estudiante.materiasMatriculadas.values_list('id', flat=True)
            foros = models.Foro.objects.filter(materia__id__in=materias_ids)
            serializer = serializers.ForoSerializer(foros, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Estudiante.DoesNotExist:
            return Response(
                {"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


class PublicacionesForoView(APIView):
    def get(self, request, foro_id):
        try:
            foro = models.Foro.objects.get(id=foro_id)
            publicaciones = foro.publicaciones.all()
            serializer = serializers.PublicacionSerializer(publicaciones, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Foro.DoesNotExist:
            return Response(
                {"error": "Foro no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


class PublicacionComentariosView(APIView):
    def get(self, request, publicacion_id):
        try:
            publicacion = models.Publicacion.objects.get(id=publicacion_id)
            serializer = serializers.PublicacionComentariosSerializer(publicacion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Publicacion.DoesNotExist:
            return Response(
                {"error": "Publicación no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )


class CrearComentarioView(APIView):
    def post(self, request):
        serializer = serializers.CrearComentarioSerializer(data=request.data)

        if serializer.is_valid():

            publicacion_id = serializer.validated_data.get("publicacion").id
            estudiante_id = serializer.validated_data.get("estudiante").id

            try:
                publicacion = models.Publicacion.objects.get(id=publicacion_id)
                estudiante = models.Estudiante.objects.get(id=estudiante_id)
            except (models.Publicacion.DoesNotExist, models.Estudiante.DoesNotExist):
                return Response(
                    {"error": "Publicación o estudiante no encontrados"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            comentario = serializer.save()
            return Response(
                {"message": "Comentario creado exitosamente", "id": comentario.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrearComentarioView(APIView):
    def post(self, request):
        serializer = serializers.CrearComentarioSerializer(data=request.data)

        if serializer.is_valid():
            publicacion_id = serializer.validated_data.get("publicacion").id
            estudiante_id = serializer.validated_data.get("estudiante").id

            try:
                models.Publicacion.objects.get(id=publicacion_id)
                models.Estudiante.objects.get(id=estudiante_id)
            except (models.Publicacion.DoesNotExist, models.Estudiante.DoesNotExist):
                return Response(
                    {"error": "Publicación o estudiante no encontrados"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            comentario = serializer.save()

            respuesta_serializer = serializers.ComentarioRespuestaSerializer(comentario)
            return Response(respuesta_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrearPublicacionView(APIView):
    def post(self, request):
        serializer = serializers.CrearPublicacionSerializer(data=request.data)

        if serializer.is_valid():
            foro_id = serializer.validated_data.get("foro").id
            estudiante_id = serializer.validated_data.get("estudiante").id

            try:
                models.Foro.objects.get(id=foro_id)
                models.Estudiante.objects.get(id=estudiante_id)
            except (models.Foro.DoesNotExist, models.Estudiante.DoesNotExist):
                return Response(
                    {"error": "Foro o estudiante no encontrados"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            publicacion = serializer.save()

            respuesta_serializer = serializers.PublicacionRespuestaSerializer(
                publicacion
            )
            return Response(respuesta_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MateriasConHorariosView(APIView):
    def get(self, request, estudiante_id):
        try:
            estudiante = models.Estudiante.objects.get(id=estudiante_id)
        except models.Estudiante.DoesNotExist:
            return Response(
                {"error": "Estudiante no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        materias = estudiante.materiasMatriculadas.all()

        serializer = serializers.MateriaConHorariosSerializer(materias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EventoView(APIView):
    def get(self, request, *args, **kwargs):
        eventos = models.Evento.objects.all().order_by("fecha_inicio")
        serializer = serializers.EventoSerializer(eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = serializers.EventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventoDetailView(APIView):
    def get(self, request, evento_id, *args, **kwargs):
        try:
            evento = models.Evento.objects.get(id=evento_id)
        except models.Evento.DoesNotExist:
            return Response({"detail": "Evento no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.EventoSerializer(evento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, evento_id, *args, **kwargs):
        try:
            evento = models.Evento.objects.get(id=evento_id)
        except models.Evento.DoesNotExist:
            return Response({"detail": "Evento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.EventoSerializer(evento, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, evento_id, *args, **kwargs):
        try:
            evento = models.Evento.objects.get(id=evento_id)
        except models.Evento.DoesNotExist:
            return Response({"detail": "Evento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        evento.delete()
        return Response({"detail": "Evento eliminado con éxito."}, status=status.HTTP_204_NO_CONTENT)