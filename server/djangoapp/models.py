# models.py

from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=100)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    year = models.IntegerField()
    dealer_id = models.IntegerField(null=True, blank=True)  # Make dealer_id optional

    def __str__(self):
        return f"{self.name} ({self.car_make})"
