from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'tipos-documento', views.TipoDocumentoViewSet)
router.register(r'pensums', views.PensumViewSet)
router.register(r'departamentos', views.DepartamentoViewSet)
router.register(r'profesores', views.ProfesorViewSet)
router.register(r'horarios', views.HorarioViewSet)
router.register(r'carreras', views.CarreraViewSet)
router.register(r'materias', views.MateriaViewSet)
router.register(r'estudiantes', views.EstudianteViewSet)
router.register(r'grupos', views.GrupoViewSet)
router.register(r'notas', views.NotaViewSet)
router.register(r'semestres', views.SemestreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
