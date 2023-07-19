# Generated by Django 3.1.3 on 2021-08-14 07:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('santri', '0025_remove_walisantri_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pengguna',
            new_name='Pengurus',
        ),
        migrations.RenameField(
            model_name='pengurus',
            old_name='nama_pengguna',
            new_name='nama_pengurus',
        ),
    ]
