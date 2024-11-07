# Generated by Django 5.1.2 on 2024-11-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_estudiante_image_alter_profesor_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudiante',
            name='image',
        ),
        migrations.RemoveField(
            model_name='profesor',
            name='image',
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='correoElectronico',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='correoInstitucional',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='correoElectronico',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='correoInstitucional',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]