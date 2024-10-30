from api.models import (
    TipoDocumento,
    Usuario,
    Profesor,
    Pensum,
    Departamento,
    Carrera,
    Materia,
    Estudiante,
    Horario,
    Grupo,
    Nota,
    Semestre,
)


tipo_documento_1 = TipoDocumento.objects.create(nombre='Cédula', abreviacion='CC')
tipo_documento_2 = TipoDocumento.objects.create(
    nombre='Tarjeta de Identidad', abreviacion='TI'
)


departamento = Departamento.objects.create(nombre='Ciencias Sociales')


pensum = Pensum.objects.create(nombre='Pensum de Psicología')


carrera = Carrera.objects.create(
    nombre='Psicología',
    codigo='PSI',
    pensum=pensum,
    semestres=10,
    modalidad=1,
    tipoCarrera=1,
    departamento=departamento,
)


materia_1 = Materia.objects.create(
    nombre='Psicología General', codigo='PSI101', creditos=3, intensidadHoraria=48
)
materia_2 = Materia.objects.create(
    nombre='Psicología del Desarrollo',
    codigo='PSI102',
    creditos=3,
    intensidadHoraria=48,
)


# horario = Horario.objects.create(
#     horaInicio='08:00', horaFin='10:00', dia=1, aula='A101'
# )


profesor = Profesor.objects.create(
    nombres='Juan',
    apellidos='Pérez',
    codigo='PROF001',
    fechaNacimiento='1980-01-15',
    direccion='Calle 123',
    telefono='1234567890',
    correoElectronico='juan.perez@example.com',
    correoInstitucional='jperez@universidad.edu',
    fechaIngreso='2010-08-15',
    numeroDocumento='12345678',
    tipoDocumento=tipo_documento_1,
)


estudiante = Estudiante.objects.create(
    nombres='Ana',
    apellidos='Gómez',
    codigo='EST001',
    fechaNacimiento='2000-05-20',
    direccion='Calle 456',
    telefono='0987654321',
    correoElectronico='ana.gomez@example.com',
    correoInstitucional='agomez@universidad.edu',
    fechaIngreso='2018-01-01',
    numeroDocumento='87654321',
    tipoDocumento=tipo_documento_2,
    creditosAprobados=30,
    estadoMatricula=1,
)


nota = Nota.objects.create(
    primera=4.5,
    segunda=4.0,
    tercera=5.0,
    cuarta=3.5,
    estudiante=estudiante,
    materia=materia_1,
)


# grupo = Grupo.objects.create(codigo='G1', materia=materia_1, horario=Horario)
# grupo.profesores.add(profesor)


semestre = Semestre.objects.create(numeroSemestre=1, pensum=pensum)
semestre.materias.add(materia_1, materia_2)
