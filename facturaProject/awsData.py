import boto3

# Initialize the SSM client
ssm = boto3.client('ssm', 'us-east-1')

service = 'FacturaProject'

# Getting shared key (SecureString with decryption)
response = ssm.get_parameter(Name='/Qickart/dev/auth-shared-key', WithDecryption=True)
sharedKey = response['Parameter']['Value']

# Getting encrypted database password with decryption
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/PASSWORDDB', WithDecryption=True)
passwordDb = response['Parameter']['Value']



#--------datos usuarioSol-------#
userSol = 'MCCULEIN'
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/CLAVESOL', WithDecryption=True)
claveSol = response['Parameter']['Value']
RucSol = '20605138293'


#secret key para user authentication
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/SECRET_KEY', WithDecryption=True)
secret_key = response['Parameter']['Value']

#urls de sunat
urlPrueba = 'https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billServices'
urlProduccion = 'https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService?wsdl'

#contraseña para la firma digital de los archivos
response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/PASSWORDp12', WithDecryption=True)
passwordP12 = response['Parameter']['Value']


response = ssm.get_parameter(Name=f'/Qickart/dev/{service}/passwordPfx', WithDecryption=True)
passwordPfx = response['Parameter']['Value']