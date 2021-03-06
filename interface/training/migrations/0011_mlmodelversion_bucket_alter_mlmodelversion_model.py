# Generated by Django 4.0.5 on 2022-06-07 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0010_alter_mlmodelversion_trained'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlmodelversion',
            name='bucket',
            field=models.CharField(default='none', max_length=1024, verbose_name='Bucket'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mlmodelversion',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='training.mlmodel'),
        ),
    ]
