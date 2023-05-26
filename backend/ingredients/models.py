from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    measurement_unit = models.CharField(max_length=50, verbose_name='кг', default='kg')
    
    def __str__(self):
        return self.name