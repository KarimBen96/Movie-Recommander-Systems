from django.db import models


class Movie(models.Model):
    movieId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

