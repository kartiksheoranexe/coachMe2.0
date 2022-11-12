# Generated by Django 4.1.3 on 2022-11-12 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coachMe', '0007_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('current_package_name', models.CharField(max_length=100)),
                ('package_desc', models.CharField(max_length=254)),
                ('duration_type', models.CharField(choices=[('Y', 'Years'), ('M', 'Months'), ('D', 'Days')], max_length=1)),
                ('duration', models.IntegerField()),
                ('price_paid', models.IntegerField()),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coachMe.coach')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]