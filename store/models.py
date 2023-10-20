from django.db import models

# Create your models here.
 
 
class Course(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=500)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='uploads/course/', blank=True, null=True)
    
    def __str__(self):
        return self.title