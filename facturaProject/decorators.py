from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from functools import wraps
from rest_framework.response import Response
from .settings import DEBUG

# Custom JWT authentication that only validates the token, no user lookup
class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # Skip user lookup, just return None (since no user is required in this case)
        return None

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):  # Include 'self'
        auth = CustomJWTAuthentication()  # Use the custom class
        try:
            if DEBUG:
                return view_func(self, request, *args, **kwargs)  # No authentication in development mode
        
            # Validate the token and get the user without fetching from the database
            user, token = auth.authenticate(request)

            if token is None:  # This will check if authentication was successful
                return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

            # Proceed to the view if token is valid
            # You can add any additional logic here if needed

        except (TokenError, InvalidToken) as e:
            # Return an error response if token is invalid
            return Response({'tokenerror': str(e)}, status=401)

        # If valid, execute the view function
        return view_func(self, request, *args, **kwargs)  # Pass 'self'

    return _wrapped_view