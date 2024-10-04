# Generated by Django 5.1.1 on 2024-10-04 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Estudiante",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("codigo", models.CharField(max_length=100)),
                ("fechaNacimiento", models.DateField()),
                ("direccion", models.CharField(max_length=255)),
                ("telefono", models.CharField(max_length=100)),
                ("correoElectronico", models.CharField(max_length=100)),
                ("correoInstitucional", models.CharField(max_length=100)),
                ("fechaIngreso", models.DateField()),
                ("numeroDocumento", models.CharField(max_length=32)),
                ("tipoDocumento", models.CharField(max_length=10)),
                ("creditosAprobados", models.IntegerField()),
                ("estadoMatricula", models.IntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="Usuario",
        ),
    ]
