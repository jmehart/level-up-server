from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from levelupapi.models import Gamer


# Tokens are used by a server and its clients. When the user first registers on the client a unique token is created for that user. The client uses the token in all fetch calls to the server to identify the user making the request.
# The Token is sent back to the client so that it can be used on future requests to identify the user. This way, the user doesn't have to keep filling out their username and password each time a new action is performed.
# an authentication token identifies a user, and not their primary key.
# The last step is to establish some URL routes that any client application can use to register and login a gamer to use the API. - look in urls.py file
# Run 'python3 manage.py runserver' in server terminal to start django app


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
    request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
    request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    # Now save the extra info in the levelupapi_gamer table
    gamer = Gamer.objects.create(
        bio=request.data['bio'],
        user=new_user
    )

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=gamer.user)
    # Return the token to the client
    data = { 'token': token.key }
    return Response(data)
