from django.db import models

# Create your models here.
# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    icon = models.ImageField(upload_to='images/departments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated_at']