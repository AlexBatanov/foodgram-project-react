# Generated by Django 4.2.1 on 2023-05-28 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Изображение блюда'),
        ),
    ]