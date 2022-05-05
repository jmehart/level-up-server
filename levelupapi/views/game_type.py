"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types view"""



# We’re using the getmethod of the ORM to retrieve a single GameType. This is equivalent to this sql execute:
# db_cursor.execute("""
#     select id, label
#     from levelupapi_gametype
#     where id = ?""",(pk,) 
# )

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        #After getting the game_type, it is passed to the serializer. Lastly, the serializer.data is passed to the Response as the response body. Using Response combines what we were doing with the _set_headers and wfile.write functions.
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data)
        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

#The list method is responsible for getting the whole collection of objects from the database. The ORM method for this one is all. Here’s the code to add to the method:
    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        #When using the allmethod this is the sql that runs:
        # select *
        # from levelupapi_gametype
        game_types = GameType.objects.all()
        # adding many=True to let the serializer know that a list vs. a single object is to be serialized.
        serializer = GameTypeSerializer(game_types, many=True)
        return Response(serializer.data)


# The serializer class determines how the Python data should be serialized to be sent back to the client. Put the following code at the bottom of the same module as above. Make sure it is outside of the view class.
# The Meta class hold the configuration for the serializer. We’re telling the serializer to use the GameType model and to include the id andlabel fields.
# look at urls.py to see how url is used for view
class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = GameType
        fields = ('id', 'label')