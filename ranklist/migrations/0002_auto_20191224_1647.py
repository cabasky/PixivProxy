# Generated by Django 3.0 on 2019-12-24 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranklist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranklist',
            name='rankdate',
            field=models.CharField(max_length=8),
        ),
    ]
