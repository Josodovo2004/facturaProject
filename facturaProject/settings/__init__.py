import facturaProject.awsData as awsData
import os

environment = awsData.development

if environment == 'pro':
    print('Servidor de Produccion')
    from .production import *
    
else:
    print('Servidor de Desarrollo')
    from .development import *


url_preuba = awsData.urlPrueba
urlProduccion = awsData.urlProduccion

userSol = awsData.userSol
passwordSol = awsData.claveSol
rucSol = awsData.RucSol

passwordP12 = awsData.passwordP12

