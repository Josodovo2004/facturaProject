import requests
from facturaProject.settings import DEBUG, cacert, url_preuba, urlProduccion, userSol, passwordSol, rucSol
import facturaProject.awsData as awsData


def envio_xml(fileName, encodedZip, tipo=True):
    ca_bundle_path = cacert  # Replace with the path to your cacert.pem file
    if tipo:
        letra = 'sendBill'
    else:
        letra = 'sendSummary'


    if DEBUG:
        ws = url_preuba
    else:
        ws = urlProduccion

    xml_envio = f'''<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
            xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.sunat.gob.pe" 
            xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
        <soapenv:Header>
            <wsse:Security>
                <wsse:UsernameToken>
                    <wsse:Username>{rucSol}{userSol}</wsse:Username>
                    <wsse:Password>{passwordSol}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </soapenv:Header>
        <soapenv:Body>
            <ser:{letra}>
                <fileName>{fileName.replace(".xml", ".ZIP")}</fileName>
                <contentFile>{encodedZip}</contentFile>
            </ser:{letra}>
        </soapenv:Body>
    </soapenv:Envelope>'''

    # Headers
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "Accept": "text/xml",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "SOAPAction": "",
        "Content-Length": str(len(xml_envio))
    }

    # Send the request

    response = requests.post(url=ws, data=xml_envio, headers=headers, verify=ca_bundle_path)
    response.raise_for_status()  # Raise an exception for HTTP error codes
    
    return response
