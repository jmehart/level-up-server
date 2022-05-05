"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models.game_type import GameType
from levelupapi.models.gamer import Gamer


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        # What if we wanted to pass in a query string parameter?
        # The request from the method parameters holds all the information for the request from the client. The request.query_params is a dictionary of any query parameters that were in the url. Using the .get method on a dictionary is a safe way to find if a key is present on the dictionary. If the 'type' key is not present on the dictionary it will return None.
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    '''
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            gamer=gamer,
            game_type=game_type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)
    '''
    
    # Inside the method, the first line of code is getting the game that is logged in. Since all of our postman or fetch requests have the user’s auth token in the headers, the request will get the user object based on that token. From there, we use the request.auth.user to get the Gamer object based on the user. Here’s the equivalent sql:
        # db_cursor.execute("""
        # select *
        # from levelupapi_gamer
        # where user = ?
        # """, (user,))
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    #To add the game to the database, we call the create ORM method and pass the fields as parameters to the function. Here’s the sql that will run:
        # db_cursor.execute("""
        # Insert into levelupapi_game (title, maker, number_of_players, skill_level, gamer_id, game_type_id)
        # values (?, ?, ?, ?, ?, ?)
        # """, (request.data["title"], request.data["maker"], request.data["numberOfPlayers"], request.data["skillLevel"], gamer, game_type)) 
    
    

    # This time, when using the CreateGameSerializer, the original game object is passed to the serializer, along with the request.data. This will make any updates on the game object. Then, just like in the create, check for validity and save the updated object.

    def update(self, request, pk):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
                


# Right now the GET methods do not include any nested data, only the foreign key. Embedding that data is only 1 line of code! Take a look at the response for getting all the games. Notice that game_type is just the id of the type. Back in the GameSerializer add this to the end of Meta class tabbed to the same level as the fields property
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level', 'game_type')
        depth = 1
        
        
        
# Instead of making a new instance of the Game model, the request.data dictionary is passed to the new serializer as the data. The keys on the dictionary must match what is in the fields on the serializer. After creating the serializer instance, call is_valid to make sure the client sent valid data. If the code passes validation, then the save method will add the game to the database and add an id to the serializer.        
        
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']        