# Generated by Django 3.2.5 on 2022-01-17 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightDetails', '0003_alter_flight_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Pending', 'Pending')], default='NONE', max_length=50),
        ),
    ]