# Generated by Django 4.2.17 on 2024-12-13 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0003_librarymanagement_decision_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarymanagement',
            name='decision_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decision_by', to=settings.AUTH_USER_MODEL),
        ),
    ]