from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('greentech', '0002_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=20, blank=True),
        ),
    ] 