from django.urls import path
from . import views

urlpatterns = [
    path("api/estudiantes", views.get_estudiantes),
    path('api/estudiantes/<int:estudiante_id>/', views.get_estudiante_por_id),
]
