# Generated by Django 4.0.1 on 2022-04-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Foydalanuvchi', 'verbose_name_plural': 'Foydalanivchilar'},
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.TextField(null=True, verbose_name='Kurs mavzulari'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True),
        ),
    ]