# Generated by Django 3.1 on 2020-08-18 07:25

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200818_0719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judge',
            name='category',
        ),
        migrations.AlterField(
            model_name='judge',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
