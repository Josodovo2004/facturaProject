import requests
def consultarTicket(comprobante, ticket):

    xml_envio = f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
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
            <ser:getStatus>
                <ticket>{ticket}</ticket>
            </ser:getStatus>
        </soapenv:Body>
    </soapenv:Envelope>'''

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "Accept": "text/xml",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "SOAPAction": "",
        "Content-Length": str(len(xml_envio))

    }

    ws = "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService"

    response = requests.post(ws, data=xml_envio, headers=headers, verify=True)

    return response