# Generated by Django 5.0.6 on 2024-07-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]