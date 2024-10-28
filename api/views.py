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
)
from api import models

# Create your views here.


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = models.TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer


class PensumViewSet(viewsets.ModelViewSet):
    queryset = models.Pensum.objects.all()
    serializer_class = PensumSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = models.Profesor.objects.all()
    serializer_class = ProfesorSerializer


class HorarioViewSet(viewsets.ModelViewSet):
    queryset = models.Horario.objects.all()
    serializer_class = HorarioSerializer


class CarreraViewSet(viewsets.ModelViewSet):
    queryset = models.Carrera.objects.all()
    serializer_class = CarreraSerializer


class MateriaViewSet(viewsets.ModelViewSet):
    queryset = models.Materia.objects.all()
    serializer_class = MateriaSerializer


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
