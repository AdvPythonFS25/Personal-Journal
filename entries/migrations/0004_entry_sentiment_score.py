# Generated by Django 5.2 on 2025-05-17 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0003_alter_entry_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='sentiment_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
