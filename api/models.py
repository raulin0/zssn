from django.db import models


class Survivor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    name = models.CharField(max_length=100, unique=True, db_index=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, db_index=True
    )
    latitude = models.DecimalField(max_digits=12, decimal_places=6)
    longitude = models.DecimalField(max_digits=12, decimal_places=6)
    water = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    medication = models.IntegerField(default=0)
    ammunition = models.IntegerField(default=0)
    is_infected = models.BooleanField(default=False)
    total_points = models.PositiveIntegerField(default=0)
    received_reports = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.total_points = self.calculate_points(
            self.water, self.food, self.medication, self.ammunition
        )
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_points(water, food, medication, ammunition):
        return (water * 4) + (food * 3) + (medication * 2) + ammunition
