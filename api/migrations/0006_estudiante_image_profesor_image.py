# Generated by Django 5.1.2 on 2024-11-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_estudiante_carrera'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='image',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profesor',
            name='image',
            field=models.CharField(default=' ', max_length=255, null=True),
        ),
    ]
