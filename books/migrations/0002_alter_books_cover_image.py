# Generated by Django 4.2.17 on 2024-12-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='cover_image',
            field=models.FileField(blank=True, null=True, upload_to='books/', verbose_name='Cover Image'),
        ),
    ]
