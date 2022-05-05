"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models.game import Game
from levelupapi.models.gamer import Gamer


# The ViewSet has all of the logic for handling an incoming request from a client, determining what action is needed (i.e. create data, get data, update data, or delete data), interacting with the database to do what the client asked, and then constructing a response to the client.
# The Serializer has a much simpler job. Once the ViewSet has determined what kind of response should be sent to the client, if that response has any data, the Serializer converts the Python data into JSON format.

# retrieve -> GET requests that have an id in the url, ex: /animals/1
# list -> GET requests that will return a list of everything in that table
# create -> POST requests to add a row to that table
# update -> PUT requests to update a row in the table
# destroy -> DELETE requests to delete a row in the table Each of those methods will use the Django ORM (Object Relational Mapper) to carry out any retrievals or modifications to the database.

# Workflow:
# Any time that you want to allow a client to access data in your database, there's a series of steps you have to follow in order to accomplish it with Django REST Framework. So far we’ve only written the models. The next step is writing the views and serializers so the client can access and manipulate the data in the database.

class EventView(ViewSet):
    """Level up game types view"""

#The retrieve method will get a single object from the database based on the pk (primary key) in the url. We’ll use the ORM to get the data, then the serializer to convert the data to json. 
    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            gamer = Gamer.objects.get(user=request.auth.user) 
            event.joined = gamer in event.attendees.all()   
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    
    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=gamer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    # def update(self, request, pk):
    #     """Handle PUT requests for a game
        
    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
        
    #     event = Event.objects.get(pk=pk)
    #     event.description = request.data["description"]
    #     event.date = request.data['date']
    #     event.time = request.data['time']
        
    #     game = Game.objects.get(pk=request.data['game_id'])
    #     organizer = Gamer.objects.get(user=request.auth.user)
        
    #     event.game = game
    #     event.organizer = organizer
        
    #     event.save()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    
    # The update method will handle the PUT requests to the resource. 
    
    def update(self, request, pk):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    
    # The destroy method handles DELETE requests to the view. This will be how we delete a row from the database.
    # Just like the retrieve and update methods, the destroy method take the pk as an argument. We’ll use that pk to get the single object, then call the delete from the ORM to remove it from the database. The response will send back a 204 status.
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT) 
    
    
    # Custom actions on a view allow for more than just basic CRUD functionality.
    # a custom action allows the client to put a verb at the end of the URL to initiate a custom action.
    # a custom action can specify which HTTP methods are supported by it.
    # With Django REST Framework, you can create a custom action that your API will support by using the @action decorator above a method within a ViewSet.
    # Using the action decorator turns a method into a new route. In this case, the action will accept POST methods and because detail=True the url will include the pk. Since we need to know which event the user wants to sign up for we’ll need to have the pk. The route is named after the function. So to call this method the url would be http://localhost:8000/events/2/signup
    # The add method on attendees creates the relationship between this event and gamer by adding the event_id and gamer_id to the join table. The response then sends back a 201 status code.
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer left'}, status=status.HTTP_204_NO_CONTENT)    
        
    

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'organizer', 'time', 'game', 'attendees', 'joined')
        depth = 2
        
        
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'description', 'date', 'game', 'time']      
        

# The Meta class inside the serializer holds the configuration info to use for the serializer. It always needs to know:
# Which model to use
# Which fields to serialize          