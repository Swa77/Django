# Generated by Django 3.2.5 on 2022-01-17 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flightDetails', '0002_auto_20220117_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightDetails.customer'),
        ),
    ]
