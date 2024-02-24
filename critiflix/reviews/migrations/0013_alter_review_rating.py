# Generated by Django 4.2.6 on 2024-02-24 14:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_alter_movie_publication_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(default=0, help_text='Rating of the movie/series from 0 to 10.', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]