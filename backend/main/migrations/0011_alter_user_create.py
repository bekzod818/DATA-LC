# Generated by Django 4.0.3 on 2022-04-07 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_user_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create',
            field=models.DateTimeField(null=True, verbose_name="Qo'shilgan vaqt"),
        ),
    ]