# Generated by Django 4.0.5 on 2022-06-07 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0005_rename_models_inputfeatures_model'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MLModelTraining',
            new_name='MLModelVersion',
        ),
    ]
