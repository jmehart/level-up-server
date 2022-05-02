from django.db import models

class Event(models.Model):
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    # q for text, date, and time field options
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("gamer", on_delete=models.CASCADE)