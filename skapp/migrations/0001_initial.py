# Generated by Django 5.0 on 2023-12-18 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, null=True)),
                ('contact', models.CharField(max_length=20)),
                ('message', models.TextField(null=True)),
                ('enq_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
