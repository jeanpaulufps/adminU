# Generated by Django 5.1.1 on 2024-10-28 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('codigo', models.CharField(max_length=20)),
                ('estado', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pensum',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombre', models.CharField(default=' ', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombres', models.CharField(default=' ', max_length=50)),
                ('apellidos', models.CharField(default=' ', max_length=50)),
                ('codigo', models.CharField(max_length=50)),
                ('fechaNacimiento', models.DateField()),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('correoElectronico', models.CharField(max_length=50)),
                ('correoInstitucional', models.CharField(max_length=50)),
                ('fechaIngreso', models.DateField()),
                ('numeroDocumento', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombre', models.CharField(max_length=50)),
                ('abreviacion', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=20)),
                ('semestres', models.IntegerField()),
                ('modalidad', models.IntegerField()),
                ('tipoCarrera', models.IntegerField()),
                (
                    'departamento',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='carreras',
                        to='api.departamento',
                    ),
                ),
                (
                    'pensum',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='carreras',
                        to='api.pensum',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('horaInicio', models.TimeField()),
                ('horaFin', models.TimeField()),
                ('dia', models.IntegerField()),
                (
                    'aula',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='aula',
                        to='api.aula',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=20)),
                ('creditos', models.IntegerField()),
                ('intensidadHoraria', models.IntegerField()),
                (
                    'requisito',
                    models.ManyToManyField(
                        blank=True, related_name='materias_requisito', to='api.materia'
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombres', models.CharField(default=' ', max_length=50)),
                ('apellidos', models.CharField(default=' ', max_length=50)),
                ('codigo', models.CharField(max_length=50)),
                ('fechaNacimiento', models.DateField()),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('correoElectronico', models.CharField(max_length=50)),
                ('correoInstitucional', models.CharField(max_length=50)),
                ('fechaIngreso', models.DateField()),
                ('numeroDocumento', models.CharField(max_length=20)),
                ('creditosAprobados', models.IntegerField()),
                ('estadoMatricula', models.IntegerField()),
                ('carrera', models.ManyToManyField(to='api.carrera')),
                (
                    'materiasMatriculadas',
                    models.ManyToManyField(
                        null=True,
                        related_name='estudiantes_matriculados',
                        to='api.materia',
                    ),
                ),
                (
                    'tipoDocumento',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='api.tipodocumento',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('primera', models.FloatField()),
                ('segunda', models.FloatField()),
                ('tercera', models.FloatField()),
                ('cuarta', models.FloatField()),
                (
                    'estudiante',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='notas',
                        to='api.estudiante',
                    ),
                ),
                (
                    'materia',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='notas',
                        to='api.materia',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('codigo', models.CharField(max_length=20)),
                (
                    'horario',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='grupos',
                        to='api.horario',
                    ),
                ),
                (
                    'materia',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='grupos',
                        to='api.materia',
                    ),
                ),
                (
                    'profesores',
                    models.ManyToManyField(related_name='grupos', to='api.profesor'),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('numeroSemestre', models.IntegerField()),
                (
                    'materias',
                    models.ManyToManyField(related_name='semestres', to='api.materia'),
                ),
                (
                    'pensum',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='semestres',
                        to='api.pensum',
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='profesor',
            name='tipoDocumento',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='api.tipodocumento',
            ),
        ),
    ]
