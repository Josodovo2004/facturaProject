from lxml import etree as ET
from django.http import JsonResponse
from facturacion.api.consultarTicket import consultarTicket
from facturacion.api.resumenComprobantes.stringResumenComprobante import stringResumenComprobante
from facturacion.api.zip_and_encode_base64 import zip_and_encode_base64
from facturacion.api.xml_envio import envio_xml
from facturacion.api.modify_xml import modify_xml
import base64
import os
import zipfile

def emitirResumenComprobante(request):



    data = {
    'cabecera': {
        'tipo_comprobante': 'RC',  # Tipo de comprobante: "RC" para Resumen de Boletas
        'serie': '001',             # Serie del resumen diario
        'correlativo': '00001',     # Correlativo del resumen diario
        'fecha_referencia': '2024-08-20',  # Fecha de emisión de las boletas
        'fecha_envio': '2024-08-21',       # Fecha de envío del resumen diario
    },
    'emisor': {
        'ruc': '20123456789',             # RUC del emisor
        'razon_social': 'Empresa S.A.C.', # Razón social del emisor
    },
    'documentos': [
        {
            'document_type_code': '03',        # Tipo de documento (03 para Boletas)
            'id': 'B001-00000001',             # ID del documento (Serie y número)
            'condition_code': '1',             # Código de condición (1 para documento emitido, 2 para anulado)
            'currency': 'PEN',                 # Moneda
            'total_amount': '100.00',          # Importe total
            'paid_amount': '82.00',           # Importe pagado
            'instruction_id': '01',            # Instrucción (01 para pago total)
            'tax_amount': '18.00',             # Importe total de impuestos
            'tax': [                           # Detalle de los impuestos
                {
                    'tax_amount': '18.00',          # Importe del impuesto
                    'id': '1000',                   # ID del impuesto (1000 para IGV)
                    'name': 'IGV',                  # Nombre del impuesto
                    'tax_type_code': 'VAT',         # Código del tipo de impuesto (VAT para IGV)
                },
            ],
        },
        # Se pueden agregar más documentos siguiendo esta estructura
    ],
}
    
    fileName = f"{data['emisor']['ruc']}-RC-{str(data['cabecera']['fecha_envio']).replace('-','')}-001.xml"

    filePath = stringResumenComprobante(data, fileName)

    modify_xml(filePath)

    encodedZip = zip_and_encode_base64(filePath)

    #obtener la respuesta de sunat
    response = envio_xml(fileName, encodedZip, False)

    zipData = base64.b64decode(encodedZip)

    with open("decoded_file.zip", "wb") as file:
        file.write(zipData)

    # SSL verification (use your .pfk file here)
    certPath = "facturacion/api/certificate/certificado.pfx"  # Replace with your .pfk file path

    # Check if the certificate file exists
    if not os.path.isfile(certPath):
        raise FileNotFoundError(f"Certificate file not found: {certPath}")

    if response.status_code == 200:
        doc = ET.fromstring(response.content)
        ticket_element = doc.find('.//{*}ticket')
        if ticket_element is not None and ticket_element.text:
            ticket = ticket_element.text
            print(f"TODO OK - TICKET: {ticket}")
        else:
            codigo = doc.find('.//{*}faultcode').text
            mensaje = doc.find('.//{*}faultstring').text
            return JsonResponse({'response' : f"error {codigo}: {mensaje}"})
    else:
        print(response.content)
        return JsonResponse({'response' : "Problema de conexion"})
    
    response = consultarTicket(ticket)
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
                return JsonResponse({'response' : "RESUMEN DE COMPROBANTES APROBADO"})
            else:
                print(doc_cdr.find('.//{*}Description').text)
                return  JsonResponse({'response' :f"RESUMEN DE COMPROBANTES RECHAZADO CON CODIGO DE ERROR: {response_code}"})

                

        else:
            codigo = doc.find('.//{*}faultcode').text
            mensaje = doc.find('.//{*}faultstring').text
            return JsonResponse({f"error {codigo}": "{mensaje}"})

    else:
        return JsonResponse({'rsponse' : f"HTTP request failed with status code {status_code}"})