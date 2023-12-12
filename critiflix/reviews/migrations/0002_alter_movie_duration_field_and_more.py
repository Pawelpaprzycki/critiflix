# Generated by Django 4.2.6 on 2023-11-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='duration_field',
            field=models.FloatField(blank=True, default='99', null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='publication_dates',
            field=models.DateField(blank=True, default='2000-01-01', null=True, verbose_name='publication date'),
        ),
    ]
