import requests

def envio_xml(comprobante, fileName, encodedZip, tipo=True):
    ca_bundle_path = "facturacion/api/certificate/cacert.pem"  # Replace with the path to your cacert.pem file
    if tipo:
        letra = 'sendBill'
    else:
        letra = 'sendSummary'

    xml_envio = f'''<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
            xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.sunat.gob.pe" 
            xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
        <soapenv:Header>
            <wsse:Security>
                <wsse:UsernameToken>
                    <wsse:Username>{comprobante.emisor.numeroDocumento}{comprobante.emisor.usuarioSol}</wsse:Username>
                    <wsse:Password>{comprobante.emisor.claveSol}</wsse:Password>
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


    # The web service URL
    ws = "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService"

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
    try:
        response = requests.post(url=ws, data=xml_envio, headers=headers, verify=ca_bundle_path)
        response.raise_for_status()  # Raise an exception for HTTP error codes
    except requests.RequestException as e:
        print(f"Error sending request: {e}")
        return None

    return response
