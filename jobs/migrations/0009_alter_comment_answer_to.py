# Generated by Django 4.2.1 on 2023-05-31 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_alter_comment_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='answer_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='answers', to='jobs.comment'),
        ),
    ]
