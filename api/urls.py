from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from .views import LoginView, PasswordResetView, PasswordResetConfirmView

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
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='api_password_reset'),
    # path(
    #     'password_reset/confirm/<uidb64>/<token>/',
    #     PasswordResetConfirmView.as_view(),
    #     name='api_password_reset_confirm',
    # ),
    path(
        'password_reset/confirm/',
        PasswordResetConfirmView.as_view(),
        name='api_password_reset_confirm',
    ),
]
