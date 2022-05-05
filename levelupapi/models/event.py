from django.db import models

class Event(models.Model):
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    # q for text, date, and time field options
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("gamer", through="eventGamer", related_name="events")
    
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
    
    # Normally, every property on a Model class in Django directly reflects a column on a table in the database. Sometimes, though, you need additional properties on a model that are calculated during a request/response cycle with a client.
    # You are going to add a joined custom property to the Event class that will let the client application know if the currently authenticated user can join a particular event.    
    # When that user is authenticated, and the client requests a list of all events, there should be a new joined key on each event. If the user is going to that event it’s value should be true, if not false. That data is not in the database, but rather calculated by the view logic.
    # Then update serializer in views to include new custom property
        
        
# In terminal:
# create a migration to create the tables in your database:
    # command = python3 manage.py makemigrations levelupapi       
# execute your migrations and create the tables in your database:   
    # command = python3 manage.py migrate