from django.db import models


class Ingredient(models.Model):
    """
    Ингредиент
    """

    name = models.CharField(max_length=250, verbose_name='Название')
    measurement_unit = models.CharField(max_length=50,
                                        verbose_name='кг', default='kg')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
