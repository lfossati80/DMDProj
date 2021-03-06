# Generated by Django 2.0.1 on 2018-01-11 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('latitude', models.IntegerField(default=0)),
                ('longitude', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.IntegerField(default=0)),
                ('longitude', models.IntegerField(default=0)),
                ('category', models.CharField(default=0, max_length=50)),
                ('radius', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
