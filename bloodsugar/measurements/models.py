from django.db import models


# Create your models here.
class Measurement(models.Model):
    ''' Model pomiarów:
    value
    measured_date
    notes
    '''
    value = models.DecimalField(decimal_places=2, max_digits=4)
    measured_date = models.DateField()
    notes = models.TextField(null=True)
