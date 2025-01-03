# Generated by Django 5.1.2 on 2024-11-07 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_estudiante_image_profesor_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profesor',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profesor',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profesor',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
