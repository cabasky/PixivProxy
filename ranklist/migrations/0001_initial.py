# Generated by Django 3.0.1 on 2020-01-16 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RankList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.IntegerField(choices=[(0, 'daily'), (1, 'weekly'), (2, 'monthly'), (3, 'rookie'), (4, 'male'), (5, 'female')])),
                ('rankdate', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='RankWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artworkid', models.DecimalField(decimal_places=0, max_digits=10)),
                ('name', models.CharField(max_length=40)),
                ('artist', models.CharField(max_length=40)),
                ('artistid', models.DecimalField(decimal_places=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.DecimalField(decimal_places=0, max_digits=2)),
                ('rankl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranklist.RankList')),
                ('rankw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranklist.RankWork')),
            ],
        ),
    ]
