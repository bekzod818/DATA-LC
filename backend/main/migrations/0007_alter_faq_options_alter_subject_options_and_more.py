# Generated by Django 4.0.3 on 2022-04-07 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_faq_course'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name': 'Savol - javob', 'verbose_name_plural': 'Savollar'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'Mavzu', 'verbose_name_plural': 'Mavzular'},
        ),
        migrations.RemoveField(
            model_name='course',
            name='content',
        ),
        migrations.RemoveField(
            model_name='course',
            name='subject',
        ),
    ]