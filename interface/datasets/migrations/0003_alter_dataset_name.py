# Generated by Django 4.0.5 on 2022-06-06 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0002_dataset_query'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Name'),
        ),
    ]
