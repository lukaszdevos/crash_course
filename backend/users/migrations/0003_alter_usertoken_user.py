# Generated by Django 3.2.9 on 2021-11-11 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usertoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token', to=settings.AUTH_USER_MODEL),
        ),
    ]
