# Generated by Django 5.1.4 on 2025-02-12 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_course_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='amount',
            field=models.IntegerField(default=1, help_text='Укажите цену в рублях', verbose_name='Цена'),
        ),
    ]
