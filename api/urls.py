from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from .views import (
    CrearPublicacionView,
    CrearComentarioView,
    LoginView,
    PublicacionesForoView,
    PublicacionComentariosView,
    PasswordResetView,
    PasswordResetConfirmView,
    EstudianteHorarioView,
    CrearHorarioView,
    GestionMateriasView,
    MateriasNoMatriculadasView,
    MateriasMatriculadasView,
    ForoView,
    PublicacionView,
    ComentarioView,
    PublicacionView,
    ForosEstudianteView,
    PublicacionComentariosView,
    MateriasConHorariosView,
)

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
    path(
        'password_reset/confirm/',
        PasswordResetConfirmView.as_view(),
        name='api_password_reset_confirm',
    ),
    path(
        'estudiantes/<int:pk>/materias/',
        views.EstudianteMateriasView.as_view(),
        name='estudiante-materias',
    ),
    path(
        'estudiantes/<int:pk>/horario/',
        EstudianteHorarioView.as_view(),
        name='estudiante-horario',
    ),
    path('horarios/', CrearHorarioView.as_view(), name='crear-horario'),
    path(
        'incluir-cancelar-materias/',
        GestionMateriasView.as_view(),
        name='gestion-materias',
    ),
    path(
        'estudiantes/<int:estudiante_id>/materias/no-matriculadas/',
        MateriasNoMatriculadasView.as_view(),
        name='materias-no-matriculadas',
    ),
    path(
        'estudiantes/<int:estudiante_id>/materias/matriculadas/',
        MateriasMatriculadasView.as_view(),
        name='materias-matriculadas',
    ),
    path('materias/<int:materia_id>/foro/', ForoView.as_view(), name='foro'),
    path(
        'foros/<int:foro_id>/publicaciones/',
        PublicacionView.as_view(),
        name='publicaciones',
    ),
    path(
        'publicaciones/<int:publicacion_id>/comentarios/',
        ComentarioView.as_view(),
        name='comentarios',
    ),
    path(
        'publicaciones/<int:publicacion_id>/',
        PublicacionView.as_view(),
        name='publicacion-detail',
    ),
    path(
        'foros-estudiante/<int:estudiante_id>/',
        ForosEstudianteView.as_view(),
        name='foros-estudiante',
    ),
    path(
        'publicaciones-foro/<int:foro_id>/',
        PublicacionesForoView.as_view(),
        name='publicaciones-por-foro',
    ),
    path(
        'publicacion/<int:publicacion_id>/',
        PublicacionComentariosView.as_view(),
        name='publicacion-con-comentarios',
    ),
    path('crear-comentario/', CrearComentarioView.as_view(), name='crear-comentario'),
    path(
        'crear-publicacion/', CrearPublicacionView.as_view(), name='crear-publicacion'
    ),
    path(
        'estudiantes/<int:estudiante_id>/materias-con-horarios/',
        MateriasConHorariosView.as_view(),
        name='materias-con-horarios',
    ),
    path('eventos/', views.EventoView.as_view(), name='eventos'),
    path('eventos/<int:evento_id>/', views.EventoDetailView.as_view(), name='evento-detail'),
]
