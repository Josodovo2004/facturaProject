from lxml import etree as ET
import xmlsec
from django.http import JsonResponse
from .stringAnulacionF import stringAnulacionF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from datetime import timedelta, date
from facturacion.api.consultarTicket import consultarTicket
from facturacion.api.xml_envio import envio_xml
from facturacion.api.zip_and_encode_base64 import zip_and_encode_base64
from facturacion.api.modify_xml import modify_xml
import io
import zipfile
import base64
import os
import xmlsec
import requests
from facturacion.models import Comprobante, Entidad, Item, ItemImpuesto, ComprobanteItem
import zipfile
import io

def emitirComunicadoAnulacion(request):
    idComprobante = request.GET.get('comprobante_id')
    motivo = request.GET.get("motivo")
    comprobante: Comprobante = Comprobante.objects.filter(id = idComprobante).first()
    
    data = {
        "comunicado": {
            "id" : f'RA-{str(date.today()).replace("-", "")}-1',
            "fecha" : date.today(),
        },
        "emisor" : {
            "documento" : comprobante.emisor.numeroDocumento,
            "tipoDocumento" : comprobante.emisor.tipoDocumento.codigo,
            "RazonSocial" : comprobante.emisor.razonSocial,	
        },
        "comprobante" : {
            "fecha" : comprobante.fechaEmision,
            "tipoDocumento" : comprobante.tipoComprobante.codigo,
            "serie" : comprobante.serie,
            "numero" : comprobante.numeroComprobante,
            "motivo" : motivo,
        }
    }

    fileName = comprobante.emisor.numeroDocumento+ '-' + data["comunicado"]["id"] + ".xml"

    filePath = stringAnulacionF(data, fileName)
    
    modify_xml(filePath)

    encodedZip = zip_and_encode_base64(filePath)

    #obtener la respuesta de sunat
    response = envio_xml(comprobante, fileName, encodedZip, False)

    zipData = base64.b64decode(encodedZip)

    with open("decoded_file.zip", "wb") as file:
        file.write(zipData)

    # SSL verification (use your .pfk file here)
    certPath = "facturacion/api/certificate/certificado.pfx"  # Replace with your .pfk file path

    # Check if the certificate file exists
    if not os.path.isfile(certPath):
        raise FileNotFoundError(f"Certificate file not found: {certPath}")

    # PASO 06 - OBTENEMOS EL TICKET
    if response.status_code == 200:
        doc = ET.fromstring(response.content)
        ticket_element = doc.find('.//{*}ticket')
        if ticket_element is not None and ticket_element.text:
            ticket = ticket_element.text
            print(f"TODO OK - TICKET: {ticket}")
        else:
            codigo = doc.find('.//{*}faultcode').text
            mensaje = doc.find('.//{*}faultstring').text
            JsonResponse({'response' : f"error {codigo}: {mensaje}"})
    else:
        print(response.content)
        return JsonResponse({'response' : "Problema de conexion"})
        

# PASO 07 - CONSULTAMOS EL TICKET

    response = consultarTicket(comprobante, ticket)
    status_code = response.status_code

    carpetacdr = f'cdr/{str(fileName).replace('.xml','')}'

    if status_code == 200:
        doc = ET.fromstring(response.content)
        content_element = doc.find('.//{*}content')
        if content_element is not None and content_element.text:
            cdr = base64.b64decode(content_element.text)
            cdr_path = os.path.join(carpetacdr, f"R-{fileName.replace(".xml", ".ZIP")}")
            os.makedirs(carpetacdr, exist_ok=True)
            with open(cdr_path, 'wb') as f:
                f.write(cdr)

            with zipfile.ZipFile(cdr_path, 'r') as zip_ref:
                zip_ref.extractall(carpetacdr)

            print("RESUMEN CONSULTADO CORRECTAMENTE")
            
            cdr_file_folder = os.path.join(carpetacdr, f'R-{fileName}')
            os.makedirs(os.path.dirname(cdr_file_folder), exist_ok=True)
            with open(cdr_file_folder, 'r', encoding='utf-8') as cdr_file:
                cdr_content = cdr_file.read()   

            doc_cdr = ET.fromstring(cdr_content.encode('utf-8'))

            response_code = doc_cdr.find('.//{*}ResponseCode').text

            if response_code == "0":
                return JsonResponse({'response' : "RESUMEN DE ANULACIONES APROBADO"})
            else:
                JsonResponse({'response' :f"RESUMEN DE ANULACIONES RECHAZADO CON CODIGO DE ERROR: {response_code}"})

            print(doc_cdr.find('.//{*}Description').text)

        else:
            codigo = doc.find('.//{*}faultcode').text
            mensaje = doc.find('.//{*}faultstring').text
            JsonResponse({f"error {codigo}": "{mensaje}"})

    else:
        JsonResponse({'rsponse' : f"HTTP request failed with status code {status_code}"})