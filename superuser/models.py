from django.db import models



# Create your models here.
class ElectionSchedule(models.Model):
    pincode=models.CharField(max_length=6,unique=True)
    date=models.DateField()
    startTime=models.TimeField()
    endTime=models.TimeField()
    
    def __str__(self):
        return f'{self.pincode}'



