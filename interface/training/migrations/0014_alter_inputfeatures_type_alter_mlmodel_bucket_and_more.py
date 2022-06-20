# Generated by Django 4.0.5 on 2022-06-12 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0013_mlmodelversion_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputfeatures',
            name='type',
            field=models.CharField(choices=[('binary', 'Binary'), ('numerical', 'Numerical'), ('category', 'Category'), ('bag', 'Bag'), ('sequence', 'Sequence'), ('vector', 'Vector'), ('audio', 'Audio'), ('date', 'Date'), ('h3', 'H3'), ('image', 'Image'), ('timeseries', 'Time Series')], max_length=1024, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='bucket',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='Bucket'),
        ),
        migrations.AlterField(
            model_name='mlmodelversion',
            name='status',
            field=models.CharField(choices=[('wait', 'Wait to start'), ('training', 'Training'), ('optimizing', 'Optimizing'), ('error', 'Error'), ('finished', 'Finished')], default='wait', max_length=50, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='outputfeatures',
            name='type',
            field=models.CharField(choices=[('binary', 'Binary'), ('numerical', 'Numerical'), ('category', 'Category'), ('bag', 'Bag'), ('sequence', 'Sequence'), ('vector', 'Vector'), ('audio', 'Audio'), ('date', 'Date'), ('h3', 'H3'), ('image', 'Image'), ('timeseries', 'Time Series')], max_length=1024, verbose_name='Type'),
        ),
    ]
