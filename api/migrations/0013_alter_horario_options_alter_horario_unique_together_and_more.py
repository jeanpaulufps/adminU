# Generated by Django 5.1.2 on 2024-11-15 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_horario_materia'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='horario',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='horario',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='horario',
            name='grupo',
        ),
    ]
