from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


# Create your models here.
class ScrapeHistory(models.Model):
    site_name = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now=True)
    site_url = models.URLField(default="null")
    class Meta:
        verbose_name_plural = "Scrape History"
    # def __str__(self):
    #     td = (timezone.now()-self.last_updated)
    #     days = td.days
    #     hours, remainder = divmod(td.seconds, 3600)
    #     minutes, seconds = divmod(remainder, 60)
    #     return f"{self.site_name} - {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
        
    
    
class QueryHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=200)
    response = models.TextField()
    
    class Meta:
        verbose_name_plural = "Query History"
    