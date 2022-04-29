
   
from django.db import models

class Event(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    # q for text, date, and time field options
    descriptions = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)