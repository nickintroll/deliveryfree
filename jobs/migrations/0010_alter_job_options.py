# Generated by Django 4.2.1 on 2023-06-04 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_alter_comment_answer_to'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ('-created',)},
        ),
    ]