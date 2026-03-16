# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='book',
            name='image_url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
