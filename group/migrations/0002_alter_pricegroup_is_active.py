# Generated by Django 3.2.10 on 2022-07-27 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricegroup',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]