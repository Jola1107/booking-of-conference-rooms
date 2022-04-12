# Generated by Django 4.0.3 on 2022-04-12 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_rooms_projector_alter_rooms_seats'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField(null=True)),
                ('id_reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.rooms')),
            ],
        ),
    ]
