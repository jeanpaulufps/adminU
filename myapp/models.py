from django.db import models


# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=100)
    correoElectronico = models.CharField(max_length=100)
    correoInstitucional = models.CharField(max_length=100)
    fechaIngreso = models.DateField()
    numeroDocumento = models.CharField(max_length=32)
    tipoDocumento = models.CharField(max_length=10)

    class Meta:
        abstract = True  # Indica que es una clase abstracta


class Estudiante(Usuario):
    # materiasMatriculadas =                            #RELACION
    # carrera =
    creditosAprobados = models.IntegerField()
    estadoMatricula = models.IntegerField()


class Profesor(Usuario):
    materias = models.CharField(max_length=1)  # RELACION


class Nota(models.Model):
    primera = models.FloatField()
    segunda = models.FloatField()
    tercera = models.FloatField()
    cuarta = models.FloatField()
    # estudiante =                                           #RELACION
    # materia =                                              #RELACION


# class Departamento(models.Model):
