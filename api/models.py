from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

# Create your models here.


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
    abreviacion = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class UsuarioManager(BaseUserManager):
    def create_user(self, correoInstitucional, password=None, **extra_fields):

        if not correoInstitucional:
            raise ValueError("El correo institucional debe ser proporcionado.")
        user = self.model(correoInstitucional=correoInstitucional, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correoInstitucional, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correoInstitucional, password, **extra_fields)


class Usuario(AbstractBaseUser):
    nombres = models.CharField(max_length=50, default=' ')
    apellidos = models.CharField(max_length=50, default=' ')
    password = models.CharField(max_length=128, null=False, default=' ')
    image = models.CharField(
        max_length=255, null=False, default='https://loremflickr.com/400/400'
    )
    codigo = models.CharField(max_length=50)
    fechaNacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    correoElectronico = models.CharField(max_length=50, unique=True)
    correoInstitucional = models.CharField(max_length=50, unique=True)
    fechaIngreso = models.DateField()
    numeroDocumento = models.CharField(max_length=20)
    tipoDocumento = models.ForeignKey(
        TipoDocumento, on_delete=models.SET_NULL, null=True
    )

    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correoInstitucional'
    REQUIRED_FIELDS = [
        'nombres',
        'apellidos',
        'codigo',
        'fechaNacimiento',
    ]

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.codigo} - {self.nombres} {self.apellidos}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_email_field_name(self):
        return 'correoInstitucional'


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

    def __str__(self):
        return self.codigo


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

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    creditos = models.IntegerField()
    intensidadHoraria = models.IntegerField()
    requisito = models.ManyToManyField(
        "self", symmetrical=False, related_name="materias_requisito", blank=True
    )

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Estudiante(Usuario):
    materiasMatriculadas = models.ManyToManyField(
        Materia, related_name="estudiantes_matriculados", blank=True
    )
    # carrera = models.ManyToManyField(Carrera, blank=False)
    creditosAprobados = models.IntegerField()
    estadoMatricula = models.IntegerField()


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

    def __str__(self):
        return self.numeroSemestre


class Horario(models.Model):
    DIA_CHOICES = [
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]

    materia = models.ForeignKey(
        Materia, on_delete=models.CASCADE, related_name="horarios"
    )
    # grupo = models.CharField(max_length=20)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    dia = models.IntegerField(choices=DIA_CHOICES)
    aula = models.ForeignKey(
        Aula, on_delete=models.SET_NULL, related_name="horarios", null=True
    )

    def save(self, *args, **kwargs):
        if self.horaInicio >= self.horaFin:
            raise ValueError("La hora de inicio debe ser anterior a la hora de fin.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.materia.nombre} (Día: {self.dia} ({self.horaInicio} - {self.horaFin}), aula: {self.aula}"


class Grupo(models.Model):
    codigo = models.CharField(max_length=20)
    materia = models.ForeignKey(
        Materia, on_delete=models.CASCADE, related_name="grupos"
    )
    profesores = models.ManyToManyField(Profesor, related_name="grupos")
    horario = models.ForeignKey(
        Horario, on_delete=models.CASCADE, related_name="grupos"
    )

    def __str__(self):
        return f"{self.materia}, codigo: {self.codigo}"


class Foro(models.Model):
    materia = models.OneToOneField(
        Materia, on_delete=models.CASCADE, related_name="foro"
    )
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return f"Foro de {self.materia.nombre}"


class Publicacion(models.Model):
    foro = models.ForeignKey(
        Foro, on_delete=models.CASCADE, related_name="publicaciones"
    )
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, related_name="publicaciones"
    )
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    publicacion = models.ForeignKey(
        Publicacion, on_delete=models.CASCADE, related_name="comentarios"
    )
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, related_name="comentarios"
    )
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.estudiante.nombres} en {self.publicacion.titulo}"


class HorarioAsesoria(models.Model):
    DIAS_SEMANA = [
        ("lunes", "Lunes"),
        ("martes", "Martes"),
        ("miercoles", "Miércoles"),
        ("jueves", "Jueves"),
        ("viernes", "Viernes"),
        ("sabado", "Sábado"),
        ("domingo", "Domingo"),
    ]

    materia = models.ForeignKey(
        Materia, on_delete=models.CASCADE, related_name="horarios_asesoria"
    )
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    lugar = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.materia.nombre}: {self.dia} {self.hora_inicio}-{self.hora_fin} en {self.lugar}"
