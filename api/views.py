# from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TipoDocumentoSerializer, PensumSerializer
from api.models import TipoDocumento, Pensum

# Create your views here.


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer


class PensumViewSet(viewsets.ModelViewSet):
    queryset = Pensum.objects.all()
    serializer_class = PensumSerializer
