# Generated by Django 5.0 on 2024-01-27 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skapp', '0022_alter_cartmodel_pid_alter_cartmodel_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='pid',
            field=models.IntegerField(),
        ),
    ]
