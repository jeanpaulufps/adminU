from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
    abreviacion = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    nombres = models.CharField(max_length=50, default=' ')
    apellidos = models.CharField(max_length=50, default=' ')
    password = models.CharField(max_length=128, null=False, default=' ')
    codigo = models.CharField(max_length=50)
    fechaNacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    correoElectronico = models.CharField(max_length=50)
    correoInstitucional = models.CharField(max_length=50)
    fechaIngreso = models.DateField()
    numeroDocumento = models.CharField(max_length=20)
    tipoDocumento = models.ForeignKey(
        TipoDocumento, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.codigo} - {self.nombres} {self.apellidos}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Encriptar la contraseña

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Pensum(models.Model):
    nombre = models.CharField(max_length=100, default=' ')
    pass

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Profesor(Usuario):
    pass


class Aula(models.Model):
    codigo = models.CharField(max_length=20)
    estado = models.IntegerField()

    def __self__(self):
        return self.codigo


class Horario(models.Model):
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    dia = models.IntegerField()
    aula = models.ForeignKey(
        Aula, on_delete=models.SET_NULL, related_name="aula", null=True
    )

    def __str__(self):
        return (
            f"Día: {self.dia} ({self.horaInicio} - {self.horaFin}), aula: {self.aula}"
        )


class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    pensum = models.ForeignKey(
        Pensum, on_delete=models.CASCADE, related_name="carreras"
    )
    semestres = models.IntegerField()
    modalidad = models.IntegerField()
    tipoCarrera = models.IntegerField()
    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE, related_name="carreras"
    )

    def __self__(self):
        return f"{self.codigo} - {self.nombre}"


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    creditos = models.IntegerField()
    intensidadHoraria = models.IntegerField()
    requisito = models.ManyToManyField(
        "self", symmetrical=False, related_name="materias_requisito", blank=True
    )

    def __self__(self):
        return f"{self.codigo} - {self.nombre}"


class Estudiante(Usuario):
    materiasMatriculadas = models.ManyToManyField(
        Materia, related_name="estudiantes_matriculados", null=True
    )
    carrera = models.ManyToManyField(Carrera, blank=False)
    creditosAprobados = models.IntegerField()
    estadoMatricula = models.IntegerField()


class Grupo(models.Model):
    codigo = models.CharField(max_length=20)
    materia = models.ForeignKey(
        Materia, on_delete=models.CASCADE, related_name="grupos"
    )
    profesores = models.ManyToManyField(Profesor, related_name="grupos")
    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, related_name="grupos"
    )

    def __self__(self):
        return f"{self.materia}, codigo: {self.codigo}"


class Nota(models.Model):
    primera = models.FloatField()
    segunda = models.FloatField()
    tercera = models.FloatField()
    cuarta = models.FloatField()
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, related_name="notas"
    )
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="notas")


class Semestre(models.Model):
    numeroSemestre = models.IntegerField()
    pensum = models.ForeignKey(
        Pensum, on_delete=models.CASCADE, related_name="semestres"
    )
    materias = models.ManyToManyField(Materia, related_name="semestres")

    def __self__(self):
        return self.numeroSemestre
