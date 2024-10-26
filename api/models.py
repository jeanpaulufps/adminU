from django.db import models

# Create your models here.


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
    abreviacion = models.CharField(max_length=10)


# class Usuario(models.Model):
#     nombres = models.CharField(max_length=50, default=' ')
#     apellidos = models.CharField(max_length=50, default=' ')
#     codigo = models.CharField(max_length=50)
#     fechaNacimiento = models.DateField()
#     direccion = models.CharField(max_length=255)
#     telefono = models.CharField(max_length=20)
#     correoElectronico = models.CharField(max_length=50)
#     correoInstitucional = models.CharField(max_length=50)
#     fechaIngreso = models.DateField()
#     numeroDocumento = models.CharField(max_length=20)
#     tipoDocumento = models.ForeignKey(
#         TipoDocumento, on_delete=models.SET_NULL, null=True
#     )

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return f"{self.nombres} {self.apellidos}"


# class Pensum(models.Model):
#     nombre = models.CharField(max_length=100, default=' ')
#     pass


# class Departamento(models.Model):
#     nombre = models.CharField(max_length=100)


# class Profesor(Usuario):
#     pass


# class Horario(models.Model):
#     horaInicio = models.TimeField()
#     horaFin = models.TimeField()
#     dia = models.IntegerField()
#     aula = models.CharField(max_length=200)


# class Carrera(models.Model):
#     nombre = models.CharField(max_length=100)
#     codigo = models.CharField(max_length=20)
#     pensum = models.ForeignKey(
#         Pensum, on_delete=models.CASCADE, related_name="carreras"
#     )
#     semestres = models.IntegerField()
#     modalidad = models.IntegerField()
#     tipoCarrera = models.IntegerField()
#     departamento = models.ForeignKey(
#         Departamento, on_delete=models.CASCADE, related_name="carreras"
#     )


# class Materia(models.Model):
#     nombre = models.CharField(max_length=100)
#     codigo = models.CharField(max_length=20)
#     creditos = models.IntegerField()
#     intensidadHoraria = models.IntegerField()
#     requisito = models.ManyToManyField(
#         "self", symmetrical=False, related_name="materias_requisito", blank=True
#     )


# class Estudiante(Usuario):
#     materiasMatriculadas = models.ManyToManyField(
#         Materia, related_name="estudiantes_matriculados", null=True
#     )
#     carrera = models.ManyToManyField(Carrera, blank=False)
#     creditosAprobados = models.IntegerField()
#     estadoMatricula = models.IntegerField()


# class Grupo(models.Model):
#     codigo = models.CharField(max_length=20)
#     materia = models.ForeignKey(
#         Materia, on_delete=models.CASCADE, related_name="grupos"
#     )
#     profesores = models.ManyToManyField(Profesor, related_name="grupos")
#     horario = models.ForeignKey(
#         Horario, on_delete=models.CASCADE, related_name="grupos"
#     )


# class Nota(models.Model):
#     primera = models.FloatField()
#     segunda = models.FloatField()
#     tercera = models.FloatField()
#     cuarta = models.FloatField()
#     estudiante = models.ForeignKey(
#         Estudiante, on_delete=models.CASCADE, related_name="notas"
#     )
#     materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="notas")


# class Semestre(models.Model):
#     numeroSemestre = models.IntegerField()
#     pensum = models.ForeignKey(
#         Pensum, on_delete=models.CASCADE, related_name="semestres"
#     )
#     materias = models.ManyToManyField(Materia, related_name="semestres")
