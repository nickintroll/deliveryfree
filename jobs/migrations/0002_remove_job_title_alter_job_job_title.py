# Generated by Django 4.2.1 on 2023-05-26 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='title',
        ),
        migrations.AlterField(
            model_name='job',
            name='job_title',
            field=models.CharField(max_length=120),
        ),
    ]
