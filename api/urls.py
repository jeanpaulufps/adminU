from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'tipos-documento', views.TipoDocumentoViewSet)
router.register(r'pensums', views.PensumViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
