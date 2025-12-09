from django.db import models
from users.models import CustomUser

class Household(models.Model):
    name = models.CharField(max_length=100) 
    
    owner = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='owned_household'
    )
    
    members = models.ManyToManyField(
        CustomUser, 
        related_name='member_households',
        blank=True
    )

    def __str__(self):
        return self.name