# from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TipoDocumentoSerializer
from api.models import TipoDocumento

# Create your views here.


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
