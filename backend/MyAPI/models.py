from django.db import models



class Movie(models.Model):
  id = models.IntegerField(("movieId"), primary_key=True)
  title = models.CharField(("title"), max_length=255)
  genres = models.CharField(("genres"), max_length=255)

  def __str__(self):
    return self.title