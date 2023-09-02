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
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    is_infected = models.BooleanField(default=False)
    total_points = models.PositiveIntegerField(default=0)

    @classmethod
    def calculate_total_points(cls, survivor_id):
        survivor = cls.objects.prefetch_related('inventory_set').get(
            id=survivor_id
        )

        total_points = survivor.inventory_set.aggregate(
            total_points=models.Sum(
                models.F('quantity') * models.F('resource__points')
            )
        )['total_points']

        survivor.total_points = total_points or 0
        survivor.save()


class Resource(models.Model):
    resource = models.CharField(max_length=20, unique=True, db_index=True)
    points = models.IntegerField()


class Inventory(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('survivor', 'resource')


class InfectionReport(models.Model):
    reporter = models.ForeignKey(
        Survivor,
        related_name='reported_reports',
        on_delete=models.CASCADE,
        db_index=True,
    )
    reported_survivor = models.ForeignKey(
        Survivor,
        related_name='received_reports',
        on_delete=models.CASCADE,
        db_index=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reporter', 'reported_survivor')

    @classmethod
    def infection_check(cls, survivor):
        report_count = cls.objects.filter(reported_survivor=survivor).count()
        if report_count >= 3 and not survivor.is_infected:
            survivor.is_infected = True
            survivor.save()
