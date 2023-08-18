# Generated by Django 4.2.1 on 2023-06-04 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_age_profile_description_profile_education_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=100)),
                ('usr1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='chats1', to='users.profile')),
                ('usr2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='chats2', to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages', to='users.chat')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages', to='users.profile')),
            ],
        ),
    ]