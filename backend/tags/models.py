from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=250, verbose_name='Тег', unique=True)
    color = models.CharField(max_length=7, verbose_name='Цвет', unique=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug'
    )

    def __str__(self):
        return self.name
