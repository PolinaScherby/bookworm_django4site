# Generated by Django 4.2.1 on 2024-03-11 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='is_published',
        ),
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20),
        ),
    ]