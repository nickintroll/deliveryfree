# Generated by Django 4.2 on 2023-08-16 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_profile_picture'),
        ('jobs', '0011_job_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_viewed', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='answers', to='users.profile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='answers', to='jobs.job')),
            ],
        ),
    ]