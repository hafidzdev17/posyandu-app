# Generated by Django 3.2 on 2023-09-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posyandu', '0002_auto_20230814_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='petugas',
            name='roles',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Bidan', 'Bidan')], default='Admin', max_length=8, null=True),
        ),
    ]
