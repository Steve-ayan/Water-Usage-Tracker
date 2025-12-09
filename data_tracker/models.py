from django.db import models
from households.models import Household 
class DailyUsage(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    
    date = models.DateField() 
    
    volume_liters = models.DecimalField(max_digits=8, decimal_places=2) 
    
    class Meta:
        unique_together = ('household', 'date') 
        ordering = ['-date']
            
    def __str__(self):
        return f"{self.household.name} - {self.date}: {self.volume_liters} L"