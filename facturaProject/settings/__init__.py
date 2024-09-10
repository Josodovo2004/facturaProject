import os

environment = os.getenv('development', 'development')

if environment == 'pro':
    print('Servidor de Produccion')
    from .production import *
    
else:
    print('Servidor de Desarrollo')
    from .development import *
    