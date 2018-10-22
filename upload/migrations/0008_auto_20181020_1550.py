# Generated by Django 2.1.2 on 2018-10-20 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0007_remove_singlefileupload_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlefileupload',
            name='md5sum',
            field=models.CharField(default='NULL', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='singlefileupload',
            name='name',
            field=models.CharField(default='anon', max_length=200),
            preserve_default=False,
        ),
    ]