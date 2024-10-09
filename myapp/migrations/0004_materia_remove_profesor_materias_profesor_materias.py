# Generated by Django 5.1.1 on 2024-10-09 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_profesor"),
    ]

    operations = [
        migrations.CreateModel(
            name="Materia",
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
                ("codigo", models.CharField(max_length=20)),
                ("creditos", models.IntegerField()),
                ("intensidadHoraria", models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name="profesor",
            name="materias",
        ),
        migrations.AddField(
            model_name="profesor",
            name="materias",
            field=models.ManyToManyField(to="myapp.materia"),
        ),
    ]