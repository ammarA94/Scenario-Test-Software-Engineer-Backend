# Generated by Django 4.0.3 on 2022-03-14 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoreApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='RegisterDate',
            field=models.DateTimeField(auto_now_add=True, db_column='RegisterDate'),
        ),
    ]
