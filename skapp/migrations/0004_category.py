# Generated by Django 5.0 on 2023-12-21 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skapp', '0003_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
