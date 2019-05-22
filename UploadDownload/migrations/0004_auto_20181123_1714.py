# Generated by Django 2.1.2 on 2018-11-23 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
        ('UploadDownload', '0003_auto_20181123_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlefileupload',
            name='username_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Authentication.SpcUser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='singlefileupload',
            name='username',
            field=models.CharField(max_length=200),
        ),
    ]