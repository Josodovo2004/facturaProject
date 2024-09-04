import os

environment = os.getenv('development', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import *