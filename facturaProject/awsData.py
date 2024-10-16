import boto3

# Initialize the SSM client
ssm = boto3.client('ssm', 'us-east-1')

service = 'FacturaProject'

# Getting shared key (SecureString with decryption)
response = ssm.get_parameter(Name='/Qickart/dev/auth-shared-key', WithDecryption=True)
sharedKey = response['Parameter']['Value']

# Getting database engine
response = ssm.get_parameter(Name='/Qickart/dev/postgresEngine')
dbEngine = response['Parameter']['Value']

# Getting database name
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/NAMEDB')
nameDb = response['Parameter']['Value']

# Getting database user
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/USERDB')
userDb = response['Parameter']['Value']

# Getting encrypted database password with decryption
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/PASSWORDDB', WithDecryption=True)
passwordDb = response['Parameter']['Value']

# Getting database port
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/PORTDB')
portDb = response['Parameter']['Value']

# Getting database host
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/HOSTDB')
hostDb = response['Parameter']['Value']


#--------datos usuarioSol-------#
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/USERSOL', WithDecryption=True)
userSol = response['Parameter']['Value']
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/CLAVESOL', WithDecryption=True)
claveSol = response['Parameter']['Value']
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/RUCSOL')
RucSol = response['Parameter']['Value']


#secret key para user authentication
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/SECRET_KEY', WithDecryption=True)
secret_key = response['Parameter']['Value']

#ver si estamos en estado de prueba o de produccion
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/DEBUG')
debugStatus = response['Parameter']['Value']

#urls de sunat
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/URL_PRUEBA')
urlPrueba = response['Parameter']['Value']
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/URL_PRODUCCION')
urlProduccion = response['Parameter']['Value']

#contraseña para la firma digital de los archivos
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/PASSWORDp12', WithDecryption=True)
passwordP12 = response['Parameter']['Value']


response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/passwordPfx', WithDecryption=True)
passwordPfx = response['Parameter']['Value']