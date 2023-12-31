# Generated by Django 4.2.4 on 2023-09-04 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survivor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], db_index=True, max_length=1)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=12)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=12)),
                ('water', models.IntegerField(default=0)),
                ('food', models.IntegerField(default=0)),
                ('medication', models.IntegerField(default=0)),
                ('ammunition', models.IntegerField(default=0)),
                ('is_infected', models.BooleanField(default=False)),
                ('total_points', models.PositiveIntegerField(default=0)),
                ('received_reports', models.IntegerField(default=0)),
            ],
        ),
    ]
